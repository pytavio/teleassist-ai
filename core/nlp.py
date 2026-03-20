import os
import json
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import streamlit as st

load_dotenv()


def get_llm():
    return ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=512,
        temperature=0
    )


def detectar_intencao(mensagem: str) -> dict:
    """
    Envia a mensagem para Claude Haiku e retorna JSON com:
    - intencao_id: string com o id da intenção detectada
    - entidades: lista de entidades encontradas
    - confianca: float entre 0 e 1
    - sentimento: "positivo", "neutro" ou "negativo"
    """
    intencoes_ativas = [
        i for i in st.session_state.intencoes if i["ativo"]
    ]

    lista_intencoes = "\n".join([
        f'- {i["id"]}: exemplos: {", ".join(i["frases"][:3])}'
        for i in intencoes_ativas
    ])

    # Monta contexto com as últimas 4 mensagens do histórico
    historico = st.session_state.get("historico_chat", [])
    contexto = ""
    if historico:
        ultimas = historico[-4:]
        linhas = []
        for m in ultimas:
            papel = "Usuário" if m["role"] == "user" else "Assistente"
            linhas.append(f"{papel}: {m['content']}")
        contexto = "\n\nContexto da conversa recente:\n" + "\n".join(linhas)

    system_prompt = f"""Você é um classificador de intenções para um chatbot de telecom.
Analise a mensagem do usuário considerando o contexto da conversa e retorne APENAS um JSON válido com esta estrutura exata:
{{
  "intencao_id": "<id_da_intencao>",
  "entidades": ["<entidade1>", "<entidade2>"],
  "confianca": <float entre 0 e 1>,
  "sentimento": "<positivo|neutro|negativo>"
}}

Intenções disponíveis:
{lista_intencoes}
- fallback: use quando nenhuma intenção acima se encaixar bem

Respostas curtas como "pode", "sim", "ok", "quero", "não" devem ser classificadas com base na intenção da mensagem anterior do usuário no contexto.{contexto}

Retorne SOMENTE o JSON, sem texto adicional."""

    llm = get_llm()

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=mensagem)
        ])
        raw = response.content.strip()
        # Remove possíveis blocos markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        resultado = json.loads(raw)
        return resultado
    except Exception as e:
        st.error(f"Erro na chamada à API: {e}")
        return {
            "intencao_id": "fallback",
            "entidades": [],
            "confianca": 0.0,
            "sentimento": "neutro"
        }


def gerar_resposta(mensagem: str, intencao_id: str, perfil_display: str, sentimento: str, template: str) -> str:
    """
    Usa o LLM para gerar uma resposta personalizada com base no template,
    no perfil do cliente e no histórico da conversa.
    """
    historico = st.session_state.get("historico_chat", [])
    ultimas = historico[-6:] if len(historico) >= 6 else historico

    system_prompt = f"""Você é TeleAssist AI, atendente virtual de uma operadora de telefonia.
Perfil do cliente: {perfil_display}
Sentimento detectado: {sentimento}
Intenção identificada: {intencao_id}

Use a resposta base abaixo como guia de conteúdo, mas adapte-a naturalmente ao contexto da conversa.
Se o cliente estiver confirmando algo ("pode", "sim", "ok", "quero"), avance o diálogo com uma próxima ação concreta.
Seja conciso, empático e direto. Máximo 2-3 frases. Não repita o que acabou de ser dito.

Resposta base: {template}"""

    mensagens = [SystemMessage(content=system_prompt)]
    for m in ultimas:
        if m["role"] == "user":
            mensagens.append(HumanMessage(content=m["content"]))
        else:
            mensagens.append(AIMessage(content=m["content"]))
    mensagens.append(HumanMessage(content=mensagem))

    llm = get_llm()
    try:
        response = llm.invoke(mensagens)
        return response.content.strip()
    except Exception as e:
        st.error(f"Erro ao gerar resposta: {e}")
        return template
