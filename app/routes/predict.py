from flask import Blueprint, jsonify, request
from services.helper_predict import predict
predict_bp = Blueprint('predict_bp', __name__)
@predict_bp.route('/predict', methods=['POST'])
def prediction_route():
    """
    Rota de previsão que recebe dados em formato JSON e retorna as previsões.
    Espera um JSON no formato:
    {
        "data": [...]
    }
    Returns:
        JSON: Um JSON contendo as previsões ou uma mensagem de erro em caso de falha.
    """
    try:
        data = request.json['data']
        predictions = predict(data)
        predictions_list = predictions.tolist()
        return jsonify({'predictions': predictions_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 400