from flask import Flask
from routes.rotas_customizadas import get_best_route

app = Flask(__name__)

app.register_blueprint(get_best_route, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True)
