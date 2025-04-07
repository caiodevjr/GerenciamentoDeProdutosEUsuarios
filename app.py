from flask import Flask
from livereload import Server
from routes.route_produto import produto_bp
from routes.route_usuario import usuario_bp
from controllers.controller_produto import produto_controller

app = Flask(__name__)
app.register_blueprint(produto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(produto_controller)
app.secret_key = 'chave_secreta'

if __name__ == '__main__':
    app.run(debug=True)
    server = Server(app.wsgi_app)
    server.serve(debug=True, port=5000)
