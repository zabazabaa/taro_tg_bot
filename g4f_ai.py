import g4f

from config import BASE_CONTEXT

import asyncio

g4f.debug.logging = False
g4f.check_version = False


def generate_resp(text: str):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[
            {"role": "system", "content": BASE_CONTEXT},
            {"role": "user", "content": text}
        ]
    )
    return response