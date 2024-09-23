import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
import io

usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

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

st.set_page_config(layout="wide")

uploaded_files = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

data = {
    "Grupo": ["Abu Dhabi Online", "Auckland Presencial", "Botswana Online", "Brooklyn Presencial", "Chicago Presencial", "Connecticut Presencial"],
    "Horário": ["19:00", "19:00", "19:00", "19:00", "19:00", "19:00"],
    "Unidade": ["Vicentina", "Satélite", "Vicentina", "Satélite", "Jardim", "Satélite"],
    "Dias da Semana": ["2ª ● 3ª ● 4ª ● 5ª", "2ª ● 3ª ● 4ª ● 5ª", "2ª ● 4ª ● 5ª", "2ª ● 3ª ● 5ª", "2ª ● 3ª ● 4ª ● 5ª", "2ª ● 3ª ● 5ª"],
    "MOD": ["Grupo", "Grupo", "Grupo", "Grupo", "Grupo", "Grupo"],
    "N Aulas": ["4", "4", "3", "3", "4", "3"],
    "Teacher": ["", "", "", "", "", ""],
    "Status": ["Online", "Presencial", "Online", "Presencial", "Presencial", "Presencial"]
}

df = pd.DataFrame(data)

st.title("Tabela de Turmas")
st.dataframe(df)

excel_file = "disponibilidade.xlsx"
df.to_excel(excel_file, index=False)

st.download_button(
    label="Baixar tabela como Excel",
    data=open(excel_file, "rb").read(),
    file_name="TURMAS.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
