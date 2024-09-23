import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")


# Lista de usuários superadministradores
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]
usuario_permitido = "usuario_especifico"  # Substitua pelo nome do usuário permitido para upload

# Input do usuário
usuario_atual = st.text_input("Digite seu nome de usuário:")

if usuario_atual in usuarios_superadmin:
    st.success("Acesso autorizado! Bem-vindo ao dashboard.")

    def load_excel(uploaded_file):
        df = pd.read_excel(uploaded_file)
        return df

    # Verifica se a tabela já foi carregada
    if 'df_upload' not in st.session_state:
        st.session_state['df_upload'] = None

    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

    if uploaded_file and usuario_atual == usuario_permitido:
        df = load_excel(uploaded_file)
        st.session_state['df_upload'] = df
        st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')

    # Exibir a tabela carregada, se existir
    if st.session_state['df_upload'] is not None:
        df_editable = st.data_editor(st.session_state['df_upload'], use_container_width=True)
        st.session_state['df_upload'] = df_editable

        if st.button("Exportar tabela editada para Excel"):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_editable.to_excel(writer, index=False, sheet_name='Dados Editados')
            buffer.seek(0)
            st.download_button(
                label="Baixar tabela editada",
                data=buffer,
                file_name="tabela_editada.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Botão para deletar a tabela
        if st.button("Deletar tabela"):
            del st.session_state['df_upload']
            st.success("Tabela deletada com sucesso!")

    elif uploaded_file:
        st.warning("Você não tem permissão para fazer upload deste arquivo.")
