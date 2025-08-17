import asyncio
from datetime import datetime, timezone, timedelta, UTC
import os
import credentials

from dotenv import find_dotenv, load_dotenv
from langchain_gigachat.chat_models.gigachat import GigaChat
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich import print as rprint

from gigachat import GigaChat as GC
from gigachat.models import Chat, Messages, MessagesRole
import gigachat.context

load_dotenv(find_dotenv())

headers = {
    "X-Session-ID": "8324244b-7133-4d30-a328-31d8466e5502",
}
# Инициализация GigaChat
model = GigaChat(streaming=False,
                 max_tokens=8000,
                 timeout=600,
                 credentials=credentials.api_key)

messages_count = 10 # Желаемое число сообщений для анализа
mcp_response = ''

giga = GC(
    credentials=credentials.api_key,
)

def chatAnalysis(messages):
    chat = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    # content=(f"Ты являешься бизнес-аналитиком. Спроси пользователя о том, что нужно проанализировать")
                    content=(f'Тебе передали список сообщений из чата в Telegram. '
                             f'О каждом сообщении передана следующая информация: '
                             f'Номер (ID) сообщения, Автор сообщения, Дата и время отправки,'
                             f'номер сообщения, ответом на которое является данное (если является ответом),'
                             f'сам текст сообщения после слова Message. Разделителем полей является |.'
                             f'Тебе нужно проанализировать сообщения.'
                             f'Сам список сообщений: /n {messages}'
                             )
                )
            ]
        )
    response = giga.chat(chat)
    answer = response.choices[0].message.content
    print('---------- Результат анализа модели: ---------------')
    print(answer)
    dt_format = '%Y-%m-%d %H-%M'
    now_utc = datetime.now()
    with open(f"report {now_utc:{dt_format}}.md", "w") as file:
        file.write(answer)


def _log(ans):
    for message in ans['messages']:
        rprint(f"[{type(message).__name__}] {message.content} {getattr(message, 'tool_calls', '')}")


async def ask_mcp():
    server_params = StdioServerParameters(
        command="uv",
        args=["--directory", "C:\\PythonProjects\\telegram-mcp", "run", "main.py"
      ],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Инициализация соединения с сервером
            await session.initialize()
            print('Сессия инициализирована')

            # Загрузка функций с сервера
            tools = await load_mcp_tools(session)
            print('Функции сервера загружены')

            # Создание и запуск агента
            agent = create_react_agent(model, tools)
            print('Агент создан и запущен')

            #Первый вопрос: запрос списка чатов
            question = "get_chats"
            print(f'Запрос в модель: {question}')
            agent_response = await agent.ainvoke({"messages": [
                {"role": "user", "content": question}]})
            print("-------------- Ответ модели: --------------")
            for message in agent_response['messages']:
                if type(message).__name__ == "ToolMessage":
                    mcp_response = message.content
                    # print(f"Получен ответ MCP-сервера: \n {message.content} {getattr(message, 'tool_calls', '')}")
            print("-----------------------------------------------------------------")
            #Второй вопрос: запрос списка чатов
            messages_in_response = 0
            question = f"выведи {messages_count} последних сообщений из канала 2893074941"
            print(f'Запрос в модель: {question}')
            agent_response = await agent.ainvoke({"messages": [
                {"role": "user", "content": question}]})
            print("-------------- Ответ модели: --------------")
            for message in agent_response['messages']:
                if type(message).__name__ == "ToolMessage":
                    mcp_response = message.content
                    messages_in_response = mcp_response.count("ID")
                    # print(f"Получен ответ MCP-сервера: \n {message.content} {getattr(message, 'tool_calls', '')}")
            print("-----------------------------------------------------------------")
            print(f'Получено {messages_in_response} последних сообщений. Работа с MCP прекращена.')
            return mcp_response

# Запуск функции ask mcp
mcp_response = asyncio.run(ask_mcp())
print("----------- Начинаем анализ сообщений ------------")

chatAnalysis(mcp_response)