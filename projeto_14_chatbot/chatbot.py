from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "Chave da Groq não encontrada. Confira o arquivo .env."
    )

client = Groq(api_key=API_KEY)

# CHATBOT
print("=" * 50)
print("🤖 Chatbot Groq")
print("Digite 'sair' para encerrar.")
print("=" * 50)

historico = []

while True:

    pergunta = input("\nVocê: ")

    if pergunta.lower() == "sair":
        print("\n🤖: Até logo.")
        break

    # Guarda a mensagem do usuário
    historico.append({
        "role": "user",
        "content": pergunta
    })

    # Resposta da Groq
    resposta = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=historico
    )

    texto = resposta.choices[0].message.content

    # Guarda a resposta do assistente
    historico.append({
        "role": "assistant",
        "content": texto
    })

    print(f"\n🤖: {texto}")
