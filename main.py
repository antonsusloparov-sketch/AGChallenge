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


def dietolog():
    chat = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    # content=(f"Ты являешься бизнес-аналитиком. Спроси пользователя о том, что нужно проанализировать")
                    content=(f'Ты являешься диетологом. Спроси у пользователя его пол,'
                             'возраст, рост, массу тела и уровень физической активности.'
                             'Рассчитай для него ежесуточную норму калорий исходя из его ответа.'
                             'Выведи число калорий одним числом.')
                )
            ]
        )
    correct_answer = re.compile(r"\d+")
    i = 1
    while i:
        response = giga.chat(chat)
        answer = response.choices[0].message.content
        print('---------- Реплика диетолога: ---------------')
        print(answer)
        print("-------------------------")
        if correct_answer.match(answer):
            print('Диетолог завершил работу')
            return int(answer)
        else:
            question = input("Введите уточнения для диетолога (0 для прекращения диалога): ")
            if question == "0":
                break
            chat.messages.append(
                Messages(
                    role=MessagesRole.USER,
                    content=question
                )
            )


def nutricolog(calories):
    chat = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    # content=(f"Ты являешься бизнес-аналитиком. Спроси пользователя о том, что нужно проанализировать")
                    content=(f'Ты являешься нутрициологом. составь диету на {calories} калорий ежедневно')
                )
            ]
        )
    i = 1
    while i:
        response = giga.chat(chat)
        answer = response.choices[0].message.content
        print('---------- Реплика нутрициолога: ---------------')
        print(answer)
        print("-------------------------")
        question = input("Введите уточнения для нутрициолога (0 для прекращения диалога): ")
        if question == "0":
            break
        chat.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=question
            )
        )


n_arg = len(sys.argv)
if sys.argv[1] == "1":
    print("Задание № 1")
    i = 1
    while i:
        question = input("Спросите у GigaChat (0 для выхода из программы): ")
        if question == "0":
            break
        response = giga.chat(question)
        print("Ответ модели:")
        print(response.choices[0].message.content)
        print("-----------------------------------------------------------------")
elif sys.argv[1] == "2":
    print("Задание № 2")
    i = 1
    while i:
        question = input("Введите модель самолёта (0 для выхода из программы): ")
        if question == "0":
            break
        question = (f"Выведи информацию о самолёте {question}. Нужно вывести информацию:"
                    "Год первого полёта, Год начала эксплуатации, Единиц произведено, "
                    "Размер экипажа, число пассажиров, числом, крейсерская скорость в км/ч (без единиц измерения)."
                    "Информацию нужно вывести в виде строки для JSON-файла, без лишних символов."
                    "Нужна только строка для JSON")
        response = giga.chat(question)
        print("Ответ модели:")
        print(response.choices[0].message.content)
        print("-----------------------------------------------------------------")
elif sys.argv[1] == "3":
    print("Задание № 3")
    dietolog()
elif sys.argv[1] == "4":
    print("Задание № 4")
    calories = dietolog()
    with open("calories.txt", "w") as file:
        file.write(str(calories))
    with open("calories.txt", "r") as file:
        daily_cal = int(file.read())
    nutricolog(daily_cal)
else:
    print("Пожалуйста, укажите в качестве аргумента скрипта номер задания")