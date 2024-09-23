import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(layout="wide")

# Lista de usuários superadministradores
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]
usuario_permitido = "BrunoMorgilloCoordenadorSUPERADMIN_123456"  # Substitua pelo nome do usuário permitido para upload
csv_file_path = 'tabela_dados.csv'  # Caminho do arquivo CSV

# Input do usuário
usuario_atual = st.text_input("Digite seu nome de usuário:")

if usuario_atual in usuarios_superadmin:
    st.success("Acesso autorizado! Bem-vindo ao dashboard.")

    def load_excel(uploaded_file, start_row=1):
        df = pd.read_excel(uploaded_file, skiprows=start_row)
        return df

    # Verifica se o arquivo CSV existe e carrega os dados
    if os.path.exists(csv_file_path):
        st.session_state['df_upload'] = pd.read_csv(csv_file_path)
    else:
        st.session_state['df_upload'] = None

    uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

    if uploaded_file and usuario_atual == usuario_permitido:
        # Defina a linha a partir da qual você deseja começar a ler (por exemplo, 2 para começar da terceira linha)
        df = load_excel(uploaded_file, start_row=1)
        st.session_state['df_upload'] = df
        df.to_csv(csv_file_path, index=False)  # Salva os dados no CSV
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
            if os.path.exists(csv_file_path):
                os.remove(csv_file_path)
            st.session_state['df_upload'] = None
            st.success("Tabela deletada com sucesso!")

    elif uploaded_file:
        st.warning("Você não tem permissão para fazer upload deste arquivo.")
