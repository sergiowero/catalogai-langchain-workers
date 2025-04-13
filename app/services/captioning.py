import base64

import httpx
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_prompt = """
Eres un experto en bienes raíces y tu tarea es describir la imagen de una propiedad de manera que resalte las características más atractivas y relevantes para un comprador potencial. Analiza la imagen y proporciona una descripción concisa (máximo 50 palabras) que incluya:

- El estilo general o estado de la propiedad (por ejemplo, moderno, acogedor, necesita reformas).
- Características destacadas visibles (como cocina equipada, jardín, piscina, etc.).
- Detalles sobre el espacio y la distribución (como habitaciones amplias, mucha luz natural, vistas atractivas).
- Cualquier elemento único o detalle arquitectónico especial.

Evita información irrelevante y mantén el tono profesional y muy descriptivo. Tu respuesta debe ser solo la descripción, sin ningún otro texto adicional.
"""

system_prompt_2 = """
Tu tarea es describir la foto de una seccion de una casa de manera descriptiva, Analiza la imagen y proporciona una descripción concisa (máximo 100 palabras).:
Evita información irrelevante. Tu respuesta debe ser solo la descripción, sin ningún otro texto adicional.
"""


def get_image_caption(image_url):
    """
    Genera un caption para la imagen usando Gemini 2.0 Flash.
    Este es un placeholder: reemplázalo con la llamada real a la API de Gemini.
    """

    llm = init_chat_model(
        model='gemini-2.0-flash-lite', model_provider='google_genai', temperature=1
    )

    # Download the image data
    image_data = base64.b64encode(httpx.get(image_url).content).decode('utf-8')

    messages = [
        SystemMessage(system_prompt_2),
        HumanMessage(
            content=[
                {'type': 'text', 'text': 'describe esta imagen'},
                {
                    'type': 'image_url',
                    'image_url': {'url': f'data:image/jpeg;base64,{image_data}'},
                },
            ],
        ),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke(input={})

    return response
