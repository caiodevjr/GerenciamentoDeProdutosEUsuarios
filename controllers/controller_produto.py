from flask import Blueprint, request, jsonify

produto_controller = Blueprint('produto_controller', __name__)

@produto_controller.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()

    nome = data.get('nome')
    preco = data.get('preco')
    estoque = data.get('estoque')

    erros = []

    if not nome or len(nome) < 3:
        erros.append("O nome do produto deve ter no mínimo 3 caracteres.")
    
    try:
        preco = float(preco)
        if preco <= 0:
            erros.append("O preço deve ser um valor positivo.")
    except (ValueError, TypeError):
        erros.append("O preço deve ser um número válido.")
    
    try:
        estoque = int(estoque)
        if estoque < 0:
            erros.append("O estoque deve ser um número inteiro maior ou igual a zero.")
    except (ValueError, TypeError):
        erros.append("O estoque deve ser um número inteiro.")

    if erros:
        return jsonify({'erros': erros}), 400

    return jsonify({'mensagem': 'Produto criado com sucesso!', 'produto': {
        'nome': nome,
        'preco': preco,
        'estoque': estoque
    }}), 201