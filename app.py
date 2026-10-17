import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuração da página do Streamlit
st.set_page_config(page_title="Meu Assistente de Investimentos", page_icon="🤖", layout="wide")

# 1. Definição da Carteira do Usuário (Ativo, Quantidade, Preço Médio de Compra)
carteira_dados = {
    "Ativo": ["PETR4.SA", "VALE3.SA", "WEGE3.SA", "IVVB11.SA"],
    "Quantidade": [100, 50, 120, 30],
    "Preço Médio": [32.50, 68.20, 41.10, 280.00]
}
df_carteira = pd.DataFrame(carteira_dados)

st.title("🤖 InvestBot - Seu Assistente de Investimentos")
st.markdown("Bem-vindo de volta! Vamos ver como estão os seus investimentos hoje.")
st.markdown("---")

# 2. Buscar cotações atuais via Yahoo Finance
@st.cache_data(ttl=3600)  # Guarda os dados em cache por 1 hora para carregar rápido
def carregar_dados(tickers):
    dados = yf.download(tickers, period="1d")['Close']
    return dados.iloc[-1] if not dados.empty else pd.Series()

with st.spinner("O robô está consultando o mercado financeiro..."):
    cotacoes_atuais = carregar_dados(df_carteira["Ativo"].tolist())

# Processar os cálculos da carteira
df_carteira["Preço Atual"] = df_carteira["Ativo"].map(cotacoes_atuais)
df_carteira["Valor Investido"] = df_carteira["Quantidade"] * df_carteira["Preço Médio"]
df_carteira["Valor Atual"] = df_carteira["Quantidade"] * df_carteira["Preço Atual"]
df_carteira["Lucro/Prejuízo R$"] = df_carteira["Valor Atual"] - df_carteira["Valor Investido"]
df_carteira["Rentabilidade %"] = (df_carteira["Lucro/Prejuízo R$"] / df_carteira["Valor Investido"]) * 100

total_investido = df_carteira["Valor Investido"].sum()
total_atual = df_carteira["Valor Atual"].sum()
lucro_total = total_atual - total_investido
rentabilidade_total = (lucro_total / total_investido) * 100

# 3. Exibição dos Indicadores Gerais
col1, col2, col3 = st.columns(3)
col1.metric("Valor Total Investido", f"R$ {total_investido:,.2f}")
col2.metric("Patrimônio Atual", f"R$ {total_atual:,.2f}", f"{rentabilidade_total:+.2f}%")
col3.metric("Resultado Geral (Lucro/Preju)", f"R$ {lucro_total:,.2f}")

st.markdown("---")

# 4. Divisão da Tela: Gráficos de um lado, Inteligência do Robô do outro
col_grafico, col_robo = st.columns([3, 2])

with col_grafico:
    st.subheader("📊 Distribuição do seu Patrimônio")
    fig = px.pie(df_carteira, values='Valor Atual', names='Ativo', 
                 title="Onde seu dinheiro está alocado atualmente",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

with col_robo:
    # Aparência do Robô
    st.subheader("💬 Fala, InvestBot!")
    
    # Lógica de análise do Robô baseado nos resultados reais
    if rentabilidade_total > 5:
        emoji_robo = "😎🚀"
        mensagem_robo = f"Sua carteira está voando alto com **{rentabilidade_total:.2f}%** de lucro acumulado! Parabéns pelas escolhas."
    elif rentabilidade_total >= 0:
        emoji_robo = "🙂👍"
        mensagem_robo = f"Estamos no azul! Sua carteira apresenta estabilidade com uma leve alta de **{rentabilidade_total:.2f}%**. O segredo é o longo prazo."
    else:
        emoji_robo = "🧐📉"
        mensagem_robo = f"O mercado está em um momento de correção e sua carteira recuou **{rentabilidade_total:.2f}%**. Não se desespere, momentos de queda podem ser ótimas oportunidades para comprar ativos de valor mais barato!"

    # Exibição estilizada da fala do Robô
    st.info(f"**Robô diz:** {emoji_robo}\n\n{mensagem_robo}")
    
    # O robô aponta o melhor e o pior ativo da carteira
    melhor_ativo = df_carteira.loc[df_carteira['Rentabilidade %'].idxmax()]
    pior_ativo = df_carteira.loc[df_carteira['Rentabilidade %'].idxmin()]
    
    st.markdown(f"⭐ **Destaque Positivo:** O ativo **{melhor_ativo['Ativo']}** está com o melhor desempenho da sua carteira (**{melhor_ativo['Rentabilidade %']:+.2f}%**).")
    st.markdown(f"⚠️ **Atenção:** O ativo **{pior_ativo['Ativo']}** está segurando o seu rendimento hoje (**{pior_ativo['Rentabilidade %']:+.2f}%**).")

# 5. Tabela Detalhada com formatação amigável
st.markdown("---")
st.subheader("📑 Visão Detalhada dos Ativos")

df_formatado = df_carteira.copy()
df_formatado["Preço Médio"] = df_formatado["Preço Médio"].map("R$ {:,.2f}".format)
df_formatado["Preço Atual"] = df_formatado["Preço Atual"].map("R$ {:,.2f}".format)
df_formatado["Valor Investido"] = df_formatado["Valor Investido"].map("R$ {:,.2f}".format)
df_formatado["Valor Atual"] = df_formatado["Valor Atual"].map("R$ {:,.2f}".format)
df_formatado["Lucro/Prejuízo R$"] = df_formatado["Lucro/Prejuízo R$"].map("R$ {:,.2f}".format)
df_formatado["Rentabilidade %"] = df_formatado["Rentabilidade %"].map("{:+.2f}%".format)

st.dataframe(df_formatado, use_container_width=True)
Use o código com cuidado.
