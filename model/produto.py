import mysql.connector
from mysql.connector import Error

nomeprod= input("Nome do produto: ")
precoprod= input("Preço do produto: ")
quantoprod= input("Estoque do produto: ")

dados = '(''\'' + nomeprod +'\''','+ precoprod + ','+ quantoprod+')'
declaracao="""INSERT INTO produtos 
(nome_produto, preco, estoque) values """
sql= declaracao + dados

try:
    conexao = mysql.connector.connect(
    host='localhost',
    database='crud_produtos',
    user='root',
    password=''
)
    inserir_produtos = sql
    cursor = conexao.cursor()
    cursor.execute(inserir_produtos)
    conexao.commit()
    print(cursor.rowcount,"registro inserido na tabela!")
    cursor.close()
except Error as erro:
    print("Falha ao inserir dados no MySQL: {}".format(erro))