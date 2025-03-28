import base64

import httpx
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

system_prompt_template = """
Eres un experto en bienes raíces y tu tarea es describir la imagen de una propiedad de manera que resalte las características más atractivas y relevantes para un comprador potencial. Analiza la imagen y proporciona una descripción concisa (máximo 50 palabras) que incluya:

- El estilo general o estado de la propiedad (por ejemplo, moderno, acogedor, necesita reformas).
- Características destacadas visibles (como cocina equipada, jardín, piscina, etc.).
- Detalles sobre el espacio y la distribución (como habitaciones amplias, mucha luz natural, vistas atractivas).
- Cualquier elemento único o detalle arquitectónico especial.

Enfócate en lo que haría que un comprador se interese en la propiedad. Evita información irrelevante y mantén el tono profesional pero atractivo.
"""


def get_image_caption(image_url):
    """
    Genera un caption para la imagen usando Gemini 2.0 Flash.
    Este es un placeholder: reemplázalo con la llamada real a la API de Gemini.
    """

    # Usamos ChatGoogleGenerativeAI para simular la generación del caption
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

    # Download and encode the image
    image_data = base64.b64encode(httpx.get(image_url).content).decode('utf-8')

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(system_prompt_template),
            HumanMessage(
                content=[
                    {'type': 'text', 'text': 'describe this image'},
                    {
                        'type': 'image_url',
                        'image_url': {'url': f'data:image/jpeg;base64,{image_data}'},
                    },
                ]
            ),
        ]
    )

    chain = prompt | llm
    caption = chain.invoke({'image_data': image_data})
    return caption  # Ejemplo: "Una sala luminosa con grandes ventanales."
