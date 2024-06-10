from app import create_app
from dotenv import load_dotenv
import os
from flasgger import Swagger
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = create_app()
swagger = Swagger(app)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
