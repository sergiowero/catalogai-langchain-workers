from langchain.prompts import ChatPromptTemplate
from langchain_core.messages.ai import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from models.product import Product

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

chat_prompt = ChatPromptTemplate.from_messages(
    [('system', system_prompt), ('user', prompt_template)]
)

llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash'
)  # Ajusta el modelo según tu necesidad
chain = chat_prompt | llm


def optimize_product_description(
    product: Product, image_captions: list[str]
) -> AIMessage:
    """
    Genera una descripción optimizada combinando los datos del producto y los captions.

    Args:
        product (Product): isntancia de producto
        image_captions (list): Lista de descripciones de imágenes.
    Returns:
        str: Descripción optimizada de la propiedad.
    """

    image_captions_text = ', '.join(image_captions)
    metadata_text = ', '.join(
        f'{key}: {value}' for key, value in product.metadata.items()
    )

    # Genera la descripción optimizada
    optimized_description = chain.invoke(
        input={
            'name': product.name,
            'description': product.description,
            'metadata': metadata_text,
            'price': product.price,
            'image_captions': image_captions_text,
        }
    )
    return optimized_description
