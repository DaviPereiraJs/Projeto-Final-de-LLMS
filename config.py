import os
from groq import Groq

# Interface minimalista inspirada no Gemini/Claude (Matte Dark Mode)
# Interface Minimalista Cinza Chumbo (Estilo ChatGPT / Claude)
ESTILO_PREMIUM = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Fundo Principal - Cinza Matte Escuro (Totalmente sem azul) */
.stApp, .main, [data-testid="stHeader"] {
    background-color: #212121 !important; 
    color: #ECECEC !important;
}

/* Sidebar - Cinza ainda mais profundo para dar contraste */
[data-testid="stSidebar"] {
    background-color: #171717 !important;
    border-right: 1px solid #2F2F2F !important;
}

/* Oculta os balões das mensagens para o texto flutuar livremente */
.stChatMessage {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 1rem 0 !important;
}

/* Caixa de digitação (Chat Input) estilo pílula */
.stChatInput>div {
    background-color: #2F2F2F !important;
    border: 1px solid #404040 !important;
    border-radius: 24px !important;
    padding: 4px 12px;
}
/* Quando o usuário clica para digitar, a borda fica verde agro sutil */
.stChatInput>div:focus-within {
    border-color: #10B981 !important; 
}

/* Área de Upload de Imagem */
[data-testid="stFileUploader"] {
    background-color: #212121 !important;
    border: 1px dashed #404040 !important;
    border-radius: 12px;
}

/* Botões Cinza Fosco */
.stButton>button {
    background-color: #2F2F2F !important;
    color: #ECECEC !important;
    border: 1px solid #404040 !important;
    border-radius: 8px;
    font-weight: 500;
}
.stButton>button:hover {
    background-color: #404040 !important;
    border-color: #10B981 !important;
    color: #10B981 !important;
}

/* Caixa de Dica (Alert) minimalista com detalhe verde */
.stAlert {
    background-color: #2F2F2F !important;
    border: none !important;
    border-left: 4px solid #10B981 !important; /* Apenas uma linha lateral verde */
    color: #ECECEC !important;
    border-radius: 4px !important;
}

/* Força os textos a ficarem cinza claro/branco */
h1, h2, h3, p, span {
    color: #ECECEC !important;
}

/* Título principal sem gradientes pesados */
h1 {
    font-weight: 600 !important;
}
</style>
"""

def inicializar_cliente_groq() -> Groq:
    """Verifica as credenciais do arquivo .env e instancia a conexão."""
    chave_api = os.getenv("GROQ_API_KEY")
    if not chave_api:
        raise ValueError("Chave da API não encontrada. Verifique o seu arquivo .env.")
    return Groq(api_key=chave_api)