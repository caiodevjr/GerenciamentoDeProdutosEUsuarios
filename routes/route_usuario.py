from model.config import conectar
from flask import Flask, render_template, request, redirect, Blueprint

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/')
def home():
    return render_template('index.html')  

@usuario_bp.route('/usuario.html')
def cadastrar_usuario():
    return render_template('usuario.html')

@usuario_bp.route('/index.html')
def index():
    return render_template('index.html')


@usuario_bp.route('/enviar_usuario', methods=['POST'])
def enviar_usuario():
    try:
        nome_usuario = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        conexao = conectar()
        cursor = conexao.cursor()

        query = "INSERT INTO usuarios (nome_usuarios, email, senha) VALUES (%s, %s, %s)"
        valores = (nome_usuario, email, senha)
        cursor.execute(query, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect('/usuario')
    except Exception as e:
        return f"Erro ao inserir no banco: {e}"


@usuario_bp.route('/usuario')
def usuario():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios ORDER BY id_usuarios DESC")  
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('usuario.html', usuarios=usuarios)
    except Exception as e:
        return f"Erro ao carregar página: {e}"


@usuario_bp.route('/listar_usuarios')
def listar_usuarios():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        return f"Erro ao buscar usuários: {e}"


@usuario_bp.route('/editar_usuario/<int:id_usuarios>')
def editar_usuario(id_usuarios):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuarios = %s", (id_usuarios,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()

        if usuario:
            return render_template('editar_usuario.html', usuario=usuario)
        else:
            return f"Usuário com ID {id_usuarios} não encontrado."

    except Exception as e:
        return f"Erro ao carregar usuário: {e}"


@usuario_bp.route('/atualizar_usuario/<int:id_usuarios>', methods=['POST'])
def atualizar_usuario(id_usuarios):
    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nome_usuarios = %s, email = %s, senha = %s WHERE id_usuarios = %s",
            (nome, email,senha, id_usuarios)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/usuario')  
    except Exception as e:
        return f"Erro ao atualizar usuário: {e}"


@usuario_bp.route('/excluir_usuario/<int:id_usuarios>', methods=['GET','POST'])
def excluir_usuario(id_usuarios):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuarios = %s", (id_usuarios,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/usuario')  
    except Exception as e:
        return f"Erro ao excluir usuário: {e}"
