# Familia Phi-3 de Microsoft

Los modelos Phi-3 son los Modelos de Lenguaje Pequeño (SLMs) más capaces y rentables disponibles, superando a modelos del mismo tamaño y del siguiente tamaño en una variedad de benchmarks de lenguaje, razonamiento, codificación y matemáticas. Esta versión amplía la selección de modelos de alta calidad para los clientes, ofreciendo más opciones prácticas para componer y construir aplicaciones de IA generativa.

La Familia Phi-3 incluye versiones mini, small, medium y vision, entrenadas con diferentes cantidades de parámetros para servir varios escenarios de aplicación. Cada modelo está ajustado por instrucciones y desarrollado de acuerdo con los estándares de IA Responsable, seguridad y protección de Microsoft para asegurar que esté listo para usar directamente. Phi-3-mini supera a modelos el doble de su tamaño, y Phi-3-small y Phi-3-medium superan a modelos mucho más grandes, incluyendo GPT-3.5T.

## Phi-3.5-vision
[Phi-3.5 Vision](https://ai.azure.com/explore/models/Phi-3.5-vision-instruct/version/1/registry/azureml) es un modelo multimodal abierto, ligero y de última generación construido sobre conjuntos de datos que incluyen datos sintéticos y sitios web públicos filtrados, con un enfoque en datos de muy alta calidad y densa capacidad de razonamiento tanto en texto como en visión. El modelo pertenece a la familia de modelos Phi-3, y la versión multimodal viene con una longitud de contexto de 128K (en tokens) que puede soportar. El modelo pasó por un riguroso proceso de mejora, incorporando tanto ajuste fino supervisado como optimización de preferencias directas para asegurar una adherencia precisa a las instrucciones y robustas medidas de seguridad.

Phi-3.5 Vision tiene 4.2B parámetros y contiene un codificador de imágenes, conector, proyector y el modelo de lenguaje Phi-3 Mini.

El modelo está destinado para un amplio uso comercial y de investigación en inglés. El modelo ofrece usos para sistemas y aplicaciones de IA de propósito general con capacidades de entrada visual y de texto que requieren:
1) entornos con restricciones de memoria/cómputo.
2) escenarios con limitaciones de latencia.
3) comprensión general de imágenes.
4) OCR.
5) comprensión de gráficos y tablas.
6) comparación de múltiples imágenes.
7) resumen de múltiples imágenes o clips de video.

El modelo Phi-3.5-vision está diseñado para acelerar la investigación en modelos de lenguaje y multimodales eficientes, para su uso como un bloque de construcción para características impulsadas por IA generativa.

![phi35_vision](../../../../translated_images/phi35visionbenchmark.2fe11de1d014201677fcb1c5c2cd04e6caa124c5468541637eb75b1897121918.es.png)

## Phi-3.5-MoE

[Phi-3.5 MoE](https://ai.azure.com/explore/models/Phi-3.5-MoE-instruct/version/1/registry/azureml) es un modelo abierto, ligero y de última generación construido sobre conjuntos de datos utilizados para Phi-3 - datos sintéticos y documentos públicos filtrados - con un enfoque en datos de muy alta calidad y densa capacidad de razonamiento. El modelo soporta multilingüismo y viene con una longitud de contexto de 128K (en tokens). El modelo pasó por un riguroso proceso de mejora, incorporando ajuste fino supervisado, optimización de políticas proximales y optimización de preferencias directas para asegurar una adherencia precisa a las instrucciones y robustas medidas de seguridad.

Phi-3 MoE tiene 16x3.8B parámetros con 6.6B parámetros activos cuando se usan 2 expertos. El modelo es un Transformer de solo decodificación con mezcla de expertos usando el tokenizador con un tamaño de vocabulario de 32,064.

El modelo está destinado para un amplio uso comercial y de investigación en inglés. El modelo ofrece usos para sistemas y aplicaciones de IA de propósito general que requieren:

1) entornos con restricciones de memoria/cómputo.
2) escenarios con limitaciones de latencia.
3) fuerte capacidad de razonamiento (especialmente matemáticas y lógica).

El modelo MoE está diseñado para acelerar la investigación en modelos de lenguaje y multimodales, para su uso como un bloque de construcción para características impulsadas por IA generativa y requiere recursos de cómputo adicionales.

![phi35moe_model](../../../../translated_images/phi35moebenchmark.2fe11de1d014201677fcb1c5c2cd04e6caa124c5468541637eb75b1897121918.es.png)

> [!NOTE]
>
> Los modelos Phi-3 no se desempeñan tan bien en benchmarks de conocimiento factual (como TriviaQA) ya que el tamaño más pequeño del modelo resulta en una menor capacidad para retener hechos.

## Phi silica

Estamos presentando Phi Silica, que está construido a partir de la serie de modelos Phi y está diseñado específicamente para las NPUs en las PCs Copilot+. Windows es la primera plataforma en tener un modelo de lenguaje pequeño (SLM) de última generación personalizado para la NPU y disponible de forma integrada. La API de Phi Silica junto con OCR, Studio Effects, Live Captions y las APIs de Recall User Activity estarán disponibles en la Biblioteca de Windows Copilot en junio. Más APIs como Vector Embedding, RAG API y Text Summarization estarán disponibles más adelante.

## **Encuentra todos los modelos Phi-3**

- [Azure AI](https://ai.azure.com/explore/models?selectedCollection=phi)
- [Hugging Face](https://huggingface.co/collections/microsoft/phi-3-6626e15e9585a200d2d761e3)

## Modelos ONNX

La principal diferencia entre los dos modelos ONNX, “cpu-int4-rtn-block-32” y “cpu-int4-rtn-block-32-acc-level-4”, es el nivel de precisión. El modelo con “acc-level-4” está diseñado para equilibrar latencia versus precisión, con una pequeña compensación en precisión para un mejor rendimiento, lo cual podría ser particularmente adecuado para dispositivos móviles.

## Ejemplo de Selección de Modelo

| | | | |
|-|-|-|-|
|Necesidad del Cliente|Tarea|Comienza con|Más Detalles|
|Necesita un modelo que simplemente resuma una conversación de mensajes|Resumen de Conversación|Modelo de texto Phi-3|El factor decisivo aquí es que el cliente tiene una tarea de lenguaje bien definida y directa|
|Una app gratuita de tutor de matemáticas para niños|Matemáticas y Razonamiento|Modelos de texto Phi-3|Debido a que la app es gratuita, los clientes quieren una solución que no les cueste de manera recurrente|
|Cámara de Patrulla Automática|Análisis de visión|Phi-Vision|Necesita una solución que pueda funcionar en el borde sin internet|
|Quiere construir un agente de reservas de viajes basado en IA|Necesita planificación compleja, llamadas a funciones y orquestación|Modelos GPT|Necesita la capacidad de planificar, llamar APIs para recopilar información y ejecutar|
|Quiere construir un copiloto para sus empleados|RAG, múltiples dominios, complejo y abierto|Modelos GPT|Escenario abierto, necesita un conocimiento más amplio del mundo, por lo tanto, un modelo más grande es más adecuado|

Aviso legal: La traducción fue realizada a partir del original por un modelo de IA y puede no ser perfecta. 
Por favor, revise el resultado y haga las correcciones necesarias.