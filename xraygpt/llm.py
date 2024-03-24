from os import environ

from langchain_openai import AzureChatOpenAI, ChatOpenAI
from loguru import logger


def get_llm() -> ChatOpenAI:
    common_openai_params = {
        "temperature": 0,
        "api_key": environ["OPENAI_API_KEY"],
        "api_version": environ.get("OPENAI_API_VERSION", "2020-05-03"),
    }
    model_id = "chatgpt"
    llm: ChatOpenAI
    if "AZURE_OPENAI_ENDPOINT" in environ:
        logger.info(f"Using AzureOpenAI {model_id}")
        llm = AzureChatOpenAI(
            azure_endpoint=environ["AZURE_OPENAI_ENDPOINT"],
            deployment_name=model_id,
            **common_openai_params,  # type: ignore[arg-type,call-arg]
        )
    else:
        logger.info(f"Using OpenAI {model_id}")
        llm = ChatOpenAI(
            model=model_id,
            **common_openai_params,  # type: ignore[arg-type]
        )
    return llm
