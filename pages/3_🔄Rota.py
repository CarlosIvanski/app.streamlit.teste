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
                    # Usando o DataFrame pré-programado
                    df_fusao = df_pre_programado.copy()

                    # Alocar a coluna "Teacher" da tabela de fusão
                    df_fusao['Teacher'] = df_fusao['Professor']

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
