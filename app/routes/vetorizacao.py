from flask import Flask, Blueprint, jsonify, request
import numpy as np
from services.helper_vetor import vectorize_text

vectorize_bp = Blueprint('vectorize_bp', __name__)


@vectorize_bp.route('/vectorize', methods=['POST'])
def vectorize_text_route():
    """
    Esta rota recebe um request POST com um payload JSON contendo o texto a ser vetorizado.
    Retorna um payload JSON com o vetor.

    Exemplo de request:
    {
        "text": "Uber é um serviço incrível!"
    }

    Resposta:
    {
        "vector": [0.23, 0.55, -0.33, ...]
    }
    """
    try:
        text = request.json['text']
        vector = vectorize_text(text)  # Assume que esta função retorna um numpy array.
        return jsonify({'vector': vector.tolist()})  # Converta o numpy array para lista, se necessário.
    except Exception as e:
        return jsonify({'message': str(e)}), 400

