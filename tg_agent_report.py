#!/usr/bin/python3

from datetime import datetime, timezone, timedelta, UTC
import pathlib

answer = (f"### Рекомендации участникам:\n"
        "\n"
        "- Изучить детально спецификацию используемого API (MCP).\n"
        "- Проверить синтаксис запросов вручную перед передачей в модель.\n"
        "- Экспериментировать с различными моделями и их настройками.\n"
        "- Рассмотреть возможность увеличения количества выделяемых токенов для улучшения качества результатов.\n"
        "- Обратиться к технической поддержке провайдера сервисов для помощи с настройкой инфраструктуры.")
dt_format = '%Y-%m-%d %H-%M'
now_utc = datetime.now()
p = pathlib.Path(__file__)
p = p.parents[0].joinpath('Reports',f'report {now_utc:{dt_format}}.md')
print(p)
with open(p, "w") as file:
    file.write(answer)