import streamlit as st
import pandas as pd
import io

usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

st.title("Acesso ao Dashboard da Rota")

usuario_atual = st.text_input("Digite seu nome de usuário:")

if usuario_atual in usuarios_superadmin:
    st.success("Acesso autorizado! Bem-vindo ao dashboard.")

    st.subheader('Importar dados das turmas e professores')

    def load_excel(uploaded_file, start_row=0):
        df = pd.read_excel(uploaded_file, skiprows=start_row)
        return df

    uploaded_files = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

    df_professores = None
    df_turmas = None

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Definindo a linha inicial para leitura
            start_row = 1 if 'turmas' in uploaded_file.name.lower() else 0  # Começa da linha 2 para turmas, linha 1 para professores
            df = load_excel(uploaded_file, start_row=start_row)
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
                    # Dados pré-programados para a tabela de fusão
                    dados_pre_programados = {
                        "Turma": [
                            "CONVERSATION 2 ONLINE",
                            "CONVERSATION 5 ONLINE",
                            "CONVERSATION 14 PRESENCIAL",
                            "CONVERSATION 12 PRESENCIAL",
                            "CONVERSATION 11 ONLINE",
                            "CONVERSATION 10 PRESENCIAL",
                            "CONVERSATION 7 PRESENCIAL",
                            "ACAPULCO COLABORADORES ONLINE",
                            "GALICIA ONLINE"
                        ],
                        "Professor": [
                            "Carlos", "Luciano", "Bruno", "Maria", 
                            "Maddie", "Luciana", "Bruno", "Maria", "Maria"
                        ]
                    }
                    df_pre_programado = pd.DataFrame(dados_pre_programados)

                    # Garantir que as colunas tenham o mesmo tipo
                    df_turmas['Teacher'] = df_turmas['Teacher'].astype(str)
                    df_pre_programado['Professor'] = df_pre_programado['Professor'].astype(str)

                    # Combinar os dados da tabela pré-programada com os dados da segunda planilha
                    df_fusao = pd.merge(df_turmas, df_pre_programado, left_on='Teacher', right_on='Professor', how='outer')

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
