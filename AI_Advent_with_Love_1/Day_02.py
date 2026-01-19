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
)

gigachat.context.session_id_cvar.set(headers.get("X-Session-ID"))

'''
Привет, ангелы. Сегодня задание такое

- Научиться задавать формат результата для возвращения
- Задайте агенту формат возвращения в prompt
- Приведите пример формата возврата

Результат: Ответ от LLM можно распарсить
Формат: Код + Видео
'''
print("День № 2")
print("==================================================================")
i = 0
question = 1
while question:
    i = i + 1
    question = input(f"Итерация {i}. Введите модель самолёта (0 для выхода из программы): ")
    if question == "0":
        break
    question = (f"Выведи информацию о самолёте {question}. Нужно вывести информацию:"
                "Год первого полёта, Год начала эксплуатации, Единиц произведено, "
                "Размер экипажа, число пассажиров, числом, крейсерская скорость в км/ч (без единиц измерения)."
                "Информацию нужно вывести в виде строки для JSON-файла, без лишних символов."
                "Нужна только строка для JSON")
    response = giga.chat(question)

    answer = response.choices[0].message.content
    print('-----------------------------------------------------------------')
    print("Ответ модели:")
    print(answer)
    print('-----------------------------------------------------------------')
    f_answer = answer.replace('\\"', '"')
    f_answer = f_answer.replace('`"', '').replace('"`', '')
    print("Форматированный JSON:")
    data = json.loads(f_answer)
    pprint.pprint(data)
    print("==================================================================")
