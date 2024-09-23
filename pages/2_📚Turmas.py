import streamlit as st
import pandas as pd
import io
from time import sleep

st.set_page_config(page_title="Turmas", layout="wide")

st.title("Detalhes das Turmas")
st.subheader('Importar dados das turmas')

# Função para carregar arquivo Excel com indicador de progresso
def load_excel(uploaded_file):
    with st.spinner("Carregando arquivo..."):
        df = pd.read_excel(uploaded_file)
        sleep(1)  # Simulação de tempo de carregamento
    return df

# Permitir upload de múltiplos arquivos Excel
uploaded_files = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = load_excel(uploaded_file)
        st.session_state[f'df_{uploaded_file.name}'] = df
        st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')
        
        # Mostrar os dados carregados em uma tabela editável
        df_editable = st.data_editor(df, use_container_width=True)
        st.session_state[f'df_{uploaded_file.name}'] = df_editable

        # Botão para exportar os dados editados para Excel
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

# Carregar e fundir usando pd.merge por uma coluna comum (por exemplo, 'ID')
if uploaded_files and len(uploaded_files) == 2:
    df1 = load_excel(uploaded_files[0])
    df2 = load_excel(uploaded_files[1])

    st.success(f"Arquivos {uploaded_files[0].name} e {uploaded_files[1].name} carregados com sucesso!")
    
    # Fazer a fusão horizontal por uma coluna comum (exemplo: 'ID')
    df_fused = pd.merge(df1, df2, on='ID', how='inner')
    
    st.subheader("Dados Fundidos por Coluna Comum")
    st.dataframe(df_fused, use_container_width=True)

    # Botão para exportar os dados fundidos
    if st.button("Exportar para Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_fused.to_excel(writer, index=False, sheet_name='Dados Fundidos')
        buffer.seek(0)

        st.download_button(
            label="Baixar Excel",
            data=buffer,
            file_name="dados_fundidos_por_id.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
