import os
import re
from typing import Dict, Generator, List

from azure.ai.textanalytics import (
    DocumentError,
    RecognizeEntitiesResult,
    TextAnalyticsClient,
)
from azure.core.credentials import AzureKeyCredential
from loguru import logger

from xraygpt.splitter import sillySplit


def _recognize_entities(
    text_analytics_client: TextAnalyticsClient, reviews: List[str]
) -> Generator[RecognizeEntitiesResult | DocumentError, None, None]:
    for r in sillySplit(reviews, 5000):
        yield text_analytics_client.recognize_entities([r])[0]


def recognize_entities(reviews: List[str]) -> set[str]:
    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    persons = set()

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    persons = set()

    for review in _recognize_entities(text_analytics_client, reviews):
        if review.is_error:
            logger.error("Error: {}", review["error"])
            continue

        for entity in review.entities:
            if entity.category == "Person" and entity.text not in persons:
                logger.debug("Person: {}", entity.text)
                persons.add(entity.text)

    return persons


if __name__ == "__main__":
    reviews = [
        """I work for Foo Company, and we hired Contoso for our annual founding ceremony. The food
        was amazing and we all can't say enough good words about the quality and the level of service.""",
        """We at the Foo Company re-hired Contoso after all of our past successes with the company.
        Though the food was still great, I feel there has been a quality drop since their last time
        catering for us. Is anyone else running into the same problem?""",
        """Bar Company is over the moon about the service we received from Contoso, the best sliders ever!!!!""",
    ]
    recognize_entities(reviews)
