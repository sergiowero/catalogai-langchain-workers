from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.models.product import Product

# Definir el system prompt (instrucciones generales)
system_prompt = """
Eres un experto en bienes raíces y en RAG. Tu tarea es crear descripciones claras, concisas e informativas de propiedades para compradores potenciales. 
Debes resaltar características clave como ubicación, tamaño, amenidades (habitaciones, baños, cochera, etc.) y detalles visuales.
El tono debe ser profesional pero descriptivo, es importante que sea optimizado para busquedas RAG con embeddings.
La descripción no debe exceder las 500 palabras. solo debes devolver la descripción, sin ningún otro texto adicional.
No incluyas etiquetas HTML, solo texto plano.
No incluyas información adicional, solo la descripción de la propiedad.
No incluyas información de contacto, precios o enlaces a sitios web.
"""

# Definir el prompt específico (user prompt con datos del producto)
human_prompt = """
Esta es la informacion de la propiedad:

- Nombre: {name}
- Descripción inicial: {description}
- Metadatos: {metadata}
- Precio: {price}
"""

messages = [
    ('system', system_prompt),
    ('human', human_prompt),
]

prompt = ChatPromptTemplate.from_messages(messages)


def sumarize_product(product: Product):
    metadata_text = ', '.join(
        f'{key}: {value}' for key, value in product.metadata.items()
    )

    llm = init_chat_model(
        model='gemini-2.0-flash', model_provider='google_genai', temperature=1
    )

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({**product.model_dump(), 'metadata': metadata_text})

    return response
