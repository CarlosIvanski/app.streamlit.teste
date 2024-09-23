import streamlit as st
import pandas as pd
import io

# Definir uma lista de usuários com permissões especiais
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

# Verificar se o nome do preenchedor está na lista de usuários com permissões especiais
if nome_preenchedor in usuarios_superadmin:
    st.subheader("teste")

st.title("Rota")

st.subheader('Importar dados das turmas e professores')

def load_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

uploaded_files = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

df_professores = None
df_turmas = None

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = load_excel(uploaded_file)
        st.session_state[f'df_{uploaded_file.name}'] = df
        st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')

        df_editable = st.data_editor(df, use_container_width=True)
        st.session_state[f'df_{uploaded_file.name}'] = df_editable

        if 'professores' in uploaded_file.name.lower():
            df_professores = df_editable
        elif 'turmas' in uploaded_file.name.lower():
            df_turmas = df_editable

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

st.subheader("Realizar Fusão dos Dados")

if st.button("Fundir Professores com Turmas e Criar Nova Tabela"):
    if df_turmas is None or df_professores is None:
        st.warning("Certifique-se de ter carregado os arquivos de turmas e professores.")
    else:
        st.write("Iniciando fusão...")
        with st.spinner("Processando..."):
            try:
                if 'Professor' not in df_professores.columns:
                    st.error('Coluna "Professor" não encontrada no arquivo de professores.')
                elif 'Teacher' not in df_turmas.columns:
                    st.error('Coluna "Teacher" não encontrada no arquivo de turmas.')
                else:
                    df_fusao = df_turmas.copy()

                    if len(df_professores) <= len(df_turmas):
                        df_fusao['Teacher'] = df_professores['Professor'].values[:len(df_turmas)]
                    else:
                        st.warning("A tabela de professores tem mais linhas do que a tabela de turmas. Apenas as primeiras serão usadas.")

                    st.success("Fusão realizada com sucesso! Nova tabela criada.")
                    
                    st.subheader("Tabela de Fusão (Turmas + Professores)")
                    st.dataframe(df_fusao)

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

# Exibir dados apenas para superadministradores
if usuario_atual in usuarios_superadmin:
    st.subheader("Dados para Superadministradores")
    st.write("Aqui estão os dados sensíveis que apenas superadministradores podem ver.")
    # Exibir os dados que você deseja mostrar
    if df_professores is not None:
        st.dataframe(df_professores)
    if df_turmas is not None:
        st.dataframe(df_turmas)
else:
    st.warning("Você não tem permissão para ver esses dados.")
