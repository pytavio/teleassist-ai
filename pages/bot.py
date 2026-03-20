import streamlit as st
from core.nlp import detectar_intencao, gerar_resposta
from core.engine import selecionar_resposta, aplicar_feedback


def render():
    st.title("💬 TeleAssist AI")
    st.caption(f"Atendendo como perfil: **{st.session_state.perfil_selecionado}**")

    # Determina id da última mensagem do assistente (para exibir feedback só nela)
    msgs_assistente = [m for m in st.session_state.historico_chat if m["role"] == "assistant"]
    ultima_id = msgs_assistente[-1]["id"] if msgs_assistente else None

    # Exibe histórico do chat
    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("meta"):
                with st.expander("🔍 Detalhes do processamento", expanded=False):
                    st.json(msg["meta"])
            # Feedback apenas na última mensagem do assistente
            if (
                msg.get("aguarda_feedback")
                and not msg.get("feedback_dado")
                and msg["id"] == ultima_id
            ):
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("👍 Útil", key=f"pos_{msg['id']}"):
                        aplicar_feedback(msg["variante_id"], msg["intencao_id"], True)
                        msg["feedback_dado"] = True
                        st.rerun()
                with col2:
                    if st.button("👎 Não ajudou", key=f"neg_{msg['id']}"):
                        aplicar_feedback(msg["variante_id"], msg["intencao_id"], False)
                        msg["feedback_dado"] = True
                        st.rerun()

    # Input do usuário
    user_input = st.chat_input("Digite sua dúvida...")

    if user_input:
        st.session_state.historico_chat.append({
            "role": "user",
            "content": user_input,
            "id": len(st.session_state.historico_chat)
        })

        with st.spinner("TeleAssist AI está processando..."):
            resultado_nlp = detectar_intencao(user_input)

        intencao_id = resultado_nlp.get("intencao_id", "fallback")
        confianca = resultado_nlp.get("confianca", 0.0)
        sentimento = resultado_nlp.get("sentimento", "neutro")
        entidades = resultado_nlp.get("entidades", [])

        if confianca < 0.5:
            intencao_id = "fallback"

        # Seleciona o template base
        variante = selecionar_resposta(
            intencao_id,
            st.session_state.perfil_selecionado,
            sentimento
        )

        # Gera resposta personalizada com LLM
        with st.spinner("Gerando resposta personalizada..."):
            texto_final = gerar_resposta(
                user_input,
                intencao_id,
                st.session_state.perfil_selecionado,
                sentimento,
                variante["texto"]
            )

        # Atualiza métricas
        st.session_state.metricas["total_interacoes"] += 1
        if intencao_id == "fallback":
            st.session_state.metricas["fallbacks"] += 1
        else:
            st.session_state.metricas["acertos"] += 1
            usado = st.session_state.metricas["intencoes_usadas"]
            usado[intencao_id] = usado.get(intencao_id, 0) + 1

        msg_id = len(st.session_state.historico_chat)
        st.session_state.historico_chat.append({
            "role": "assistant",
            "content": texto_final,
            "id": msg_id,
            "variante_id": variante["id"],
            "intencao_id": intencao_id,
            "aguarda_feedback": True,
            "feedback_dado": False,
            "meta": {
                "intencao_detectada": intencao_id,
                "confianca": confianca,
                "sentimento": sentimento,
                "entidades": entidades,
                "perfil_aplicado": st.session_state.perfil_selecionado,
                "variante_id": variante["id"],
                "score_variante": variante["score"],
                "template_base": variante["texto"]
            }
        })

        st.rerun()
