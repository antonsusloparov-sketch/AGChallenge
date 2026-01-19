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
День 3. Общение

- Задать ограничение модели, чтобы она сама остановилась
- Опишите в промпте результат, который модель должна собрать и выдать вам ответ

Как пример можно использовать данные для ТЗ (условно модель должна собрать требования для ТЗ и в какой-то момент переписки вернуть вам ТЗ)

Результат: Вы общаетесь и модель выдает вам какой-то результат на основе вашего общения (например, ТЗ)
Формат: Видео
'''

chat = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content=(f'Ты учитель географии. Проведи опрос ученика на знание городов России.'
                     'Для этого попроси ученика называть российские города.'
                     # 'Проводи опрос сама и проси называть города.'
                     'Он может назвать их по одному или по несколько.'
                     'Запоминай его ответы и выводи ему список названных городов и их число.'
                     'Как только он назовёт пять или более городов, напиши "больше пяти!".'
                     # 'Уточнения: Не пытайся моделировать диалог, не пиши программу для ПК.'
                     # 'Не составляй инструкцию по опросу ученика. Не строй пример/сценарий диалога с учеником.'
                     )
        )
    ]
)

print("День № 3")
print("==================================================================")
i = 0
question = 1
while question:
    response = giga.chat(chat)
    answer = response.choices[0].message.content
    print('---------- Реплика чата: ---------------')
    print(answer)
    print("-------------------------")
    if answer.find('ольше пяти')>=0:
        print('Чат завершил работу')
        break
    else:
        i = i + 1
        question = input(f"Итерация {i}. Введите свой ответ (0 для прекращения диалога): ")
        if question == "0":
            break
        chat.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=question
            )
        )
        print("==================================================================")
