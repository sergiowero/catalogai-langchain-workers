import base64

import httpx
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_prompt = """
Tu tarea es describir la foto de una seccion de una casa de manera descriptiva, Analiza la imagen y proporciona una descripción concisa (máximo 100 palabras):
Evita información irrelevante. Tu respuesta debe ser solo la descripción, sin ningún otro texto adicional.
"""

messages = [
    ('system', system_prompt),
    (
        'human',
        [
            {'type': 'text', 'text': 'describe esta imagen'},
            {
                'type': 'image_url',
                'image_url': {'url': 'data:image/jpeg;base64,{image_data}'},
            },
        ],
    ),
]

prompt = ChatPromptTemplate.from_messages(messages)


def get_image_data(image_url: str):
    return base64.b64encode(httpx.get(image_url).content).decode('utf-8')


def get_image_caption(image_data: bytes):
    """
    Genera un caption para la imagen usando Gemini 2.0 Flash.
    Este es un placeholder: reemplázalo con la llamada real a la API de Gemini.
    """

    llm = init_chat_model(
        model='gemini-2.0-flash-lite', model_provider='google_genai', temperature=1
    )

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({'image_data': image_data})

    return response
