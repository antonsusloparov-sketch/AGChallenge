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
    model="GigaChat-2"
    # model="GigaChat-2-Pro"

)

gigachat.context.session_id_cvar.set(headers.get("X-Session-ID"))

'''
День 6. Температура

Запустите один и тот же запрос с температурой = 0, 0.7 и 1.2

- Сравните результаты (точность, креативность, разнообразие)
- Сформулируйте, для каких задач лучше подходит каждая настройка

Результат: Текст или код с примерами разных ответов
Формат: Видео + Код

P.S. Начинается вторая неделя, поэтому к этому заданию прикрепляется дополнительное - посмотреть видео (дублирую ссылкой - https://disk.yandex.ru/i/fo9M-T6zzGX05A)
Если будут вопросы - пишите в чаты
'''

sys_prompt_1 = (f'Нужно ли устанавливать CUDA Toolkit от NVIDIA, на Windows, '
                'чтобы ML Studio или Jan увидели GPU и запускали модели на GPU? Или достаточно установить обычные драйвера?'
                'Сообщай только ответ на вопрос, без теории.'
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
    question = input(f"Итерация {i}. Введите свой ответ (0 для прекращения диалога, величина > 0 - задание температуры * 10): ")
    if question == "0":
        break
    elif question == re.compile(r"\d+"):
        chat.temperature = int(question)/10
    else:
        chat.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=question
            )
    )
    print("==================================================================")
