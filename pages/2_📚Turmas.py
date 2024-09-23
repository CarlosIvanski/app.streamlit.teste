import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Turmas", layout="wide"
)

st.title("Detalhes das Turmas")

st.subheader('Importar dados das turmas')

# Função para carregar arquivo Excel
def load_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

# Carregar arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

# Carregar os dados do Excel para o st.session_state apenas uma vez
if uploaded_file is not None and 'df' not in st.session_state:
    st.session_state.df = load_excel(uploaded_file)
    st.success('Arquivo carregado com sucesso!')

    # Mostrar os dados carregados em uma tabela editável
    df_editable = st.data_editor(st.session_state.df, use_container_width=True)
    
    # Atualizar o DataFrame na sessão após a edição
    st.session_state.df = df_editable

    # Botão para exportar os dados editados para Excel
    st.subheader("Exportar Dados Editados para Excel")
    if st.button("Exportar para Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df.to_excel(writer, index=False, sheet_name='Dados Editados')
        buffer.seek(0)
        
        st.download_button(
            label="Baixar Excel",
            data=buffer,
            file_name="dados_editados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
