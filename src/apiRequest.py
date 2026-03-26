import os
import requests
from dotenv import load_dotenv
from flask import jsonify
#from src.params import NobelParams, LaureateParams

load_dotenv()


def get_nobels():
    try:
        response = requests.get(
                os.getenv("BASE_URL") + "/exactSciences"
            )
        data = response.json()
        return data
    except Exception as e:
        print('erro ' + str(e))

def get_nobels_by_category(category: str, year: int):
    try:
        response = requests.get(
                os.getenv("BASE_URL") + "/nobelByCategory?category={}&year={}".format(category, year)
            )
        data = response.json()
        return data
    except Exception as e:
        print('erro ' + str(e))
def get_laureates():
    try:
        response = requests.get(
                os.getenv("BASE_URL") + "/laureates"
            )
        data = response.json()
        return data
    except Exception as e:
        print('erro ' + str(e))


def get_favorites_details(ids : list[int]):
    try:
        data = []
        for id in ids:
            response = requests.get(
                os.getenv("BASE_URL") + "/laureatesById?id={}".format(id)
            )
            data.append(response.json())
        return data
    except Exception as e:
        print('erro ' + str(e))

def get_laureate_by_id(id : int):
    try:
        response = requests.get(
            os.getenv("BASE_URL") + "/laureatesById?id={}".format(id)
        )
        return response.json()
    except Exception as e:
        print('erro ' + str(e))
