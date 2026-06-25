from datetime import datetime

def obter_dica_do_turno() -> str:
    """Calcula o horário do servidor e retorna uma dica contextualizada para o produtor."""
    hora_atual = datetime.now().hour
    
    if 5 <= hora_atual < 12:
        return "☀️ **Dica da Manhã:** O início do dia é o melhor momento para a irrigação, pois a evaporação é menor."
    elif 12 <= hora_atual < 18:
        return "🌤️ **Dica da Tarde:** Cuidado com o sol forte! Evite aplicar defensivos agrícolas agora para não queimar as folhas."
    else:
        return "🌙 **Dica da Noite:** A noite é ideal para revisar o planejamento de amanhã e verificar a umidade do solo."