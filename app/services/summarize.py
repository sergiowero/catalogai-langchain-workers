from google.genai import types

from app.clients.gemini import client
from app.models.product import Product

# Definir el system prompt (instrucciones generales)
system_prompt = """
Eres un experto en bienes raíces y en RAG. Tu tarea es crear descripciones claras, concisas e informativas de propiedades para compradores potenciales. 
Debes resaltar características clave como ubicación, tamaño, amenidades (habitaciones, baños, cochera, etc.) y detalles visuales.
El tono debe ser profesional pero descriptivo, es importante que sea optimizado para busquedas RAG con embeddings.
La descripción no debe exceder las 500 palabras.
"""

# Definir el prompt específico (user prompt con datos del producto)
prompt_template = """
Crea una descripción optimizada para la siguiente propiedad usando estos datos:

- Nombre: {name}
- Descripción inicial: {description}
- Metadatos: {metadata}
- Precio: {price}
- Descripciones de imágenes: {image_captions}

Combina toda la información en un párrafo coherente y optimizado para RAG.
"""


def sumarize_product(product: Product, image_captions: list[str]):
    image_captions_text = ', '.join(image_captions)

    metadata_text = ', '.join(
        f'{key}: {value}' for key, value in product.metadata.items()
    )

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
        ),
        contents=prompt_template.format(
            name=product.name,
            description=product.description,
            metadata=metadata_text,
            price=product.price,
            image_captions=image_captions_text,
        ),
    )

    return response
