import asyncio
import os
import credentials

from dotenv import find_dotenv, load_dotenv
from langchain_gigachat.chat_models.gigachat import GigaChat
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rich import print as rprint

load_dotenv(find_dotenv())

# Инициализация GigaChat
model = GigaChat(streaming=False,
                 max_tokens=8000,
                 timeout=600,
                 credentials=credentials.api_key)


def _log(ans):
    for message in ans['messages']:
        rprint(f"[{type(message).__name__}] {message.content} {getattr(message, 'tool_calls', '')}")


async def main():
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

            i = 1
            while i:
                question = input("Спросите про TG (0 для выхода): ")
                if question == "0":
                    break
                agent_response = await agent.ainvoke({"messages": [
                    {"role": "user", "content": question}]})
                print("Ответ модели:")
                _log(agent_response)
                print("-----------------------------------------------------------------")

# Запуск функции main
asyncio.run(main())