import random
import streamlit as st
from data.defaults import PERFIL_MAP


def selecionar_resposta(intencao_id: str, perfil_display: str, sentimento: str) -> dict:
    """
    Seleciona a melhor variante de resposta para a combinação
    de intenção + perfil + sentimento.
    Retorna o dict da variante selecionada.
    """
    perfil_key = PERFIL_MAP.get(perfil_display, "generico")

    # Sentimento negativo força perfil insatisfeito independente do perfil base
    if sentimento == "negativo" and perfil_key not in ["inadimplente", "churn"]:
        perfil_key = "insatisfeito"

    variantes = st.session_state.respostas.get(intencao_id, [])

    if not variantes:
        variantes = st.session_state.respostas.get("fallback", [])

    # Tenta encontrar variante específica para o perfil
    especificas = [v for v in variantes if v["perfil"] == perfil_key]
    genericas = [v for v in variantes if v["perfil"] == "generico"]

    candidatas = especificas if especificas else genericas
    if not candidatas:
        candidatas = variantes

    # Seleciona por maior score; em empate, escolhe aleatoriamente
    score_max = max(v["score"] for v in candidatas)
    melhores = [v for v in candidatas if v["score"] == score_max]
    return random.choice(melhores)


def aplicar_feedback(variante_id: str, intencao_id: str, positivo: bool):
    """
    Atualiza o score da variante com base no feedback.
    """
    variantes = st.session_state.respostas.get(intencao_id, [])
    for v in variantes:
        if v["id"] == variante_id:
            delta = 0.1 if positivo else -0.1
            v["score"] = round(min(1.0, max(0.0, v["score"] + delta)), 2)
            break

    # Atualiza métricas
    if positivo:
        st.session_state.metricas["feedbacks_positivos"] += 1
    else:
        st.session_state.metricas["feedbacks_negativos"] += 1
