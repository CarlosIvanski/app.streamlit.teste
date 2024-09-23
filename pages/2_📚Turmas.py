import streamlit as st
import pandas as pd
import io

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

    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

    if uploaded_file and usuario_atual == usuario_permitido:
        df = load_excel(uploaded_file)
        st.session_state['df_upload'] = df
        st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')

        # Exibir a tabela carregada
        df_editable = st.data_editor(df, use_container_width=True)
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
            if 'df_upload' in st.session_state:
                del st.session_state['df_upload']
                st.success("Tabela deletada com sucesso!")
            else:
                st.warning("Nenhuma tabela para deletar.")

    elif uploaded_file:
        st.warning("Você não tem permissão para fazer upload deste arquivo.")
