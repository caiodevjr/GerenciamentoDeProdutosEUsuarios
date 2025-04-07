import mysql.connector
from mysql.connector import Error

nomeusua= input("Nome do usuário: ")
email= input("Email: ")
senha= input("Senha: ")

dados = '(''\'' + nomeusua +'\''','+ email + ','+ senha +')'
declaracao="""INSERT INTO usuarios 
(nome_usuarios, email, senha) values """
sql2= declaracao + dados

try:
    conexao = mysql.connector.connect(
    host='localhost',
    database='crud_produtos',
    user='root',
    password=''
)
    inserir_usuarios = sql2
    cursor = conexao.cursor()
    cursor.execute(inserir_usuarios)
    conexao.commit()
    print(cursor.rowcount,"registro inserido na tabela!")
    cursor.close()
except Error as erro:
    print("Falha ao inserir dados no MySQL: {}".format(erro))