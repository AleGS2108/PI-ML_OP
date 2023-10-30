## Librerias importadas
import pandas as pd
import sklearn
import gzip
from fastapi import FastAPI
from sklearn.metrics.pairwise import cosine_similarity

## Instancia
app = FastAPI()

## Query 1
@app.get('/Developer')
def Developer(developer:str):
    df_steam=pd.read_csv('df_steam.csv')
    df_developer = df_steam[df_steam['developer'] == developer]
    if df_developer.empty:
        return {"error": "El developer no se encontró en los datos"}
    juegos_por_anio = df_developer.groupby('release_date')['item_name'].count().reset_index()
    juegos_por_anio.columns = ['release_date', 'cantidad_juegos']
    juegos_precio_cero_por_anio = df_developer[df_developer['price'] == 0.0].groupby('release_date')['item_name'].count().reset_index()
    juegos_precio_cero_por_anio.columns = ['release_date', 'cantidad_juegos_precio_cero']
    juegos_por_anio = juegos_por_anio.merge(juegos_precio_cero_por_anio, on='release_date', how='left')
    juegos_por_anio['porcentaje_juegos_precio_cero'] = (juegos_por_anio['cantidad_juegos_precio_cero'] / juegos_por_anio['cantidad_juegos']) * 100
    juegos_por_anio.fillna(0.0, inplace=True)
    respuesta = {}
    for index, row in juegos_por_anio.iterrows():
        respuesta[int(row['release_date'])] = {
            'cantidad_juegos': row['cantidad_juegos'],
            'porcentaje_juegos_free': row['porcentaje_juegos_precio_cero']
        }
    return respuesta

## Query 2
@app.get('/User_data')
def obtener_informacion_juegos(user_id:str):
    df_sub2=pd.read_csv('df_sub2.csv')
    df_usuario = df_sub2[df_sub2['user_id'] == user_id]
    if df_usuario.empty:
        return {"error": "El usuario no se encontró en los datos"}
    precio_total = df_usuario['price'].sum()
    porcentaje_recomendados = (df_usuario['recommend'].sum() / len(df_usuario)) * 100
    cantidad_juegos = len(df_usuario)
    informacion = {
        'user_id': user_id,
        'precio_total': precio_total,
        'porcentaje_recomendados': porcentaje_recomendados,
        'cantidad_juegos': cantidad_juegos
    }
    return informacion

## Query 3
@app.get('/User_for_genre')
def obtener_usuario_mas_horas_jugadas_por_genero(genero:str):
    with gzip.open('df_sub1.csv.gz', 'rb') as f:
        df_sub1 = pd.read_csv(f)
    df_genero = df_sub1[df_sub1['genres'].apply(lambda x: genero in x)]
    if df_genero.empty:
        return {"error": "El genero no se encontró en los datos"}
    usuario_mas_horas = df_genero.groupby('user_id')['playtime_forever'].sum().idxmax()
    df_usuario_mas_horas = df_genero[df_genero['user_id'] == usuario_mas_horas]
    acumulacion_horas_por_anio = df_usuario_mas_horas.groupby('release_date')['playtime_forever'].sum().reset_index()
    acumulacion_horas_por_anio.columns = ['Año', 'Horas']
    lista_acumulacion_horas = acumulacion_horas_por_anio.to_dict('records')
    respuesta = {
        "Usuario con más horas jugadas para " + genero: usuario_mas_horas,
        "Horas jugadas": lista_acumulacion_horas
    }
    return respuesta

## Query 4
@app.get('/Best_developer_year')
def top_desarrolladores_recomendados_por_anio(anio:int):
    df_sub2=pd.read_csv('df_sub2.csv')
    df_filtrado = df_sub2[(df_sub2['release_date'] == anio) & (df_sub2['recommend'] == True) & (df_sub2['sentiment_analysis'] == 2)]
    if df_filtrado.empty:
        return {"error": "El developer no se encontró en los datos"}
    conteo_juegos_por_desarrollador = df_filtrado['developer'].value_counts().reset_index()
    conteo_juegos_por_desarrollador.columns = ['Desarrollador', 'Cantidad']
    top_desarrolladores = conteo_juegos_por_desarrollador.head(3)
    resultado = []
    for index, row in top_desarrolladores.iterrows():
        puesto = "Puesto " + str(index + 1)
        desarrollador = row['Desarrollador']
        resultado.append({puesto: desarrollador})
    return resultado

## Query 5
@app.get('/Developer_reviews_analysis')
def sumar_sentimientos_por_desarrollador(developer:str):
    df_sub2=pd.read_csv('df_sub2.csv')
    df_filtrado = df_sub2[df_sub2['developer'] == developer]
    if df_filtrado.empty:
        return {"error": "El developer no se encontró en los datos"}
    positivo = df_filtrado[df_filtrado['sentiment_analysis'] == 2].shape[0]
    negativo = df_filtrado[df_filtrado['sentiment_analysis'] == 0].shape[0]
    resultado = {
        developer: {
            'Negativo': negativo,
            'Positivo': positivo
        }
    }
    return resultado

## Modelo de recomendacion id_juego
@app.get('/Id_game_recommendation')
def get_recommendations(input_product_id):
    data_encoded=pd.read_csv('ModeloML1.csv')
    juegos=[]
    input_product = data_encoded[data_encoded['item_id'] == int(input_product_id)]
    if input_product.empty:
        return {"error": "El ID del producto de entrada no existe en la base de datos."}
    input_product_name = input_product['item_name'].values[0]
    similarity_scores = cosine_similarity(input_product.iloc[:, 2:], data_encoded.iloc[:, 2:])
    similarity_series = pd.Series(similarity_scores[0], index=data_encoded['item_id'])
    sorted_similarities = similarity_series.sort_values(ascending=False)
    num_recommendations = 5
    top_recommended_games = sorted_similarities[1:num_recommendations + 1]
    recommended_game_names = data_encoded[data_encoded['item_id'].isin(top_recommended_games.index)]['item_name']
    juegos.append(input_product_name)
    recommended_games_list = []
    for game_name in recommended_game_names:
        recommended_games_list.append(game_name)
        juegos.append(game_name)
    return {"input_product_name": input_product_name, "recommended_games": recommended_games_list}