import src.pydantic_models as pydantic_models
import src.laureate_pydantic_models as laureateModels
import json
from src import validators
from flask import Response, request
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
import sqlite3
from src import api_request
from src import db

info = Info(title="API de registro de favoritos", version="1.0.0", description="API Registro de ganhadores nobel favoritos")
app = OpenAPI(
    __name__,
    info=info,
    servers=[]   
)
CORS(app)

db.init_db()

favorite_tag = Tag(name="Favoritos", description="Gerência as premiações favoritas")
external_tag = Tag(name="Api secundaria", description="Requisições para API secundária")


@app.get(
    "/favorites",
    tags=[favorite_tag],
    responses={
        200: pydantic_models.FavoriteItemResponse,
        404: pydantic_models.DefaultResponse,
        500: pydantic_models.DefaultResponse,
    }
)
def get_favorites(query: pydantic_models.FavoriteDetailsQuery):
    """Retorna a lista de favoritos"""
    try:
        favorites = db.get_all_favorites()
        if not favorites:
            return Response(
                json.dumps({"message": "Nenhum Favorito encontrado"}, ensure_ascii=False),
                status=404,
                mimetype="application/json"
            )
        if query.orderBy == pydantic_models.OrderByEnum.amount:
            favorites = sorted(favorites, key=lambda x: x.get("amount", 0), reverse=True)
        elif query.orderBy == pydantic_models.OrderByEnum.name:
            favorites = sorted(favorites, key=lambda x: x.get("laureateName", ""))
        return Response(
            json.dumps(favorites, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao buscar favoritos: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )
    
@app.post(
    "/favorite",
    tags=[favorite_tag],
    responses={
        201: pydantic_models.DefaultResponse,
        400: pydantic_models.DefaultResponse,
        409: pydantic_models.DefaultResponse,
        500: pydantic_models.DefaultResponse
    }
)
def create_favorite(body: pydantic_models.FavoriteInput):
    """Cria um favorito."""
    try:
        favorite = request.get_json()
        laureate = api_request.get_laureate_by_id(favorite["laureateId"])
        favorite["laureateName"] = laureate["fullName"]["en"]
        favorite["motivation"] = laureate["nobelPrizes"][0]["motivation"]["en"]
        favorite["motivation"] = laureate["nobelPrizes"][0]["motivation"]["en"]
        favorite["amount"] = laureate["nobelPrizes"][0]["prizeAmount"]
        valid, message = validators.valid_favorite(favorite)
        if not valid:
            return Response(
                json.dumps({"message": message}, ensure_ascii=False),
                status=400,
                mimetype="application/json"
            )
        
        db.create_favorite(favorite)
        return Response(
            json.dumps({"message": "Favorito criado!"}, ensure_ascii=False),
            status=201,
            mimetype="application/json"
        )
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            return Response(
                json.dumps(
                    {"message": "Este ganhador já está nos favoritos."},
                    ensure_ascii=False
                ),
                status=409,  
                mimetype="application/json"
            )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao criar favorito: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )    
@app.put(
    "/favorite",
    tags=[favorite_tag],
    responses={
        200: pydantic_models.DefaultResponse,
        400: pydantic_models.DefaultResponse,
        500: pydantic_models.DefaultResponse
    }
)    
def edit_favorite(body: pydantic_models.FavoriteEditInput):
    """Edita um favorito."""
    try:
        object = request.get_json()
        db.update_description(object["id"], object["description"])
        return Response(
            json.dumps({"message": "favorito editado!"}, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao editar favorito: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )
    
@app.delete(
    "/favorite",
    tags=[favorite_tag],
    responses={
        200: pydantic_models.DefaultResponse,
        500: pydantic_models.DefaultResponse
    }
)    
    
def delete_favorite(query: pydantic_models.FavoriteIdQuery):
    """Remove um favorito pelo ID."""
    try:
        db.delete_favorite(query.id)
        return Response(
            json.dumps({"message": "favorito removido com sucesso"}, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao remover favorito: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )
    

@app.get(
    "/favorite_details",
    tags=[external_tag],
    responses={
        200: laureateModels.LaureateIdListResponse,
        500: pydantic_models.DefaultResponse
    }
)    
    
def get_favorites_details():
    """Retorna os detalhes de todos os ganhadores favoritos."""
    try:
        ids = db.get_favorites_ids()
        response = api_request.get_favorites_details(ids)
        return Response(
            json.dumps(response, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao buscar detalhes: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )   
     
@app.get(
    "/exactSciencesNobel",
    tags=[external_tag],
    responses={
        200: pydantic_models.NobelResponse,
        500: pydantic_models.DefaultResponse
    }
)    
    
def get_nobels():
    """Retorna os nobels e seus ganhadores dos ultimos 10 anos para ciências exatas"""
    try:
        response = api_request.get_nobels()
        return Response(
            json.dumps(response, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao buscar nobels: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )    
    
@app.get(
    "/nobelByCategory",
    tags=[external_tag],
    responses={
        200: pydantic_models.DefaultResponse,
        500: pydantic_models.DefaultResponse
    }
)    
def get_nobels_by_category(query: pydantic_models.NobelQuery):

    """Retorna os nobels por categoria e ano"""
    try:
        response = api_request.get_nobels_by_category(query.category, query.ye)
        return Response(
            json.dumps(response, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao buscar nobels: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )    
    

@app.get(
    "/allLaureates",
    tags=[external_tag],
    responses={
        200: laureateModels.LaureateIdListResponse,
        500: pydantic_models.DefaultResponse
    }
)        
def get_all_Laureals():

    """Retorna os nobels por categoria e ano"""
    try:
        response = api_request.get_laureates()
        return Response(
            json.dumps(response, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )
    except Exception as e:
        return Response(
            json.dumps({"message": f"Erro ao remover favorito: {str(e)}"}, ensure_ascii=False),
            status=500,
            mimetype="application/json"
        )        


if __name__ == "__main__":
    app.run()    
