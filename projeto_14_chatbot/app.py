
import os
from pathlib import Path

import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="NOVA AI | Seu assistente",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega a chave da Groq
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")

# ==========================================
# DESIGN DO SITE
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #0b0a12;
    color: #f5f3ff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(11, 10, 18, 0.9);
}

[data-testid="stSidebar"] {
    background: #100e1b;
    border-right: 1px solid #29223e;
}

.logo {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(90deg, #e9d5ff, #a78bfa, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-icon {
    color: #a78bfa;
    font-size: 32px;
}

.tagline {
    color: #928aa9;
    font-size: 12px;
    letter-spacing: 1px;
}

.hero {
    text-align: center;
    padding: 65px 10px 35px;
}

.hero-icon {
    font-size: 55px;
    color: #c4b5fd;
    text-shadow: 0 0 35px #7c3aed;
}

.hero h1 {
    font-size: clamp(30px, 4vw, 46px);
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #f5f3ff;
    margin-bottom: 12px;
}

.hero p {
    color: #aaa2c1;
    font-size: 16px;
}

.section-label {
    color: #a78bfa;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

div[data-testid="stChatMessage"] {
    background: #151321;
    border: 1px solid #2b2540;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
}

[data-testid="stChatInput"] {
    border: 1px solid #59427e;
    border-radius: 16px;
    background: #151321;
}

[data-testid="stChatInput"] textarea {
    color: #f5f3ff !important;
}

.stButton > button {
    background: #191528;
    color: #e9ddff;
    border: 1px solid #35294d;
    border-radius: 13px;
    min-height: 48px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #2a1e43;
    border-color: #a78bfa;
    color: white;
}

div[data-testid="stStatusWidget"] {
    visibility: hidden;
}

hr {
    border-color: #29223e;
}

.footer {
    text-align: center;
    color: #716984;
    font-size: 12px;
    padding: 30px 0 12px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# ESTADO DO CHAT
# ==========================================

if "conversas" not in st.session_state:
    st.session_state.conversas = {}

if "conversa_atual" not in st.session_state:
    st.session_state.conversa_atual = "Conversa 1"
    st.session_state.conversas["Conversa 1"] = []

if "contador" not in st.session_state:
    st.session_state.contador = 1

historico = st.session_state.conversas[
    st.session_state.conversa_atual
]

# ==========================================
# BARRA LATERAL
# ==========================================

with st.sidebar:
    st.markdown("""
    <div style="padding: 12px 0 20px;">
        <span class="logo-icon">✦</span>
        <span class="logo"> NOVA AI</span>
        <p class="tagline">SEU ASSISTENTE INTELIGENTE</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("＋  Nova conversa", use_container_width=True):
        st.session_state.contador += 1
        nome = f"Conversa {st.session_state.contador}"
        st.session_state.conversas[nome] = []
        st.session_state.conversa_atual = nome
        st.rerun()

    st.markdown("### 💬 Suas conversas")

    nomes = list(st.session_state.conversas.keys())

    for nome in reversed(nomes):
        if st.button(
            f"▸  {nome}",
            key=f"abrir_{nome}",
            use_container_width=True
        ):
            st.session_state.conversa_atual = nome
            st.rerun()

    st.divider()

    st.markdown("### ✨ Sobre a NOVA")

    st.caption(
        "Uma assistente de inteligência artificial "
        "para ajudar você a estudar, programar, "
        "escrever e explorar novas ideias."
    )

    st.divider()

    st.markdown("### ⚙️ Informações")
    st.caption("Modelo: GPT-OSS 120B")
    st.caption("API: Groq")
    st.caption("Interface: Streamlit")

    if st.button("🗑️ Apagar conversa atual", use_container_width=True):
        st.session_state.conversas[
            st.session_state.conversa_atual
        ] = []
        st.rerun()

    st.markdown(
        '<div class="footer">Feito com 💜 e tecnologia</div>',
        unsafe_allow_html=True
    )

# ==========================================
# TELA INICIAL
# ==========================================

if not historico:
    st.markdown("""
    <div class="hero">
        <div class="hero-icon">✦</div>
        <h1>O futuro começa com uma pergunta.</h1>
        <p>Olá! Eu sou a NOVA AI. Como posso ajudar você hoje?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">EXPLORE POSSIBILIDADES</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "💻  Aprender programação\n\n"
            "Descubra Python de um jeito simples.",
            use_container_width=True
        ):
            st.session_state.pergunta_sugerida = (
                "Me ensine Python do zero, com exemplos simples."
            )
            st.rerun()

        if st.button(
            "📚  Organizar meus estudos\n\n"
            "Monte um plano para estudar melhor.",
            use_container_width=True
        ):
            st.session_state.pergunta_sugerida = (
                "Me ajude a criar um plano de estudos organizado."
            )
            st.rerun()

    with col2:
        if st.button(
            "💡  Criar novas ideias\n\n"
            "Explore projetos criativos e interessantes.",
            use_container_width=True
        ):
            st.session_state.pergunta_sugerida = (
                "Me dê ideias criativas para projetos de tecnologia."
            )
            st.rerun()

        if st.button(
            "✍️  Escrever um texto\n\n"
            "Organize suas ideias com a ajuda da IA.",
            use_container_width=True
        ):
            st.session_state.pergunta_sugerida = (
                "Me ajude a escrever um texto claro e bem organizado."
            )
            st.rerun()

else:
    st.markdown("## ✦ Vamos continuar?")
    st.caption("Converse com a NOVA AI abaixo.")

# ==========================================
# MOSTRAR O HISTÓRICO
# ==========================================

for mensagem in historico:
    avatar = "🧑‍💻" if mensagem["role"] == "user" else "✦"

    with st.chat_message(mensagem["role"], avatar=avatar):
        st.markdown(mensagem["content"])

# ==========================================
# ENTRADA E RESPOSTA DA GROQ
# ==========================================

pergunta = st.chat_input("Escreva sua mensagem para a NOVA AI...")

if "pergunta_sugerida" in st.session_state:
    pergunta = st.session_state.pop("pergunta_sugerida")

if pergunta:
    if not API_KEY:
        st.error(
            "Não encontrei a chave da Groq. "
            "Confira o arquivo .env na pasta do projeto."
        )
        st.stop()

    historico.append({
        "role": "user",
        "content": pergunta
    })

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(pergunta)

    with st.chat_message("assistant", avatar="✦"):
        try:
            with st.spinner("A NOVA está preparando sua resposta..."):
                cliente = Groq(api_key=API_KEY)

                resposta = cliente.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é a NOVA AI, uma assistente "
                                "inteligente, simpática e prestativa. "
                                "Responda em português, seja clara "
                                "e use exemplos quando forem úteis."
                            )
                        },
                        *historico
                    ],
                    temperature=0.7
                )

                texto = resposta.choices[0].message.content

                if not texto:
                    texto = "Não recebi uma resposta. Tente novamente."

            st.markdown(texto)

            historico.append({
                "role": "assistant",
                "content": texto
            })

        except Exception as erro:
            historico.pop()
            st.error(
                "Não consegui me conectar à Groq. "
                "Confira sua chave, sua conexão e o modelo configurado."
            )
            st.caption(f"Detalhe técnico: {erro}")

# ==========================================
# RODAPÉ
# ==========================================

st.markdown("""
<div class="footer">
    NOVA AI · Inteligência, criatividade e possibilidades.
</div>
""", unsafe_allow_html=True)
