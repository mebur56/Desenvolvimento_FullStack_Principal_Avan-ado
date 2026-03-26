import src.pydanticModels as pydanticModels
import src.laureatePydanticModel as laureateModels
import json
from src import validators
from flask import Response, request
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
import sqlite3
from src import apiRequest
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
        200: pydanticModels.FavoriteItemResponse,
        404: pydanticModels.DefaultResponse,
        500: pydanticModels.DefaultResponse,
    }
)
def get_favorites(query: pydanticModels.FavoriteDetailsQuery):
    """Retorna a lista de favoritos"""
    try:
        favorites = db.get_all_favorites()
        if not favorites:
            return Response(
                json.dumps({"message": "Nenhum Favorito encontrado"}, ensure_ascii=False),
                status=404,
                mimetype="application/json"
            )
        if query.orderBy == pydanticModels.OrderByEnum.amount:
            favorites = sorted(favorites, key=lambda x: x.get("amount", 0), reverse=True)
        elif query.orderBy == pydanticModels.OrderByEnum.name:
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
        201: pydanticModels.DefaultResponse,
        400: pydanticModels.DefaultResponse,
        409: pydanticModels.DefaultResponse,
        500: pydanticModels.DefaultResponse
    }
)
def create_favorite(body: pydanticModels.FavoriteInput):
    """Cria um favorito."""
    try:
        favorite = request.get_json()
        laureate = apiRequest.get_laureate_by_id(favorite["laureateId"])
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
        200: pydanticModels.DefaultResponse,
        400: pydanticModels.DefaultResponse,
        500: pydanticModels.DefaultResponse
    }
)    
def edit_favorite(body: pydanticModels.FavoriteEditInput):
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
        200: pydanticModels.DefaultResponse,
        500: pydanticModels.DefaultResponse
    }
)    
    
def delete_favorite(query: pydanticModels.FavoriteIdQuery):
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
        500: pydanticModels.DefaultResponse
    }
)    
    
def get_favorites_details():
    """Retorna os detalhes de todos os ganhadores favoritos."""
    try:
        ids = db.get_favorites_ids()
        response = apiRequest.get_favorites_details(ids)
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
@app.get(
    "/exactSciecensNobel",
    tags=[external_tag],
    responses={
        200: pydanticModels.DefaultResponse,
        500: pydanticModels.DefaultResponse
    }
)    
    
def get_nobels():
    """Retorna os nobels e seus ganhadores dos ultimos 10 anos"""
    try:
        response = apiRequest.get_nobels()
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
