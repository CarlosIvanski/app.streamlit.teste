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

    # Carregar o arquivo Excel
    if 'df_oculto' not in st.session_state:
        try:
            st.session_state.df_oculto = pd.read_excel("dados.xlsx")  # Substitua pelo caminho do seu arquivo
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo Excel: {e}")

    # Botão para exibir a tabela do Excel
    if st.button("Mostrar dados gerenciáveis"):
        st.subheader("Tabela de Dados")
        st.dataframe(st.session_state.df_oculto)

else:
    st.warning("Você não tem permissão para acessar este dashboard. Por favor, insira um nome de usuário autorizado.")
