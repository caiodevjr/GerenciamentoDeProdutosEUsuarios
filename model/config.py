import mysql.connector

def conectar():
    return mysql.connector.connect(
    host='localhost',
    database='crud_produtos',
    user='root',
    password=''
)

#teste pra conexao com o banco

#if conexao.is_connected():
#    db_info=conexao.get_server_info()
#    print("conectado ao servidar mysql",db_info)
#    cursor=conexao.cursor()
#    cursor.execute("select database();")
#    linha=cursor.fetchone()
#    print("conectado ao banco dedados ",linha)   

#if conexao.is_connected():
#    cursor.close()
#    conexao.close()
#    print("conexão foi encerrada")'''
