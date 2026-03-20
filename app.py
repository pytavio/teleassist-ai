import streamlit as st
from core.state import init_state
from data.defaults import PERFIS

st.set_page_config(
    page_title="TeleAssist AI",
    page_icon="📱",
    layout="wide"
)

init_state()

# Sidebar
with st.sidebar:
    st.markdown("## 📱 TeleAssist AI")
    st.markdown("---")

    pagina = st.radio(
        "Navegação",
        ["💬 Atendimento", "⚙️ Painel Admin"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Perfil do Cliente")
    perfil = st.selectbox(
        "Selecione o perfil",
        PERFIS,
        index=PERFIS.index(st.session_state.perfil_selecionado)
    )
    st.session_state.perfil_selecionado = perfil

    st.markdown("---")
    st.caption("TeleAssist AI · MBA FIAP IA Leadership")

# Roteamento de páginas
if pagina == "💬 Atendimento":
    from pages.bot import render
    render()
else:
    from pages.admin import render
    render()
