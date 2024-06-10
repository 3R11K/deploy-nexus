from flask import Flask
import os
import gdown

def create_app():
    # Caminho onde o arquivo será salvo
    output = './models/GoogleNews-vectors-negative300.bin'

    # Verifica se o arquivo já existe
    if not os.path.exists(output):
        # ID do arquivo no Google Drive
        file_id = '1y8nTSjAiaGf_KljXJUSgPuknMuf4Fglg'
        # URL de download direto
        url = f'https://drive.google.com/uc?id={file_id}'
        
        print("Baixando o arquivo...")
        
        # Baixa o arquivo
        gdown.download(url, output, quiet=False)
    else:
        print("O arquivo já existe, não é necessário baixar novamente.")

    app = Flask(__name__)

    from .routes.clean_data import clean_data_bp
    from .routes.predict import predict_bp
    from .routes.vetorizacao import vectorize_bp
    from .routes.process import process_bp

    app.register_blueprint(clean_data_bp, url_prefix='/clean_data')
    app.register_blueprint(predict_bp, url_prefix="/predict")
    app.register_blueprint(vectorize_bp, url_prefix='/vectorize')
    app.register_blueprint(process_bp, url_prefix='/process')

    return app
