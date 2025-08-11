from gigachat import GigaChat

import credentials

giga = GigaChat(
   credentials=credentials.api_key,
)

response = giga.chat("Расскажи про себя")

print(response.choices[0].message.content)

