import mysql.connector
from mysql.connector import Error

def obter_dados_produto():
    """Solicita ao usuário os dados do produto."""
    nome = input("Nome do produto: ").strip()
    
    while True:
        try:
            preco = float(input("Preço do produto: ").replace(',', '.'))
            if preco <= 0:
                raise ValueError("O preço deve ser um valor positivo.")
            break
        except ValueError:
            print("Erro: Digite um preço válido.")

    while True:
        try:
            estoque = int(input("Estoque do produto: "))
            if estoque < 0:
                raise ValueError("O estoque deve ser um número inteiro maior ou igual a zero.")
            break
        except ValueError:
            print("Erro: Digite um número inteiro válido para o estoque.")

    return nome, preco, estoque

def inserir_produto(nome, preco, estoque):
    """Insere um novo produto no banco de dados."""
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='crud_produtos',
            user='root',
            password=''
        )

        cursor = conexao.cursor()
        sql = """INSERT INTO produtos (nome_produto, preco, estoque) 
                VALUES (%s, %s, %s)"""
        valores = (nome, preco, estoque)

        cursor.execute(sql, valores)
        conexao.commit()
        
        print(f"{cursor.rowcount} registro(s) inserido(s) com sucesso!")

    except Error as erro:
        print(f"Falha ao inserir dados no MySQL: {erro}")

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão com MySQL encerrada.")

if __name__ == "__main__":
    produto = obter_dados_produto()
    inserir_produto(*produto)
