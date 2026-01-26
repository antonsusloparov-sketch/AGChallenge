from __future__ import annotations
import json
import os
import pprint
import sys, re
import time
import openai

import credentials


'''
День 9. Сжатие диалога

Реализуйте механизм «сжатия истории диалога» (например, каждые 10 сообщений делать summary и хранить его вместо оригинала)
Проверьте, как агент продолжает вести разговор с учётом summary вместо всей истории
Сравните качество ответов и использование токенов

Результат: Агент работает с компрессией и выполняет ту же работу за меньшее количество токенов
Формат: Видео + Код
'''

sys_prompt_1 = (f'Расскажи о нововведениях Apache Superset 3.1 по сравнению с Apache Superset 3.0'
                 'Не выдумывай ничего. Основывайся на официальных release-notes-3-1 с github.'
                 'Какие новые визуализации были добавлены? Подумай.'
                 # 'Запоминай его ответы и выводи ему список названных городов и их число.'
                 # 'Как только он назовёт пять или более городов, напиши "больше пяти!".'
                 )


messages=[
    {
        "role" : "system",
        "text" : sys_prompt_1,
    },
]

# model_uri = "aliceai-llm"
# model_uri = "yandexgpt/rc"
# model_uri = "qwen3-235b-a22b-fp8/latest"
model_uri = "gemma-3-27b-it/latest"
# model_uri = "yandexgpt/latest"
client = openai.OpenAI(
    api_key=credentials.YC_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=credentials.YC_FOLDER
)

print("День № 9")
print("==================================================================")
# result = giga.tokens_count(input_=[sys_prompt_1], model="GigaChat-2-Pro")
# print(f'Токенов в системном промте: {result}')
print("==================================================================")
i = 0
question = 1
while question:
    start_time = time.perf_counter_ns()
    response = client.responses.create(
        model=f"gpt://{credentials.YC_FOLDER}/{model_uri}",
        input=sys_prompt_1,
        temperature=0,
        max_output_tokens=1500
    )
    result = response.output[0].content[0]

    end_time = time.perf_counter_ns()
    execution_time = end_time - start_time
    answer = result.text
    # answer_status = result.`.alternatives[0].status
    # model_usage = result.usage
    # print('--- Статистика использования чата: -----')
    # print(f'Токенов использовано: {model_usage}')
    print(f'Время исполнения: {execution_time/(10**9):.4f} c.')
    print('================== Статус ответа чата: =================')
    print(f'Статус результата: {result.type}')
    print('====================== Ответ чата: =====================')
    print(answer)
    print("-------------------------")
    i = i + 1
    question = input(f"Итерация {i}. Введите свой ответ (0 для прекращения диалога) ")
    if question == "0":
        break
    else:
        messages.append(
            {
                "role": "user",
                "text": question,
            }
            )
    print("==================================================================")