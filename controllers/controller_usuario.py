from flask import Blueprint, request, jsonify
import mysql.connector
from mysql.connector import Error
import re

usuario_controller = Blueprint('usuario_controller', __name__)

def conectar():
    """Estabelece a conexão com o banco de dados."""
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='crud_produtos',
            user='root',
            password=''
        )
        return conexao
    except Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None

def validar_email(email):
    """Verifica se o email é válido."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@usuario_controller.route('/usuarios', methods=['POST'])
def criar_usuario():
    """Cria um novo usuário no banco de dados."""
    data = request.get_json()

    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip()
    senha = data.get('senha', '').strip()

    if len(nome) < 3:
        return jsonify({'erro': 'O nome deve ter pelo menos 3 caracteres'}), 400
    if not validar_email(email):
        return jsonify({'erro': 'Email inválido'}), 400
    if len(senha) < 6:
        return jsonify({'erro': 'A senha deve ter no mínimo 6 caracteres'}), 400

    conexao = conectar()
    if not conexao:
        return jsonify({'erro': 'Erro ao conectar ao banco'}), 500

    try:
        cursor = conexao.cursor()
        sql = """INSERT INTO usuarios (nome_usuarios, email, senha) VALUES (%s, %s, %s)"""
        valores = (nome, email, senha)
        cursor.execute(sql, valores)
        conexao.commit()
        return jsonify({'mensagem': 'Usuário criado com sucesso!', 'id': cursor.lastrowid}), 201
    except Error as erro:
        return jsonify({'erro': f'Erro ao inserir usuário: {erro}'}), 500
    finally:
        cursor.close()
        conexao.close()

@usuario_controller.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """Retorna a lista de usuários cadastrados."""
    conexao = conectar()
    if not conexao:
        return jsonify({'erro': 'Erro ao conectar ao banco'}), 500

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id, nome_usuarios, email FROM usuarios")
        usuarios = cursor.fetchall()
        return jsonify(usuarios), 200
    except Error as erro:
        return jsonify({'erro': f'Erro ao buscar usuários: {erro}'}), 500
    finally:
        cursor.close()
        conexao.close()

@usuario_controller.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    """Atualiza os dados de um usuário."""
    data = request.get_json()

    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip()
    senha = data.get('senha', '').strip()

    if len(nome) < 3:
        return jsonify({'erro': 'O nome deve ter pelo menos 3 caracteres'}), 400
    if not validar_email(email):
        return jsonify({'erro': 'Email inválido'}), 400
    if len(senha) < 6:
        return jsonify({'erro': 'A senha deve ter no mínimo 6 caracteres'}), 400

    conexao = conectar()
    if not conexao:
        return jsonify({'erro': 'Erro ao conectar ao banco'}), 500

    try:
        cursor = conexao.cursor()
        sql = """UPDATE usuarios SET nome_usuarios = %s, email = %s, senha = %s WHERE id = %s"""
        valores = (nome, email, senha, id)
        cursor.execute(sql, valores)
        conexao.commit()
        if cursor.rowcount == 0:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        return jsonify({'mensagem': 'Usuário atualizado com sucesso!'}), 200
    except Error as erro:
        return jsonify({'erro': f'Erro ao atualizar usuário: {erro}'}), 500
    finally:
        cursor.close()
        conexao.close()

@usuario_controller.route('/usuarios/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    """Exclui um usuário do banco de dados."""
    conexao = conectar()
    if not conexao:
        return jsonify({'erro': 'Erro ao conectar ao banco'}), 500

    try:
        cursor = conexao.cursor()
        sql = "DELETE FROM usuarios WHERE id = %s"
        cursor.execute(sql, (id,))
        conexao.commit()
        if cursor.rowcount == 0:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        return jsonify({'mensagem': 'Usuário excluído com sucesso!'}), 200
    except Error as erro:
        return jsonify({'erro': f'Erro ao excluir usuário: {erro}'}), 500
    finally:
        cursor.close()
        conexao.close()
