from model.config import conectar
from flask import Blueprint, render_template, request, redirect, jsonify, flash

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
        print(f"Erro ao executar query: {e}")
        return []  

@produto_bp.route('/enviar', methods=['POST'])
def enviar():
    try:
        nome_produto = request.form.get('nome')
        preco = float(request.form.get('preco'))
        estoque = int(request.form.get('estoque'))

        query = "INSERT INTO produtos (nome_produto, preco, estoque) VALUES (%s, %s, %s)"
        valores = (nome_produto, preco, estoque)
        executar_query(query, valores)

        flash("Produto cadastrado com sucesso!", "success")
        return redirect('/produto')
    except Exception as e:
        flash(f"Erro ao inserir no banco: {e}", "error")
        return redirect('/produto')

@produto_bp.route('/produto')
def produto():
    try:
        produtos = executar_query("SELECT * FROM produtos ORDER BY id_produtos DESC", fetch=True)
        
        if not isinstance(produtos, list):
            produtos = []
        
        return render_template('produto.html', produtos=produtos)
    except Exception as e:
        return f"Erro ao carregar produtos: {e}"


@produto_bp.route('/listar')
def listar():
    try:
        produtos = executar_query("SELECT * FROM produtos", fetch=True)
        return jsonify(produtos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@produto_bp.route('/editar/<int:id_produtos>')
def editar(id_produtos):
    try:
        produto = executar_query("SELECT * FROM produtos WHERE id_produtos = %s", (id_produtos,), fetch=True)
        if produto:
            return render_template('editar_produto.html', produto=produto[0])
        else:
            flash(f"Produto com ID {id_produtos} não encontrado.", "error")
            return redirect('/produto')
    except Exception as e:
        flash(f"Erro ao carregar produto: {e}", "error")
        return redirect('/produto')

@produto_bp.route('/atualizar/<int:id_produtos>', methods=['POST'])
def atualizar(id_produtos):
    try:
        nome = request.form.get('nome')
        preco = float(request.form.get('preco'))
        estoque = int(request.form.get('estoque'))

        query = """UPDATE produtos 
                SET nome_produto = %s, preco = %s, estoque = %s 
                WHERE id_produtos = %s"""
        valores = (nome, preco, estoque, id_produtos)
        executar_query(query, valores)

        flash("Produto atualizado com sucesso!", "success")
        return redirect('/produto')
    except Exception as e:
        flash(f"Erro ao atualizar produto: {e}", "error")
        return redirect('/produto')

@produto_bp.route('/excluir/<int:id_produtos>', methods=['GET', 'POST'])
def excluir(id_produtos):
    try:
        query = "DELETE FROM produtos WHERE id_produtos = %s"
        resultado = executar_query(query, (id_produtos,))

        if resultado:
            flash("Produto excluído com sucesso!", "success")
        else:
            flash("Produto não encontrado.", "error")

        return redirect('/produto')
    except Exception as e:
        flash(f"Erro ao excluir produto: {e}", "error")
        return redirect('/produto')
