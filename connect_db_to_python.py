import mysql.connector

# Conectar ao banco de dados MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mc030446!",
    database="teste"
)

cursor = conn.cursor()

# Testar a conexão e listar tabelas
cursor.execute("SHOW TABLES")
tabelas = cursor.fetchall()

print("Tabelas no banco de dados:")
for tabela in tabelas:
    print(tabela[0])

# Fechar a conexão
cursor.close()
conn.close()
