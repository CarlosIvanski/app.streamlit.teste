import mysql.connector

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mc030446!",
        database="teste"
    )

def alocar_professores():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Obter IDs das turmas
    cursor.execute("SELECT id_turma FROM turmas")
    turmas = cursor.fetchall()

    # Obter IDs dos professores
    cursor.execute("SELECT id_prof FROM professores")  # Ajuste o nome da coluna conforme necessário
    professores = cursor.fetchall()

    # Verificar se há pelo menos 3 turmas e 3 professores
    if len(turmas) < 3 or len(professores) < 3:
        print("Número insuficiente de turmas ou professores.")
        conn.close()
        return

    # Alocar 3 professores em 3 turmas
    for i in range(3):
        id_turma = turmas[i][0]
        id_professor = professores[i][0]

        # Inserir alocação
        cursor.execute("INSERT INTO alocacoes_professores (id_professor, id_turma) VALUES (%s, %s)", (id_professor, id_turma))

    # Confirmar as alterações
    conn.commit()
    conn.close()
    print("Professores alocados com sucesso!")

# Executar a função
alocar_professores()