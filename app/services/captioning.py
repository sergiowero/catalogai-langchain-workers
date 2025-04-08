import httpx
from clients.gemini import client
from google.genai import types
from PIL import Image

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

    # Download and encode the image
    image = Image.open(httpx.get(image_url).content)

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        config=types.GenerateContentConfig(
            system_instruction=system_prompt_template,
        ),
        contents=['describe esta imagen', image],
    )

    return response.text
