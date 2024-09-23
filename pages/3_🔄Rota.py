import streamlit as st
import pandas as pd
import io

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

    # Placeholder para o arquivo Excel pré-implementado
    excel_data = {
        "Coluna 1": ["Dado 1", "Dado 2", "Dado 3"],
        "Coluna 2": ["Valor 1", "Valor 2", "Valor 3"]
    }
    df_oculto = pd.DataFrame(excel_data)

    # Botão para exibir a tabela do Excel
    if st.button("Mostrar dados gerenciáveis"):
        st.subheader("Tabela de Dados")
        st.dataframe(df_oculto)

else:
    st.warning("Você não tem permissão para acessar este dashboard. Por favor, insira um nome de usuário autorizado.")
