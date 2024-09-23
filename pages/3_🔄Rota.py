import streamlit as st
import pandas as pd

# Lista de usuários superadministradores
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

# Título do dashboard
st.title("Acesso ao Dashboard da Rota")

# Input para o nome de usuário
usuario_atual = st.text_input("Digite seu nome de usuário:")

if usuario_atual in usuarios_superadmin:
    st.success("Acesso autorizado! Bem-vindo ao dashboard.")

    # Botão "falso"
    if st.button("Clique aqui para armazenar dados"):
        st.success("Dados armazenados lidos com sucesso!")

    # Verificar se o DataFrame já foi criado
    if 'df_oculto' not in st.session_state:
        # Criar a tabela pré-armazenada com os dados fornecidos
        dados = {
            "Grupo": [
                "CONVERSATION 2 ONLINE",
                "CONVERSATION 5 ONLINE",
                "CONVERSATION 14 PRESENCIAL",
                "CONVERSATION 12 PRESENCIAL",
                "CONVERSATION 11 ONLINE",
                "CONVERSATION 10 PRESENCIAL",
                "CONVERSATION 7 PRESENCIAL"
            ],
            "Horário": ["21:00", "20:00", "08:00", "19:00", "07:00", "20:00", "18:00"],
            "Unidade": ["Vicentina", "Vicentina", "Vicentina", "Satélite", "Vicentina", "Jardim", "Vicentina"],
            "Dias da Semana": ["3ª ● 5ª", "2ª ● 4ª", "3ª", "4ª", "6ª", "4ª", "6ª"],
            "Stage": ["#REF!", "#REF!", "#REF!", "#REF!", "#REF!", "#REF!", "#REF!"],
            "Livro": ["", "", "", "", "", "", ""],
            "MOD": ["CONV", "CONV", "CONV - INICIANTE", "CONV - INTERMEDIÁRIO", "CONV - INTERMEDIÁRIO", "CONV - INTERMEDIÁRIO", "CONV - INTERMEDIÁRIO"],
            "N Aula": ["2", "2", "1", "1", "1", "1", "1"],
            "PARAG ATUAL": ["#REF!", "#REF!", "#REF!", "#REF!", "#REF!", "#REF!", "#REF!"],
            "PARAG FINAL": ["#REF!", "#REF!", "#REF!", "#REF!", "#REF!", "#REF!", "#REF!"],
            "Teacher": ["Carlos", "Luciano", "Bruno", "Maria", "Maddie", "Luciana", "Bruno"],
            "Status": ["Online", "Online", "Presencial", "Presencial", "Online", "Presencial", "Presencial"]
        }
        st.session_state.df_oculto = pd.DataFrame(dados)

    # Botão para exibir a tabela
    if st.button("Mostrar dados gerenciáveis"):
        st.subheader("Tabela de Dados")
        st.dataframe(st.session_state.df_oculto)

else:
    st.warning("Você não tem permissão para acessar este dashboard. Por favor, insira um nome de usuário autorizado.")

# Função para ler o arquivo existente
def read_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()

# Especificar o caminho para o arquivo Excel existente
file_path = 'pages/TURMAS.xlsx'

# Ler o conteúdo do arquivo
excel_data = read_file(file_path)

# Botão de download para o arquivo Excel existente
st.download_button(
    label="Baixar exemplo.xlsx",
    data=excel_data,
    file_name='TURMAS_final.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
