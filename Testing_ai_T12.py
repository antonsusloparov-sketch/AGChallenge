import sys, re, os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import gigachat.context
import credentials

headers = {
    "X-Session-ID": "8324244b-7133-4d30-a328-31d8466e5502",
}

giga = GigaChat(
    credentials=os.environ.get("GIGACHAT_CREDENTIALS"),
)

gigachat.context.session_id_cvar.set(headers.get("X-Session-ID"))

print(os.environ.get("GIGACHAT_CREDENTIALS"))
i = 1
while i:
    question = input("Спросите у GigaChat (0 для выхода из программы): ")
    if question == "0":
        break
    response = giga.chat(question)
    print("Ответ модели:")
    print(response.choices[0].message.content)
    print("-----------------------------------------------------------------")