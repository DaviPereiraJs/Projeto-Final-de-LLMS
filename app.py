import streamlit as st
import os
import base64
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env para a memória
load_dotenv()

# ==========================================
# 1. CONFIGURAÇÃO INICIAL E API
# ==========================================
# Puxa a chave do arquivo .env de forma segura
chave_api = os.getenv("GROQ_API_KEY")

# Proteção caso o .env não seja lido corretamente
if not chave_api:
    st.error("⚠️ Chave da API não encontrada. Verifique se o seu arquivo .env está na mesma pasta do projeto e configurado corretamente.")

# Inicializa o cliente do Groq com a chave
client = Groq(api_key=chave_api)

# Configuração da página do Streamlit
st.set_page_config(page_title="AgroAssist", page_icon="🚜", layout="centered")
st.title("🚜 AgroAssist - Seu Especialista Agrícola")

# ==========================================
# 2. LÓGICA DE DICAS POR HORÁRIO
# ==========================================
def obter_dica_do_turno():
    """Retorna uma dica baseada no horário atual."""
    hora_atual = datetime.now().hour
    
    if 5 <= hora_atual < 12:
        return "☀️ **Dica da Manhã:** O início do dia é o melhor momento para a irrigação, pois a evaporação é menor. Boa colheita!"
    elif 12 <= hora_atual < 18:
        return "🌤️ **Dica da Tarde:** Cuidado com o sol forte! Evite aplicar defensivos agrícolas agora para não queimar as folhas."
    else:
        return "🌙 **Dica da Noite:** A noite é ideal para revisar o planejamento de amanhã e verificar a umidade do solo."

# Exibe a dica na tela logo abaixo do título
st.info(obter_dica_do_turno())

# ==========================================
# 3. MEMÓRIA DO CHAT (SESSION STATE)
# ==========================================
# O System Prompt garante que ele só fale de agricultura
prompt_sistema = """
Você é um agrônomo especialista altamente qualificado. 
Sua missão é ajudar agricultores. 
REGRA DE OURO: Você DEVE responder APENAS a perguntas relacionadas à agricultura, plantio, colheita, solo, pragas e clima rural. 
Se o usuário perguntar sobre esportes, tecnologia, política ou qualquer outro assunto, recuse educadamente e lembre-o de que você é um especialista agrícola.
"""

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {"role": "system", "content": prompt_sistema}
    ]

# ==========================================
# 4. ANÁLISE DE IMAGEM (BARRA LATERAL)
# ==========================================
with st.sidebar:
    st.header("📸 Análise de Plantio")
    st.write("Envie uma foto da sua folha, praga ou solo para análise.")
    imagem_enviada = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    
    if imagem_enviada:
        st.image(imagem_enviada, caption="Imagem carregada", use_container_width=True)
        if st.button("Analisar Imagem"):
            with st.spinner("Analisando..."):
                # Converte a imagem para o formato que a IA entende (Base64)
                imagem_base64 = base64.b64encode(imagem_enviada.getvalue()).decode('utf-8')
                
                try:
                    # Chamada para o modelo de visão do Groq (Llama 3.2 Vision)
                    resposta_visao = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Atue como um agrônomo. Analise esta imagem e identifique possíveis doenças, pragas ou a condição visível da planta/solo. Seja direto e dê recomendações."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagem_base64}"}}
                                ]
                            }
                        ],
                        temperature=0.2
                    )
                    st.success("Análise concluída!")
                    st.write(resposta_visao.choices[0].message.content)
                except Exception as e:
                    st.error(f"Erro ao analisar a imagem: {e}")

# ==========================================
# 5. INTERFACE DO CHATBOT PRINCIPAL
# ==========================================
# Exibe o histórico de mensagens (escondendo o system prompt do usuário)
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Caixa de texto para o usuário digitar
pergunta = st.chat_input("Digite sua dúvida agrícola aqui...")

if pergunta:
    # 1. Mostra a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(pergunta)
    
    # 2. Salva na memória
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    
    # 3. Envia para a IA gerar a resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                resposta = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.mensagens,
                    temperature=0.5
                )
                texto_resposta = resposta.choices[0].message.content
                st.markdown(texto_resposta)
                
                # 4. Salva a resposta da IA na memória
                st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})
            except Exception as e:
                st.error(f"Erro na comunicação: {e}")