from model.config import conectar
from flask import Blueprint, render_template, request, redirect, jsonify, flash
import bcrypt #pip install bcrypt

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

def executar_query(query, valores=None, fetch=False):
    """Executa uma query SQL no banco de dados"""
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, valores or ())
        if fetch:
            resultado = cursor.fetchall()
        else:
            conn.commit()
            resultado = cursor.lastrowid

        cursor.close()
        conn.close()
        return resultado
    except Exception as e:
        return f"Erro ao executar query: {e}"

def hash_senha(senha):
    """Criptografa a senha usando bcrypt"""
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@usuario_bp.route('/enviar_usuario', methods=['POST'])
def enviar_usuario():
    try:
        nome_usuario = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        senha_criptografada = hash_senha(senha)

        query = "INSERT INTO usuarios (nome_usuarios, email, senha) VALUES (%s, %s, %s)"
        valores = (nome_usuario, email, senha_criptografada)
        executar_query(query, valores)

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect('/usuario')
    except Exception as e:
        flash(f"Erro ao inserir no banco: {e}", "error")
        return redirect('/usuario')

@usuario_bp.route('/usuario')
def usuario():
    try:
        usuarios = executar_query("SELECT id_usuarios, nome_usuarios, email FROM usuarios ORDER BY id_usuarios DESC", fetch=True)
        return render_template('usuario.html', usuarios=usuarios)
    except Exception as e:
        return f"Erro ao carregar usuários: {e}"

@usuario_bp.route('/listar_usuarios')
def listar_usuarios():
    try:
        usuarios = executar_query("SELECT id_usuarios, nome_usuarios, email FROM usuarios", fetch=True)
        return jsonify(usuarios)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@usuario_bp.route('/editar_usuario/<int:id_usuarios>')
def editar_usuario(id_usuarios):
    try:
        usuario = executar_query("SELECT id_usuarios, nome_usuarios, email FROM usuarios WHERE id_usuarios = %s", (id_usuarios,), fetch=True)
        if usuario:
            return render_template('editar_usuario.html', usuario=usuario[0])
        else:
            flash(f"Usuário com ID {id_usuarios} não encontrado.", "error")
            return redirect('/usuario')
    except Exception as e:
        flash(f"Erro ao carregar usuário: {e}", "error")
        return redirect('/usuario')

@usuario_bp.route('/atualizar_usuario/<int:id_usuarios>', methods=['POST'])
def atualizar_usuario(id_usuarios):
    try:
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        senha_criptografada = hash_senha(senha)

        query = """UPDATE usuarios 
                SET nome_usuarios = %s, email = %s, senha = %s 
                WHERE id_usuarios = %s"""
        valores = (nome, email, senha_criptografada, id_usuarios)
        executar_query(query, valores)

        flash("Usuário atualizado com sucesso!", "success")
        return redirect('/usuario')
    except Exception as e:
        flash(f"Erro ao atualizar usuário: {e}", "error")
        return redirect('/usuario')

@usuario_bp.route('/excluir_usuario/<int:id_usuarios>', methods=['GET', 'POST'])
def excluir_usuario(id_usuarios):
    try:
        query = "DELETE FROM usuarios WHERE id_usuarios = %s"
        resultado = executar_query(query, (id_usuarios,))

        if resultado:
            flash("Usuário excluído com sucesso!", "success")
        else:
            flash("Usuário não encontrado.", "error")

        return redirect('/usuario')
    except Exception as e:
        flash(f"Erro ao excluir usuário: {e}", "error")
        return redirect('/usuario')