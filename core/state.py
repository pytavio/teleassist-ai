import copy
import streamlit as st
from data.defaults import DEFAULT_INTENCOES, DEFAULT_ENTIDADES, DEFAULT_RESPOSTAS, PERFIS


def init_state():
    if "iniciado" not in st.session_state:
        st.session_state.iniciado = True
        st.session_state.intencoes = copy.deepcopy(DEFAULT_INTENCOES)
        st.session_state.entidades = copy.deepcopy(DEFAULT_ENTIDADES)
        st.session_state.respostas = copy.deepcopy(DEFAULT_RESPOSTAS)
        st.session_state.historico_chat = []
        st.session_state.metricas = {
            "total_interacoes": 0,
            "acertos": 0,
            "fallbacks": 0,
            "feedbacks_positivos": 0,
            "feedbacks_negativos": 0,
            "intencoes_usadas": {}
        }
        st.session_state.perfil_selecionado = PERFIS[0]
        st.session_state.ultima_variante_id = None
        st.session_state.ultima_intencao_id = None
