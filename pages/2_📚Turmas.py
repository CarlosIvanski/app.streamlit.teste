import streamlit as st
import pandas as pd
import io

# Lista de usuários superadministradores
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

# Input do usuário
usuario_atual = st.text_input("Digite seu nome de usuário:")

if usuario_atual in usuarios_superadmin:
    st.success("Acesso autorizado! Bem-vindo ao dashboard.")

    def load_excel(uploaded_file):
        df = pd.read_excel(uploaded_file)
        return df

    uploaded_files = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = load_excel(uploaded_file)
            st.session_state[f'df_{uploaded_file.name}'] = df
            st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')

            df_editable = st.data_editor(df, use_container_width=True)
            st.session_state[f'df_{uploaded_file.name}'] = df_editable

            if st.button(f"Exportar {uploaded_file.name} para Excel"):
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_editable.to_excel(writer, index=False, sheet_name='Dados Editados')
                buffer.seek(0)
                st.download_button(
                    label=f"Baixar {uploaded_file.name} editado",
                    data=buffer,
                    file_name=f"{uploaded_file.name}_editado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
