from flask import Blueprint, request, jsonify

produto_controller = Blueprint('produto_controller', __name__)

def validar_produto(data):
    """Valida os dados do produto e retorna uma lista de erros."""
    erros = []
    nome = data.get('nome', '').strip()
    preco = data.get('preco')
    estoque = data.get('estoque')

    if len(nome) < 3:
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

    return erros, {'nome': nome, 'preco': preco, 'estoque': estoque}

@produto_controller.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json() or {}
    erros, produto = validar_produto(data)

    if erros:
        return jsonify({'erros': erros}), 400

    return jsonify({'mensagem': 'Produto criado com sucesso!', 'produto': produto}), 201
