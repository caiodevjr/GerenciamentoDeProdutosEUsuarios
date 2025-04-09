import mysql.connector
from mysql.connector import Error
import re

def obter_dados_usuario():
    """Solicita os dados do usuário e realiza validações básicas."""
    nome = input("Nome do usuário: ").strip()

    while True:
        email = input("Email: ").strip()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        print("Erro: Digite um email válido.")

    while True:
        senha = input("Senha: ").strip()
        if len(senha) >= 6:
            break
        print("Erro: A senha deve ter pelo menos 6 caracteres.")

    return nome, email, senha

def inserir_usuario(nome, email, senha):
    """Insere um novo usuário no banco de dados."""
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            database='crud_produtos',
            user='root',
            password=''
        )

        cursor = conexao.cursor()
        sql = """INSERT INTO usuarios (nome_usuarios, email, senha) 
                VALUES (%s, %s, %s)"""
        valores = (nome, email, senha)

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
    usuario = obter_dados_usuario()
    inserir_usuario(*usuario)
