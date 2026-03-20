import streamlit as st
from core.nlp import detectar_intencao
from core.engine import selecionar_resposta, aplicar_feedback


def render():
    st.title("⚙️ Painel Administrativo")

    aba1, aba2, aba3, aba4 = st.tabs([
        "🧠 Intenções & Entidades",
        "💬 Respostas & Scores",
        "🧪 Simulador",
        "📊 Dashboard"
    ])

    # ABA 1 — INTENÇÕES
    with aba1:
        st.subheader("Intenções cadastradas")
        for i, intencao in enumerate(st.session_state.intencoes):
            with st.expander(f"{'✅' if intencao['ativo'] else '⏸️'} {intencao['nome']}"):
                ativo = st.toggle("Ativo", value=intencao["ativo"], key=f"ativo_{intencao['id']}")
                st.session_state.intencoes[i]["ativo"] = ativo
                st.text_area(
                    "Frases de treinamento (uma por linha)",
                    value="\n".join(intencao["frases"]),
                    key=f"frases_{intencao['id']}",
                    height=100
                )

        st.markdown("---")
        st.subheader("Entidades configuradas")
        for ent in st.session_state.entidades:
            st.markdown(f"**{ent['nome']}** — valores: `{', '.join(ent['valores'])}`")

    # ABA 2 — RESPOSTAS
    with aba2:
        st.subheader("Variantes de resposta por intenção")
        intencao_sel = st.selectbox(
            "Selecione a intenção",
            list(st.session_state.respostas.keys())
        )
        variantes = st.session_state.respostas.get(intencao_sel, [])
        for v in sorted(variantes, key=lambda x: x["score"], reverse=True):
            with st.expander(f"[{v['perfil'].upper()}] Score: {v['score']:.2f} — {v['texto'][:60]}..."):
                novo_texto = st.text_area("Texto da resposta", value=v["texto"], key=f"txt_{v['id']}")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("💾 Salvar", key=f"salvar_{v['id']}"):
                        v["texto"] = novo_texto
                        st.success("Salvo!")
                with col2:
                    if st.button("🔄 Reset score", key=f"reset_{v['id']}"):
                        v["score"] = 0.5
                        st.info("Score resetado para 0.5")
                st.progress(v["score"], text=f"Score atual: {v['score']:.2f}")

    # ABA 3 — SIMULADOR
    with aba3:
        st.subheader("Simulador de conversa")
        msg_sim = st.text_input("Digite uma mensagem para testar")

        if st.button("▶️ Simular") and msg_sim:
            with st.spinner("Processando..."):
                resultado = detectar_intencao(msg_sim)

            intencao_id = resultado.get("intencao_id", "fallback")
            confianca = resultado.get("confianca", 0.0)
            if confianca < 0.5:
                intencao_id = "fallback"

            variante = selecionar_resposta(intencao_id, st.session_state.perfil_selecionado, resultado.get("sentimento", "neutro"))

            st.markdown("### Resultado")
            col1, col2, col3 = st.columns(3)
            col1.metric("Intenção detectada", intencao_id)
            col2.metric("Confiança", f"{confianca:.0%}")
            col3.metric("Sentimento", resultado.get("sentimento", "neutro"))

            st.markdown(f"**Entidades:** {', '.join(resultado.get('entidades', [])) or 'nenhuma'}")
            st.markdown(f"**Perfil aplicado:** {st.session_state.perfil_selecionado}")
            st.markdown(f"**Variante selecionada:** `{variante['id']}` (score: {variante['score']:.2f})")
            st.info(f"💬 **Resposta:** {variante['texto']}")

            st.markdown("---")
            st.markdown("**Avaliar esta resposta:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 Boa resposta"):
                    aplicar_feedback(variante["id"], intencao_id, True)
                    st.success(f"Score atualizado: {variante['score']:.2f}")
            with col2:
                if st.button("👎 Resposta ruim"):
                    aplicar_feedback(variante["id"], intencao_id, False)
                    st.warning(f"Score atualizado: {variante['score']:.2f}")

    # ABA 4 — DASHBOARD
    with aba4:
        st.subheader("Métricas da sessão")
        m = st.session_state.metricas
        total = m["total_interacoes"]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de interações", total)
        col2.metric("Taxa de acerto", f"{(m['acertos']/total*100):.0f}%" if total > 0 else "—")
        col3.metric("Taxa de fallback", f"{(m['fallbacks']/total*100):.0f}%" if total > 0 else "—")

        feedbacks = m["feedbacks_positivos"] + m["feedbacks_negativos"]
        satisfacao = (m["feedbacks_positivos"] / feedbacks * 100) if feedbacks > 0 else 0
        col4.metric("Satisfação", f"{satisfacao:.0f}%" if feedbacks > 0 else "—")

        st.markdown("---")
        st.subheader("Intenções mais acionadas")
        if m["intencoes_usadas"]:
            dados = dict(sorted(m["intencoes_usadas"].items(), key=lambda x: x[1], reverse=True))
            st.bar_chart(dados)
        else:
            st.info("Nenhuma interação registrada ainda.")

        st.markdown("---")
        st.subheader("Histórico da sessão")
        historico = [
            {
                "mensagem": msg["content"][:60] + "..." if len(msg["content"]) > 60 else msg["content"],
                "papel": msg["role"],
                "intenção": msg.get("meta", {}).get("intencao_detectada", "—"),
                "score": msg.get("meta", {}).get("score_variante", "—")
            }
            for msg in st.session_state.historico_chat
            if msg["role"] == "assistant"
        ]
        if historico:
            st.dataframe(historico, use_container_width=True)
        else:
            st.info("Nenhuma conversa registrada ainda.")
