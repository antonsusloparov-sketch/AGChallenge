from gigachat import GigaChat
import credentials

giga = GigaChat(
   credentials=credentials.api_key,
)

i = 1
while i:
    question = input("Спросите у GigaChat (введите ""Стоп"" для выхода из программы): ")
    if question == "Стоп":
        break
    response = giga.chat(question)
    print("Ответ модели:")
    print(response.choices[0].message.content)
    print("-----------------------------------------------------------------")