from typing import List, Optional, Tuple
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.messages import AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

from xraygpt.db.base import Item

def _gross_recognize_entities(text: str, llm: ChatOpenAI) -> List[str]:
    # Define the prompt with a structured JSON schema
    response_schemas = [
            ResponseSchema(name="item", description="An array of entity names", type="[string]"),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    chat_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template("You are an agent to help me recognize entities in text, give me the entities based on following rules\n1. Entities are people's names\n2. Outputs should following the format: {format_instructions}"),
            HumanMessagePromptTemplate.from_template("{text}")
        ],
        input_variables=["text"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()},
    )

    chain = chat_template | llm | output_parser

    resp = chain.invoke({"text": text})
    print(resp)
    return resp["item"]


def _refine_recognized_entity(text: str, name: str, items: List[Item], llm) -> Tuple[List[str], Optional[Item]]:
    response_schemas = [
            ResponseSchema(name="to_delete", description="An array of entity ids to delete", type="[string]"),
            ResponseSchema(name="entity_name", description="Array of entity names of single entity", type="[string]"),
            ResponseSchema(name="entity_description", description="entity description", type="string"),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

    chat_template = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template("You are an assistant tasked with refining a specific entity from text. Given the recognized entity \"{name}\" and related database information, your tasks are:\n1. Identify if the entity \"{name}\" is incorrect, irrelevant, or outdated, and mark it for deletion if necessary.\n2. Update the entity by deleting and adding a new entry if the text provides more important or detailed information.\n3. Ensure the updated entity name remains accurate.\n4. Provide a simple and concise entity description with less than 100 words.\\nOnly process and output information for the entity \"{name}\".\nYour output must follow this format: {format_instructions}"),
            HumanMessagePromptTemplate.from_template("Existing entity: {reference}"),
            HumanMessagePromptTemplate.from_template("{text}")
        ],
        input_variables=["text", "name", "reference"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()},
    )

    chain = chat_template | llm | output_parser

    references = [(",".join(i["name"]), i["description"]) for i in items]
    reference_description = "\n".join([f"{n}: {d}" for n,d in references])
    resp = chain.invoke({"text": text, "name": name, "reference": reference_description})
    print(resp)
    return resp["to_delete"], Item(id="", name=resp["entity_name"], description=resp["entity_description"])

def recognize_entities(text: str, llm: ChatOpenAI, db):
    items = _gross_recognize_entities(text, llm)
    for i in items:
        related = db.query(i)
        to_delete, to_add = _refine_recognized_entity(text, i, related, llm)
        for d in to_delete:
            db.delete(Item(id=d, name=[], description=""))

        if to_add:
            db.add(to_add)
