import json
import pprint
import sys, re
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import gigachat.context
import credentials

headers = {
    "X-Session-ID": "8324244b-7133-4d30-a328-31d8466e5502",
}

giga = GigaChat(
    credentials=credentials.api_key,
    # model="GigaChat-2"
    model="GigaChat-2-Pro"
)

gigachat.context.session_id_cvar.set(headers.get("X-Session-ID"))

'''
День 5. System Prompt

- Задайте агенту systemPrompt и сделайте несколько шагов в диалоге с агентом
- В ходе работы поменяйте systemPrompt и продолжите диалог 

Сравните как меняется реакция агента с изменением systemPrompt

Результат: Сделайте выводы и запишите в таблицу
Формат: Видео
'''

sys_prompt_1 = (f'Ты учитель географии. Проведи опрос ученика на знание городов России. '
                     'Для этого попроси ученика называть российские города. '
                     'Он может назвать их по одному или по несколько. '
                     'Запоминай его ответы и выводи ему список названных городов и их число.'
                     )

sys_prompt_2 = (f'Ты учитель географии. Проведи опрос ученика на знание городов США.'
                     'Для этого попроси ученика называть города Соединённых Штатов Америки. '
                     'Он может назвать их по одному или по несколько.'
                     'Запоминай его ответы и выводи ему список названных городов и их число.'
                     )

chat = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content=sys_prompt_1
        )
    ]
)

print("День № 5")
print("==================================================================")
i = 0
question = 1
while question:
    response = giga.chat(chat)
    answer = response.choices[0].message.content
    print('---------- Реплика чата: ---------------')
    print(answer)
    print("-------------------------")
    i = i + 1
    question = input(f"Итерация {i}. Введите свой ответ (0 для прекращения диалога, 1 для смены страны на США): ")
    if question == "0":
        break
    elif question == "1":
        chat.messages[0].content = sys_prompt_2
    chat.messages.append(
        Messages(
            role=MessagesRole.USER,
            content=question
        )
    )
    print("==================================================================")
