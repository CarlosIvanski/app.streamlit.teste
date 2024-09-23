import streamlit as st
import pandas as pd
import io

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
