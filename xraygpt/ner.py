import os
from typing import Dict, List

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from xraygpt.splitter import sillySplit


def recognize_entities(reviews: List[str]) -> None:
    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    reviews = sillySplit(reviews, 5000)
    result_raw = [text_analytics_client.recognize_entities([r])[0] for r in reviews]
    result = [review for review in result_raw if not review.is_error]
    result_error = [review for review in result_raw if review.is_error]
    for error in result_error:
        print("Error: ", error["error"])
    related_to_reviews: Dict[str, List[str]] = {}

    for idx, review in enumerate(result):
        for entity in review.entities:
            print(f"Entity '{entity.text}' has category '{entity.category}'")
            related_to_reviews.setdefault(entity.text, [])
            related_to_reviews[entity.text].append(reviews[idx])


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
