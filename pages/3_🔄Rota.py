import streamlit as st
import pandas as pd
import io

usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

st.title("Acesso ao Dashboard da Rota")

usuario_atual = st.text_input("Digite seu nome de usuário:")

if usuario_atual in usuarios_superadmin:
    st.success("Acesso autorizado! Bem-vindo ao dashboard.")

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
                    elif 'Unnamed: 10' not in df_turmas.columns:
                        st.error('Coluna "Unnamed: 10" não encontrada no arquivo de turmas.')
                    else:
                        df_fusao = df_turmas.copy()

                        # Ajustar o número de linhas na fusão
                        n_professores = len(df_professores)
                        n_turmas = len(df_turmas)

                        if n_professores < n_turmas:
                            # Preencher somente até o número de professores disponíveis
                            df_fusao['Unnamed: 10'] = pd.Series(df_professores['Professor'].values)
                        else:
                            # Se houver mais professores do que turmas, use apenas os primeiros
                            df_fusao['Unnamed: 10'] = df_professores['Professor'].values[:n_turmas]

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

else:
    st.warning("Você não tem permissão para acessar este dashboard. Por favor, insira um nome de usuário autorizado.")
