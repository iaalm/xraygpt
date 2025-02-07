import json
from typing import List, Optional, Tuple
from uuid import uuid4

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger

from xraygpt.db.base import Item


async def _gross_recognize_entities(text: str, llm: ChatOpenAI) -> List[str]:
    # Define the prompt with a structured JSON schema
    response_schemas = [
        ResponseSchema(
            name="item", description="An array of entity names", type="[string]"
        ),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    chat_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are an agent to help me recognize named entities in text, give me the entities based on following rules\n1. Entities are only people's names\n2. Outputs should following the format: {format_instructions}"
            ),
            HumanMessagePromptTemplate.from_template("{text}"),
        ],
        input_variables=["text"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    chain = chat_template | llm | output_parser

    resp = await chain.ainvoke({"text": text})
    logger.debug("{num_items} items recognized grossly", num_items=len(resp["item"]))
    return resp["item"]


async def _refine_recognized_entity(
    text: str, name: str, items: List[Item], llm
) -> Tuple[List[Item], Optional[Item]]:
    logger.debug(
        "Refining recognized entity: {name} with {num_items} references",
        name=name,
        num_items=len(items),
    )
    response_schemas = [
        ResponseSchema(
            name="to_delete",
            description="An array of entity ids to delete",
            type="[int]",
        ),
        ResponseSchema(
            name="entity_name",
            description="Array of entity names of single entity",
            type="[string]",
        ),
        ResponseSchema(
            name="entity_description", description="entity description", type="string"
        ),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    chat_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                'You are an assistant tasked with refining a specific entity from text. Given the recognized entity "{name}" and related database information, your tasks are:\n1. Identify if the entity "{name}" is incorrect, irrelevant, or outdated, and mark it for deletion if necessary.\n2. If the text provides more important or detailed information, update the entity by deleting it and adding a new one\n3. If you found multiple "existing entity" are actually same entity, merge them by remove all and add a new one with all their names\n4. Ensure the updated entity name remains accurate. Each eneity often have multiple names, e.g. nick name, full name, first name, last name. Put all names you know into "eneity_name" and make sure full name as first one\n5. Each related entities are marked with an ID in []. To delete provide the ID in "to_delete"\n6. Provide a simple and concise entity description with less than 100 words. When new infomation appearred for same entity, remove less important information and keep critial infomation like age, relationship, occupation, title, birthday, etc.7. DO NOT any information not in context.\nOnly process and output information for the entity "{name}".\nYour output must follow this format: {format_instructions}'
            ),
            HumanMessagePromptTemplate.from_template("Existing entity:\n{reference}"),
            HumanMessagePromptTemplate.from_template("{text}"),
        ],
        input_variables=["text", "name", "reference"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    chain = chat_template | llm | output_parser

    references = [(json.dumps(i["name"]), i["description"]) for i in items]
    reference_description = "\n".join(
        [f"[{ix}]: {n}: {d}" for ix, (n, d) in enumerate(references)]
    )
    resp = chain.invoke(
        {"text": text, "name": name, "reference": reference_description}
    )
    logger.trace(
        "Reference description: {reference_description}",
        reference_description=reference_description,
    )
    to_delete = [i for i in resp["to_delete"] if i < len(items)]
    if len(to_delete) != len(resp["to_delete"]):
        logger.warning(
            "Some items to delete are invalid: {to_delete}", to_delete=resp["to_delete"]
        )
    item_to_delete = [items[i] for i in to_delete]
    name_to_delete = [i["name"] for i in item_to_delete]
    logger.debug("Items to delete: {name_to_delete}", name_to_delete=name_to_delete)
    frequency = sum([i["frequency"] for i in item_to_delete]) + 1

    item_to_add = None
    if resp["entity_name"]:
        logger.debug("Adding new item {name}", name=resp["entity_name"])
        new_id = uuid4().hex
        item_to_add = Item(
            id=new_id,
            name=resp["entity_name"],
            description=resp["entity_description"],
            frequency=frequency,
        )
    else:
        logger.warning("No item to add")

    return item_to_delete, item_to_add


async def recognize_entities(text: str, llm: ChatOpenAI, db):
    items = await _gross_recognize_entities(text, llm)
    for i in items:
        related = db.query(i)
        to_delete, to_add = await _refine_recognized_entity(text, i, related, llm)
        for d in to_delete:
            db.delete(d)

        if to_add:
            db.add(to_add)
