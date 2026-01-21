import json
import pprint
import sys, re, time
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
    # model="GigaChat-2-Pro"
    model="GigaChat-2-Max"
)

gigachat.context.session_id_cvar.set(headers.get("X-Session-ID"))

'''
День 7. Версии моделей

- Вызовите один и тот же запрос на двух разных моделях (из начала, середины и конца списка HuggingFace)
- Замерьте время ответа, количество токенов и итоговую стоимость (если модель платная)
- Сравните качество ответов

Результат: Короткий вывод и ссылки
Формат: Видео + Код
'''

sys_prompt_1 = (f'Имеется таблица с котировками ценной бумаги, созданная скриптом:'

                'CREATE TABLE raw.tqbr_sber_d1_fnm_api ('
                '	datetime timestamp NOT NULL,'
                '	opn float4 NOT NULL,'
                '	hgh float4 NOT NULL,'
                '	low float4 NOT NULL,'
                '	cls float4 NOT NULL,'
                '	volume float8 NOT NULL,'
                '	load_date timestamptz NOT NULL,'
                '	CONSTRAINT tqbr_sber_d1_fnm_api_pk PRIMARY KEY (datetime)'
	
                'Напиши SQL-функцию для PostgreSQL,'
                'считающую экспоненциальное скользящее среднее по ценам закрытия'
                '(поле cls) с коэффициентом alfa = 1/10.'
                'Используй оконные функции SQL'

                'Приведи пример её использования (вызова).'
                )

chat = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content=sys_prompt_1
        )
    ],
    temperature= 1
)

print("День № 7")
print("==================================================================")
i = 0
question = 1
while question:
    start_time = time.perf_counter_ns()
    response = giga.chat(chat)
    end_time = time.perf_counter_ns()
    execution_time = end_time - start_time
    answer = response.choices[0].message.content
    print('---------- Реплика чата: ---------------')
    print(answer)
    print("-------------------------")
    i = i + 1
    question = input(f"Итерация {i}. Время исполнения: {execution_time/(10**9):.4f} c. "
                     f"Введите свой ответ (0 для прекращения диалога) ")
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
