import base64
from groq import Groq

class GroqService:
    def __init__(self, client: Groq):
        self.client = client

    def analisar_imagem(self, imagem_bytes: bytes) -> str:
        """Processa a conversão da imagem para base64 e invoca o modelo Llama Vision."""
        imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')
        resposta = self.client.chat.completions.create(
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
        return resposta.choices[0].message.content

    def transcrever_audio(self, arquivo_audio) -> str:
        """Envia o buffer de áudio do Streamlit diretamente para o modelo Whisper da Groq."""
        transcricao = self.client.audio.transcriptions.create(
            file=("audio.wav", arquivo_audio.read()),
            model="whisper-large-v3-turbo",
            language="pt",
            response_format="json"
        )
        return transcricao.text

    def enviar_mensagem_chat(self, historico_mensagens: list) -> str:
        """Consome o histórico de conversação estruturado e retorna a resposta de texto."""
        resposta = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=historico_mensagens,
            temperature=0.5
        )
        return resposta.choices[0].message.content