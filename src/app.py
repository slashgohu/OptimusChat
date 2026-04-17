# imports
import json
import pandas as pd
import requests
import streamlit as st

# config ollama
ollama_url = "http://localhost:11434/api/generate"
modelo = "gpt-oss"

# carregar dados
perfil = json.load(open('data/perfil_investidor.json'))
produtos = json.load(open('data/produtos_financeiros.json'))
transacoes = pd.read_csv('data/transacoes.csv')
historico = pd.read_csv('data/historico_atendimento.csv')

# contexto
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# system prompt
system_prompt = """Você é o Optimus, um agente financeiro com anos de experiência no mercado e bem didático. Com o objetivo de ensinar sobre conceitos de finanças para o usuário final.

REGRAS:
- NUNCA recomende investimentos específicos, apenas os explique;
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais. Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos pelo usuário para exemplos personalizados;
- Seja didático e amigável, use uma linguagem mais simples, sempre pergunte se o usuário entendeu sua explicação;
- Se não souber algo, ADMITA;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos;
"""

# ollama
def perguntar(msg):
    prompt = f"""
    {system_prompt}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(ollama_url, json={"model": modelo, "prompt": prompt, "stream": False})
    return r.json()['response']

# interface
st.title("🎓 Optimus, seu Otimizador Financeiro")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))