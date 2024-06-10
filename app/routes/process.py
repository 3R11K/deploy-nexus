from app.routes.clean_data import clean_tweet
from app.routes.vetorizacao import vectorize_text_route
from app.routes.predict import prediction_route
from flask import Flask, Blueprint, jsonify, request
import requests

process_bp = Blueprint('process_bp', __name__)

@process_bp.route('/tweet', methods=['POST'])
def process_tweet():
    """
    Esta rota recebe um request POST com um payload JSON contendo o texto a ser processado.
    Retorna um payload JSON com a previsão.
    
    Exemplo de request:
    {
        "data": "Uber é um serviço incrível!"
    }
    
    Resposta:
    {
        "prediction": 1
    }
    """
    
    #faça todas as rotas como no exemplo acima através de requests.post
    data = request.json["data"]
    
    try:
        # Enviar solicitação para limpeza de dados
        request_clean = requests.post("http://localhost:5000/clean_data/tweet", json={"data": data})
        request_clean.raise_for_status()
        response_clean = request_clean.json()
        cleaned_data = response_clean["text"]

        # Enviar solicitação para vetorização
        request_vetor = requests.post("http://localhost:5000/vectorize/vectorize", json={"text": cleaned_data})
        request_vetor.raise_for_status()
        response_vetor = request_vetor.json()
        vetor = response_vetor["vector"]

        # Enviar solicitação para previsão
        request_predict = requests.post("http://localhost:5000/predict/predict", json={"vector": vetor})
        request_predict.raise_for_status()
        response_predict = request_predict.json()

        return jsonify({"prediction": response_predict[0]})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
        
 