import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

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

st.title("Table de Turmas")
st.dataframe(df)

excel_file = "disponibilidade.xlsx"
df.to_excel(excel_file, index=False)

st.download_button(
    label="Baixar tabela como Excel",
    data=open(excel_file, "rb").read(),
    file_name="TURMAS.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
