import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Turmas", layout="wide")

st.title("Detalhes das Turmas")

st.subheader('Importar dados das turmas e professores')

# Função para carregar arquivo Excel
def load_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

# Permitir upload de múltiplos arquivos Excel
uploaded_files = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

# Inicializar variáveis para os dois arquivos importantes
df_professores = None
df_turmas = None

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = load_excel(uploaded_file)
        st.session_state[f'df_{uploaded_file.name}'] = df
        st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')

        # Mostrar os dados carregados em uma tabela editável
        df_editable = st.data_editor(df, use_container_width=True)
        st.session_state[f'df_{uploaded_file.name}'] = df_editable

        # Identificar qual arquivo é de professores e qual é de turmas
        if 'professores' in uploaded_file.name.lower():
            df_professores = df_editable
        elif 'turmas' in uploaded_file.name.lower():
            df_turmas = df_editable

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

# Sempre mostrar o botão de fusão
st.subheader("Realizar Fusão dos Dados")

# Botão para fundir os professores na tabela de turmas e criar uma nova tabela
if st.button("Fundir Professores com Turmas e Criar Nova Tabela"):
    if df_turmas is None or df_professores is None:
        st.warning("Certifique-se de ter carregado os arquivos de turmas e professores.")
    else:
        # Mensagem de debug para confirmar que o código chegou até aqui
        st.write("Iniciando fusão...")

        try:
            # Verificar se as colunas essenciais existem
            if 'Professor' not in df_professores.columns:
                st.error('Coluna "Professor" não encontrada no arquivo de professores.')
            elif 'Teacher' not in df_turmas.columns:
                st.error('Coluna "Teacher" não encontrada no arquivo de turmas.')
            else:
                # Fazer a fusão preenchendo a coluna "Teacher" com a coluna "Professor"
                df_fusao = df_turmas.copy()

                # Verificar o tamanho dos dataframes
                if len(df_professores) <= len(df_turmas):
                    df_fusao['Teacher'] = df_professores['Professor'].values[:len(df_turmas)]
                else:
                    st.warning("A tabela de professores tem mais linhas do que a tabela de turmas. Apenas as primeiras serão usadas.")

                st.success("Fusão realizada com sucesso! Nova tabela criada.")
                
                # Mostrar a nova tabela de fusão
                st.subheader("Tabela de Fusão (Turmas + Professores)")
                st.dataframe(df_fusao)

                # Botão para exportar a nova tabela de fusão para Excel
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_fusao.to_excel(writer, index=False, sheet_name='Tabela de Fusão')
                buffer.seek(0)

                st.download_button(
                    label="Baixar Excel",
                    data=buffer,
                    file_name="tabela_fusao.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except Exception as e:
            st.error(f"Erro durante a fusão: {e}")
