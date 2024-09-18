# Função para converter os dados para DataFrame
def converter_para_dataframe(dados, nome_usuario, data):
    registros = []
    for professor, detalhes in dados.items():
        registro = {
            'Professor': professor,
            'Unidades': ', '.join([unidade for unidade, selecionado in detalhes.items() if unidade in unidades and selecionado]),
            'Carro': 'Sim' if detalhes.get('Carro', False) else 'Não',
            'Máquinas': ', '.join(detalhes['Máquina']),
            'Disponibilidade': ', '.join(detalhes['Disponibilidade']),
            'Módulo': ', '.join(detalhes['Modulo']),
            'Observações': detalhes.get('Observações', ''),
            'Nome do Preenchendor': nome_usuario,
            'Data': data.strftime('%Y-%m-%d')  # Garantindo que a data seja formatada sem hora
        }
        registros.append(registro)
    return pd.DataFrame(registros)

# Converter os dados coletados para um DataFrame
df_novo = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificacao)

# Botão para salvar os dados na tabela em tempo real
if st.button("Salvar dados"):
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, df_novo], ignore_index=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success("Dados salvos com sucesso!")

# Definir uma lista de usuários com permissões especiais
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

# Verificar se o nome do preenchedor está na lista de usuários com permissões especiais
if nome_preenchedor in usuarios_superadmin:
    st.subheader("Tabela Atualizada de Disponibilidade")

    # Iterar sobre as linhas do DataFrame e exibir as informações com botões de deletar
    for i, row in st.session_state.df_disponibilidade.iterrows():
        cols = st.columns(len(row) + 1)  # +1 para o botão de deletar
        for j, value in enumerate(row):
            cols[j].write(value)
        
        # Exibir o botão de deletar apenas se o nome do preenchedor estiver na lista de permissões
        if cols[len(row)].button("Deletar", key=f"delete_{i}"):
            deletar_linha(i)

    # Botão para exportar os dados para Excel, visível para todos os usuários na lista de permissões especiais
    st.subheader("Exportar Dados para Excel")
    if st.button("Exportar para Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df_disponibilidade.to_excel(writer, index=False, sheet_name='Disponibilidade')
        buffer.seek(0)
        
        st.download_button(
            label="Baixar Excel",
            data=buffer,
            file_name="disponibilidade_professores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
