from flask import Flask, Blueprint, jsonify, request, send_file
from services.helper_clean_data import carrega_dados, pipeline
import io 
import pandas as pd
import spacy

clean_data_bp = Blueprint('clean_data', __name__)

# Define uma rota que retorna dados tratados após receber um arquivo '.csv'
@clean_data_bp.route("/csv", methods=['POST'])
def clean_csv():
    """
    Limpa os dados de um arquivo CSV enviado por meio de uma solicitação HTTP.
    
    Esta função espera receber um arquivo CSV por meio de uma solicitação HTTP.
    Ele lê o arquivo CSV, executa uma limpeza nos dados utilizando o spaCy para processamento de linguagem natural,
    e salva os dados limpos em um novo arquivo CSV. O arquivo limpo é então enviado de volta como uma resposta à solicitação.

    Retorna:
        Um arquivo CSV contendo os dados limpos.
        
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        Exception: Se ocorrer algum erro não esperado durante o processamento.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        file_stream = io.BytesIO(file.read())
        file_stream.seek(0)
        
        data = pd.read_csv(file_stream)
        nlp = spacy.load("en_core_web_sm")
        cleaned_data = []

        # Corrigido para iterar sobre as linhas do DataFrame
        for row in data.iterrows():
            cleaned_text = pipeline(nlp, row)  
            cleaned_data.append(cleaned_text)
        
        df = pd.DataFrame(cleaned_data, columns=['cleaned_text'])

        # Salva os dados limpos em um arquivo CSV
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name='cleaned-data.csv')
    
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Define uma rota que retorna dados tratados após receber um tweet 
@clean_data_bp.route("/tweet", methods=['POST'])
def clean_tweet():
    """
    Função para limpar tweets usando um pipeline NLP.

    Esta função recebe uma solicitação HTTP contendo um tweet em formato JSON,
    processa o tweet usando um pipeline de processamento de linguagem natural (NLP)
    e retorna o tweet limpo.

    Retornos:
        JSON: Um dicionário JSON contendo o tweet limpo.
        Em caso de sucesso, o dicionário conterá a chave 'prediction' com o tweet limpo.
        Em caso de erro, o dicionário conterá a chave 'message' com a descrição do erro e um status HTTP 400.

    Exceções:
        Qualquer exceção gerada durante o processamento será capturada e uma resposta JSON
        com o erro será retornada com status HTTP 400.
    """
    try:
        tweet = request.json['data']
        clean_tweet = pipeline(tweet)
        return jsonify({"text":clean_tweet})
    except Exception as e:
        return jsonify({'message': str(e)}), 400
