import json
import pprint
import sys, re
import time

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import gigachat.context
from instructor.cli.batch import results

import credentials

headers = {
    "X-Session-ID": "8324244b-7133-4d30-a328-31d8466e5511",
}

giga = GigaChat(
    credentials=credentials.api_key,
    # model="GigaChat-2"
    model="GigaChat-2-Pro"
)

gigachat.context.session_id_cvar.set(headers.get("X-Session-ID"))

'''
День 9. Сжатие диалога

Реализуйте механизм «сжатия истории диалога» (например, каждые 10 сообщений делать summary и хранить его вместо оригинала)
Проверьте, как агент продолжает вести разговор с учётом summary вместо всей истории
Сравните качество ответов и использование токенов

Результат: Агент работает с компрессией и выполняет ту же работу за меньшее количество токенов
Формат: Видео + Код
'''

sys_prompt_1 = (f'Расскажи о нововведениях Apache Superset 3.1 по сравнению с Apache Superset 3.0'
                 'Не выдумывай ничего. Основывайся на официальных Release Notes for Superset 3.1.0 с github.'
                'Выведи названия добавленных или измененных (улучшенных) графиков и технологий.'
                'Выведи результат в виде json-файла с полями: Область улучшения, Улучшение, Краткое описание улучшения,'
                'Подробное описание улучшения.'
                 # 'Запоминай его ответы и выводи ему список названных городов и их число.'
                 # 'Как только он назовёт пять или более городов, напиши "больше пяти!".'
                 )

chat = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content=(sys_prompt_1)
        )
    ],
    temperature=0
)

print("День № 8")
print("==================================================================")
result = giga.tokens_count(input_=[sys_prompt_1], model="GigaChat-2-Pro")
print(f'Токенов в системном промте: {result}')
print("==================================================================")
i = 0
question = 1
while question:
    start_time = time.perf_counter_ns()
    response = giga.chat(chat)
    end_time = time.perf_counter_ns()
    execution_time = end_time - start_time
    answer = response.choices[0].message.content
    model_usage = response.usage
    print('--- Статистика использования чата: -----')
    if question != 1 :
        result = giga.tokens_count(input_=[question], model="GigaChat-2-Pro")
        print(f'Токенов в сообщении: {result}')
    print(f'Токенов использовано: {model_usage}')
    print(f'Время исполнения: {execution_time/(10**9):.4f} c.')
    print('===================== Реплика чата: ====================')
    print(answer)
    print("-------------------------")
    i = i + 1
    question = input(f"Итерация {i}. Введите свой ответ (0 для прекращения диалога) ")
    if question == "0":
        break
    else:
        chat.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=question
            )
    )
    print("==================================================================")