import streamlit as st
from dotenv import load_dotenv
from config import ESTILO_PREMIUM, inicializar_cliente_groq
from utils.helpers import obter_dica_do_turno
from services.groq_service import GroqService

# Carrega as variáveis de ambiente locais do .env
load_dotenv()

# Inicialização da UI do Streamlit
st.set_page_config(page_title="AgroAssist", page_icon="🌿", layout="centered")
st.markdown(ESTILO_PREMIUM, unsafe_allow_html=True)

# Instanciação segura da camada de serviços
try:
    cliente_groq = inicializar_cliente_groq()
    groq_service = GroqService(cliente_groq)
except ValueError as error:
    st.error(f"⚠️ {error}")
    st.stop()

st.title("🌿 AgroAssist")
st.markdown("**Seu Especialista Agrícola Inteligente**")

# Exibição do aviso dinâmico baseado nas horas
st.info(obter_dica_do_turno())

# Gerenciamento do histórico em cache (st.session_state)
prompt_sistema = """
Você é um agrônomo especialista altamente qualificado. Sua missão é ajudar agricultores. 
REGRA DE OURO: Você DEVE responder APENAS a perguntas relacionadas à agricultura, plantio, colheita, solo, pragas e clima rural. 
"""

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "system", "content": prompt_sistema}
    ]

# --- RENDERIZAÇÃO DA BARRA LATERAL (VISÃO) ---
with st.sidebar:
    st.header("📸 Análise de Plantio")
    st.markdown("Envie uma foto da sua folha, praga ou solo.")
    imagem_enviada = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    
    if imagem_enviada:
        st.image(imagem_enviada, use_container_width=True, clamp=True)
        if st.button("Analisar Imagem"):
            with st.spinner("Analisando com visão computacional..."):
                try:
                    # Executa a regra isolada no serviço correspondente
                    texto_analise = groq_service.analisar_imagem(imagem_enviada.getvalue())
                    st.success("Análise concluída!")
                    st.write(texto_analise)
                    
                    # INJEÇÃO DE CONTEXTO: Garante que o histórico capture os dados da imagem
                    contexto_imagem = f"[CONTEXTO DO SISTEMA: O agricultor enviou uma foto para análise na barra lateral. O diagnóstico de visão computacional da foto indicou: {texto_analise}]"
                    st.session_state.mensagens.append({"role": "system", "content": contexto_imagem})
                    
                except Exception as e:
                    st.error(f"Erro ao analisar a imagem: {e}")

# --- RENDERIZAÇÃO DO HISTÓRICO DE CHAT ---
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- PROCESSAMENTO ENTRADA DE DADOS (TEXTO OU VRA) ---
pergunta = None

st.markdown("---")
st.write("🎤 **Grave sua pergunta:**")
audio_gravado = st.audio_input("Fale com o assistente", label_visibility="collapsed")

if audio_gravado:
    with st.spinner("Transcrevendo o áudio..."):
        try:
            pergunta = groq_service.transcrever_audio(audio_gravado)
            st.success(f"Você disse: '{pergunta}'")
        except Exception as e:
            st.error(f"Erro ao processar o áudio: {e}")

texto_digitado = st.chat_input("Ou digite sua dúvida agrícola aqui...")
if texto_digitado:
    pergunta = texto_digitado

# --- DISPARO DOS MODELOS DE CONVERSAÇÃO ---
if pergunta:
    with st.chat_message("user"):
        st.markdown(pergunta)
    
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    
    with st.chat_message("assistant"):
        with st.spinner("Processando..."):
            try:
                texto_resposta = groq_service.enviar_mensagem_chat(st.session_state.mensagens)
                st.markdown(texto_resposta)
                st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
            except Exception as e:
                st.error(f"Erro na comunicação: {e}")