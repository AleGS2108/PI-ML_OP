# Proyecto Individual N°1: ML-OPS

Este proyecto consiste en una base de datos ficticia de juegos de la plataforma Steam y un sistema de recomendación basado en la similitud del coseno.

Los datasets empleados pueden encontrarse en el siguiente link ["Datasets originales"](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj).

Información:

- australian_user_reviews
- australian_users_items
- output_steam_games

## Data Engineering

### ETL (Extract, Transform, Load)

En la fase de Data Engineering, se realizó el proceso de ETL para garantizar la calidad y disponibilidad de los datos. Los pasos incluyeron:

1. **Extracción**: Los datos se extrajeron de las fuentes suministradas.

2. **Transformación**: Se aplicaron transformaciones para limpiar y estructurar los datos, lo que incluyó la normalización de nombres, la gestión de datos faltantes y la unificación de formatos.

3. **Carga**: Los datos transformados se cargaron en una base de datos limpia y normalizada para su posterior análisis y uso.

## Data Science

### Modelo de Recomendación

En la fase de Data Science, se desarrolló un modelo de recomendación basado en la similitud del coseno y el identificador único de los juegos (item_id). El proceso involucró:

1. **Preprocesamiento de Datos**: Se prepararon los datos para el modelo, incluyendo la creación de una matriz de similitud del coseno.

2. **Modelo de Recomendación**: Se implementó un sistema de recomendación que utiliza la similitud del coseno para identificar juegos similares a un juego dado.

3. **Evaluación del Modelo**: Se evaluó el rendimiento del modelo en función de un heatmap basado en el juego analizado y la lista de juegos recomendados brindado por el modelo.

## Diagrama de flujo



## API con FastAPI

Para acceder a la funcionalidad de este proyecto, se ha implementado una API utilizando [FastAPI](https://fastapi.tiangolo.com/). La API permite realizar las consultas solicitadas.

### Endpoints de la API

+ def **developer**: Devuelve la cantidad de juegos lanzados y el porcentaje de juegos "Free to Play" por año según la empresa desarrolladora.
+ def **userdata**: Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y la cantidad de juegos que posee en su biblioteca de Steam.
+ def **UserForGenre**: Devuelve el usuario que acumula mayor cantidad de horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
+ def **best_developer_year**: Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
+ def **developer_reviews_analysis**: Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador y una lista con la cantidad total de registros de reseñas
   de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
+ def **recomendacion_juego(**: Se ingresa el id de producto, devuelve una lista con 5 juegos recomendados similares al ingresado.

## Despliegue en Render

Este proyecto se encuentra desplegado y accesible en [Render](https://render.com/). Puedes acceder a la API en la siguiente URL: 
[deployment](https://deploy-mlop.onrender.com/docs)

## Instrucciones de Uso

Para utilizar este proyecto, sigue estos pasos:

1. **Requisitos Previos**: Asegúrate de tener instaladas las bibliotecas y dependencias necesarias proporcionadas en el archivo "requirements.txt".

2. **Configuración de la Base de Datos**: Configurar la conexión a la base de datos.

3. **Acceso a la API**: Utiliza la API para obtener las consultas deseadas.

## Contacto

Para cualquier pregunta o comentario, no dudes en ponerte en contacto: [correo](mailto:tu_correo@ejemplo.com) 
o por [linkedin](https://www.linkedin.com/in/m-alejandro-garcia-soto-a35680212/).

¡Muchas gracias por la atención!

