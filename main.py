import sys
from gigachat import GigaChat
import credentials

if __name__ == '__main__':

    giga = GigaChat(
        credentials=credentials.api_key,
    )

    n_arg = len(sys.argv)
    print(f'Всего аргументов : {n_arg}')
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
    else:
        print("Пожалуйста, укажите в качестве аргумента скрипта номер задания")