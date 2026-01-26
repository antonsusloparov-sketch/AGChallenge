from __future__ import annotations
import json
import os
import pprint
import sys, re
import time

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import gigachat.context
from instructor.cli.batch import results
from yandex_cloud_ml_sdk import YCloudML

import credentials

sdk = YCloudML(
    folder_id=credentials.YC_FOLDER,
    auth=credentials.YC_API_KEY,
)

'''
День 9. Сжатие диалога

Реализуйте механизм «сжатия истории диалога» (например, каждые 10 сообщений делать summary и хранить его вместо оригинала)
Проверьте, как агент продолжает вести разговор с учётом summary вместо всей истории
Сравните качество ответов и использование токенов

Результат: Агент работает с компрессией и выполняет ту же работу за меньшее количество токенов
Формат: Видео + Код
'''

stocks_data = "Data\\TQBR.LKOH_M60.txt"

sys_prompt_1 = (f'Напиши программу на языке Python версии не более 3.12, которая '
                f'берет данные о котировках ценной бумаги из файла {stocks_data}, '
                f'помещает их в Pandas dataframe, используя поле datetime в качестве ключа, '
                f'формат даты-времени: "%d.%m.%Y %H:%M" , '
                f'столбцы данных отделены друг от друга символами табуляции. '
                f'в качестве десятичного разделителя используется точка. '
                f'На основе загруженных данных программа должна построить свечной график в mplfinance'
                # 'Выведи результат в виде json-файла с полями: Область улучшения, Улучшение, Краткое описание улучшения,'
                # 'Подробное описание улучшения.'
                 )

'''
# Пример корректного результата
import pandas as pd
import mplfinance as mpf

# Чтение данных из файла в DataFrame
df = pd.read_csv('Data/TQBR.LKOH_M60.txt', delimiter='\t',
                 parse_dates=['datetime'],
                 date_parser=lambda x: pd.to_datetime(x, format='%d.%m.%Y %H:%M'))

# Установим столбец datetime как индекс
df.set_index('datetime', inplace=True)

# Построение свечного графика
mpf.plot(df, type='candle', style='charles',
         title='LKOH Stock Price',
         ylabel='Price',
         figscale=1.5)
'''


messages=[
    {
        "role" : "system",
        "text" : sys_prompt_1,
    },
]

# model_uri = "aliceai-llm"
# model_uri = "yandexgpt/rc"
model_uri = "yandexgpt"
# model_uri = "yandexgpt/latest"
model = sdk.models.completions(f"gpt://{credentials.YC_FOLDER}/{model_uri}")
model = model.configure(temperature=1)

print("День № 9")
print("==================================================================")
i = 0
question = 1
while question:
    start_time = time.perf_counter_ns()
    if question != "1":
        operation = model.run_deferred(messages)
        result = operation.wait()
        # result = model.run(messages)
        end_time = time.perf_counter_ns()
        execution_time = end_time - start_time
        answer = result.alternatives[0].text
        answer_status = result.alternatives[0].status
        model_usage = result.usage
        print('--- Статистика использования чата: -----')
        print(f'Токенов использовано: {model_usage}')
        print(f'Время исполнения: {execution_time/(10**9):.4f} c.')
        print('================== Статус ответа чата: =================')
        print(f'Статус результата: {result.status}, статус ответа: {answer_status}')
        print('====================== Ответ чата: =====================')
        print(answer)
        print("-------------------------")
    i = i + 1
    question = input(f"Итерация {i}. Введите свой ответ (0 для прекращения диалога, 1 - для сворачивания контекста) ")
    if question == "0":
        break
    elif question == "1":
        del messages[1:len(messages)-1]
        print(f"История чата очищена")
        print("==================================================================")
    elif question != "0" and question != "1" and question != "":
        messages.append(
            {
                "role": "user",
                "text": question,
            }
            )
        print(f'В messages {len(messages)} сообщений')
    print("==================================================================")