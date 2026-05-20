from __future__ import annotations

from datetime import timezone, timedelta

from airflow.notifications.basenotifier import BaseNotifier
from airflow.providers.telegram.hooks.telegram import TelegramHook

MSK = timezone(timedelta(hours=3))


class TelegramNotifier(BaseNotifier):
    """Sends a Telegram message when a DAG task fails."""

    def __init__(self, conn_id: str = "telegram_default") -> None:
        self.conn_id = conn_id

    def notify(self, context: dict) -> None:
        ti = context["task_instance"]
        dag = context["dag"]
        exception = context.get("exception")

        text = (
            f"🚨 DAG Failed\n\n"
            f"DAG: {dag.dag_id}\n"
            f"Task: {ti.task_id}\n"
            f"Time: {ti.execution_date.astimezone(MSK).strftime('%Y-%m-%d %H:%M:%S UTC+3')}\n"
            f"Run: {ti.run_id}\n\n"
            f'Log: <a href="{ti.log_url}">открыть лог</a>\n\n'
            f"Error: {exception}"
        )

        hook = TelegramHook(telegram_conn_id=self.conn_id)
        hook.send_message({"text": text})
