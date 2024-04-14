from django.conf import settings
from openai import OpenAI


def is_harmful(input_text: str) -> bool:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.moderations.create(input=input_text)
    categories_object = response.results[0].categories

    if any(getattr(categories_object, attr) for attr in categories_object.__dict__):
        return True
    else:
        return False
