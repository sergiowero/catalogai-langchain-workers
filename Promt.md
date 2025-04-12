

# Prompt Mejorado: Desarrollo de un Agente de IA para Tiendas Online de Bienes Raíces

## Objetivo Principal
Desarrollar un agente de inteligencia artificial basado en un modelo de lenguaje (LLM) para tiendas en línea especializadas en bienes raíces (casas). El propósito central del agente es **maximizar las ventas** para las tiendas y proporcionar una **experiencia de atención al cliente excepcional**. El agente debe recomendar productos (casas) personalizados y asistir a los usuarios en el proceso de búsqueda y compra, optimizando la conversión de leads en ventas.

### Enfoque del MVP
El primer MVP se centrará exclusivamente en **tiendas de bienes raíces**, donde personas o empresas registran casas para captar clientes. El agente será un chatbot que interactúe con los usuarios finales (potenciales compradores) y utilice una base de conocimientos proporcionada por las empresas inmobiliarias.

---

## Funcionalidades Clave del Agente
El agente debe cumplir con las siguientes tareas esenciales:

1. **Recomendación de Casas Personalizadas**
   - Basarse en las descripciones y preferencias que el usuario proporcione en el chat (prompts).
   - Considerar atributos específicos como:
     - **Ubicación**: ciudad, colonia, cercanía a puntos de interés (escuelas, parques, centros comerciales).
     - **Características Físicas**: número de habitaciones, baños, estacionamientos, pisos, tamaño de construcción, calidad de acabados, jardín, alberca, etc.
     - **Servicios y Plusvalías**: seguridad, acceso a transporte, valor de reventa.
   - Priorizar recomendaciones que maximicen el interés del usuario y la probabilidad de venta.

2. **Agendamiento de Llamadas**
   - Facilitar la conexión entre usuarios y vendedores humanos programando citas o llamadas directamente desde el chat.

3. **Acciones Personalizadas**
   - Lost usuarios Empresariales podran elegir acciones dentro de su pagina para que el agente pueda ejecutarlas, talez como agregar a favoritos o ir a la pagina de la casa.

4. **Análisis de Estadísticas**
   - Recopilar y almacenar datos sobre las preferencias más buscadas por los usuarios (ej. casas con alberca, 3 habitaciones, etc.) para proporcionar insights a las empresas inmobiliarias.

5. **Optimización para Ventas**
   - Proporcionar a las páginas inmobiliarias información clave para captar clientes, destacando ventajas competitivas (ej. precios competitivos, ubicaciones exclusivas).

---

## Restricciones del Sistema
- **Usuarios Empresariales**: Las empresas con páginas web de bienes raíces serán los clientes principales. Estas empresas:
  - Registrarán, actualizarán y eliminarán casas en la base de conocimientos del agente.
  - Proporcionarán la información inicial y actualizada de las propiedades.
  - Podran usar una API REST o un formulario web
- **Usuarios Finales**: Los compradores potenciales interactúan con el chatbot a través de las páginas web de las empresas, especificando sus preferencias en el chat. 
  - Estos usaurios son efimeros, osea no necesitan registrarse en ningun lado para poder hacer uso del sistema, el agente de ia debera conversar con ellos para obetner la informaicon y hacer las busquedas correspondientes.
- **Base de Conocimientos**: El agente solo recomendará casas basándose en los datos proporcionados por las empresas, sin acceso a información externa no autorizada.

---

## Arquitectura Propuesta: Frontend y Backend

### División General
- **Frontend**: Interfaz de usuario (chatbot) para los compradores y panel de administración para las empresas inmobiliarias.
- **Backend**: Lógica del agente, almacenamiento de datos, procesamiento de prompts y conexión con la base de conocimientos, REST API, generacion de apiKeys para clientes.

#### Componentes del Backend
Para cumplir con las funcionalidades descritas, el backend debe incluir los siguientes elementos:

1. **Base de Datos**
   - Almacenar la información de las casas (atributos como ubicación, tamaño, precio, etc.).
   - Guardar los favoritos de los usuarios y las estadísticas de búsqueda.
   - Tecnologías sugeridas: PostgreSQL con extensiones para geolocaclizacion y vectores

2. **API del LLM**
   - Integración con un modelo de lenguaje (ej. Grok, GPT, o similar) para procesar los prompts de los usuarios y generar recomendaciones.
   - se recomienda n8n si es posible
   - Endpoints para enviar prompts y recibir respuestas estructuradas.

3. **Motor de Recomendaciones**
   - Algoritmo que filtre y ordene las casas según las preferencias del usuario , como RAG.
   - Ejemplo: Ponderar atributos como precio, ubicación y número de habitaciones.

4. **Sistema de Agendamiento**
   - Usar n8n para agendar 

5. **Gestor de Estadísticas**
   - por el momento solo almacenar la informacion esructurada

6. **Autenticación y Seguridad**
   - Supabase

7. **Interfaz con el Frontend**
   - API REST o WebSocket para comunicación en tiempo real entre el chatbot y el backend.

---

## Recolección de Datos del Usuario para Recomendaciones

### Estrategia para el Feature de Recomendaciones vía Chatbot
El agente recopilará datos de los usuarios a través de la interacción natural en el chat. Aquí hay un enfoque detallado:

1. **Interacción Inicial**
   - El chatbot inicia con una pregunta abierta:  
     _"Hola, ¿qué tipo de casa estás buscando? Puedes decirme cosas como ubicación, número de habitaciones, o si prefieres algo con alberca o jardín."_
   - Esto permite al usuario compartir preferencias sin un formulario rígido.

2. **Procesamiento de Prompts**
   - El LLM analiza el texto del usuario para identificar atributos clave (ej. "quiero una casa en Polanco con 3 recámaras y estacionamiento" → {ubicación: Polanco, habitaciones: 3, estacionamiento: sí}).
   - Si falta información crítica (ej. presupuesto), el chatbot pregunta:  
     _"¿Tienes un presupuesto en mente para esta casa?"_

3. **Confirmación y Refinamiento**
   - El agente resume las preferencias detectadas:  
     _"Entendí que buscas una casa en Polanco con 3 recámaras y estacionamiento. ¿Hay algo más que quieras agregar, como tamaño o servicios?"_
   - Esto asegura que las recomendaciones sean precisas.

4. **Integración con la Base de Conocimientos**
   - El backend usa los atributos extraídos para consultar la base de datos y devolver las casas más relevantes.
   - El LLM presenta las opciones al usuario en un formato amigable:  
     _"Te recomiendo esta casa en Polanco: 3 recámaras, 2 baños, 150 m², con estacionamiento y jardín. ¿Te interesa saber más o agendar una llamada?"_

5. **Métodos de Captura de Datos**
   - **Chat en Tiempo Real**: WebSocket para una experiencia fluida.
   - **Historial del Usuario**: Guardar las interacciones en la base de datos (con consentimiento) para personalizar futuras recomendaciones.
   - **Formularios Opcionales**: Ofrecer un formulario breve en el frontend para usuarios que prefieran ingresar datos manualmente.

---

## Preguntas para Profundizar (Opcional)
- ¿Qué tan detallada quieres que sea la base de conocimientos inicial de las casas?
- ¿Prefieres un enfoque basado en reglas o uno con aprendizaje automático para las recomendaciones?
- ¿Qué nivel de integración esperas con sistemas externos (ej. calendarios, CRM de las empresas)?
- ¿Hay un límite de usuarios o casas que el MVP debe soportar?

---

## Notas Técnicas
Dado tu perfil técnico, asumo que estás familiarizado con tecnologías como Python (para el backend), frameworks como Flask/Django/FastAPI, y bases de datos relacionales o no relacionales. Si necesitas un desglose más granular (ej. esquema de la base de datos, código inicial), puedo proporcionarlo en una iteración posterior.

---

Este prompt mejorado es más claro, estructurado y específico, lo que permite a cualquier LLM generar respuestas más útiles y accionables para un escenario de investigación y desarrollo. ¿Cómo te gustaría proceder?