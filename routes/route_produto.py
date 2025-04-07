from model.config import conectar
from flask import Flask, render_template, request, redirect, Blueprint

produto_bp = Blueprint('produto_bp', __name__)

@produto_bp.route('/')
def home():
    return render_template('index.html')  
@produto_bp.route('/produto.html')
def cadastrar_produto():
    return render_template('produto.html')
@produto_bp.route('/usuario.html')
def cadastrar_usuario():
    return render_template('usuario.html')
@produto_bp.route('/index.html')
def index():
    return render_template('index.html')


@produto_bp.route('/enviar', methods=['POST'])
def enviar():
    try:
        nome_produto = request.form.get('nome')
        preco = float(request.form.get('preco'))
        estoque = int(request.form.get('estoque'))
        conexao = conectar()
        cursor = conexao.cursor()

        query = "INSERT INTO produtos (nome_produto, preco, estoque) VALUES (%s, %s, %s)"
        valores = (nome_produto, preco, estoque)
        cursor.execute(query, valores)
        conexao.commit()

        cursor.close()
        conexao.close()

        return redirect('/produto')
    except Exception as e:
        return f"Erro ao inserir no banco: {e}"
    
@produto_bp.route('/produto')
def produto():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos ORDER BY id_produtos DESC")  
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('produto.html', produtos=produtos)
    except Exception as e:
        return f"Erro ao carregar página: {e}"
    
@produto_bp.route('/listar')
def listar():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        cursor.close()
        conn.close()
        return produtos
    except Exception as e:
        return f"Erro ao buscar produtos: {e}"

@produto_bp.route('/editar/<int:id_produtos>')
def editar(id_produtos):
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produtos WHERE id_produtos = %s", (id_produtos,))
        produto = cursor.fetchone()
        cursor.close()
        conn.close()

        if produto:
            return render_template('editar_produto.html', produto=produto)
        else:
            return f"Produto com ID {id_produtos} não encontrado."

    except Exception as e:
        return f"Erro ao carregar produto: {e}"

@produto_bp.route('/atualizar/<int:id_produtos>', methods=['POST'])
def atualizar(id_produtos):
    try:
        nome = request.form.get('nome')
        preco = float(request.form.get('preco'))
        estoque = int(request.form.get('estoque'))

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produtos SET nome_produto = %s, preco = %s, estoque = %s WHERE id_produtos = %s",
            (nome, preco, estoque, id_produtos)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/produto')  
    except Exception as e:
        return f"Erro ao atualizar produto: {e}"
    
@produto_bp.route('/excluir/<int:id_produtos>', methods=['GET','POST'])
def excluir(id_produtos):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id_produtos = %s", (id_produtos,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/produto')  
    except Exception as e:
        return f"Erro ao excluir produto: {e}"

