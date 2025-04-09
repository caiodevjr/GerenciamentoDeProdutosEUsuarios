import mysql.connector

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
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None

def testar_conexao():
    """Testa a conexão com o banco de dados e exibe informações."""
    conexao = conectar()
    
    if conexao and conexao.is_connected():
        try:
            db_info = conexao.get_server_info()
            print(f"Conectado ao servidor MySQL, versão: {db_info}")

            cursor = conexao.cursor()
            cursor.execute("SELECT DATABASE();")
            banco = cursor.fetchone()
            print(f"Conectado ao banco de dados: {banco[0]}")

        except mysql.connector.Error as erro:
            print(f"Erro ao executar consulta: {erro}")

        finally:
            cursor.close()
            conexao.close()
            print("Conexão encerrada.")

if __name__ == "__main__":
    testar_conexao()


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
