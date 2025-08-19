#!/usr/bin/python3

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
chanels_data=''

# Инициализация GigaChat
model = GigaChat(streaming=False,
                 max_tokens=8000,
                 timeout=600,
                 credentials=credentials.api_key)


def _log(ans):
    for message in ans['messages']:
        rprint(f"[{type(message).__name__}] {message.content} {getattr(message, 'tool_calls', '')}")


async def ask_telegram_mcp():
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
            print(f'Запрос в Telegram: {question}')
            agent_response = await agent.ainvoke({"messages": [
                {"role": "user", "content": question}]})
            # print("-------------- Ответ модели: --------------")
            for message in agent_response['messages']:
                if type(message).__name__ == "ToolMessage":
                    mcp_response = message.content
                    # print(f"Получен ответ MCP-сервера: \n {message.content} {getattr(message, 'tool_calls', '')}")
            print("-----------------------------------------------------------------")
            return mcp_response

async def ask_sql_mcp():
    server_params = StdioServerParameters(
        command="uv",
        args=["run",
        "postgres-mcp",
        "--access-mode=unrestricted"
        ],
        env={
        "DATABASE_URI": "postgresql://postgres:postgres@localhost:5432/AI"
      }
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
            question = f"Выполни запрос SQL : INSERT INTO chanels (id, name) VALUES (1, {chanels_data})"
            mcp_response = ''
            print(f'Запрос в CrystalDBA: {question}')
            agent_response = await agent.ainvoke({"messages": [
                {"role": "user", "content": question}]})
            # print("-------------- Ответ модели: --------------")
            print(agent_response)
            for message in agent_response['messages']:
                if type(message).__name__ == "ToolMessage":
                    mcp_response = message.content
                    print(f"Получен ответ MCP-сервера: \n {message.content} {getattr(message, 'tool_calls', '')}")
            print("-----------------------------------------------------------------")
            return mcp_response


# Запуск функции ask telegram mcp
mcp_response = asyncio.run(ask_telegram_mcp())
print("------------- Получено из Telegram ---------------")
print(mcp_response)

chanels_data=mcp_response
mcp_response = asyncio.run(ask_sql_mcp())
print(mcp_response)