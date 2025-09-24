import httpx

from api.workflow_engine.nodes.base import BaseNodeExecutor


class TelegramNodeExecutor(BaseNodeExecutor):
    async def execute(self, input_data: dict) -> dict:
        bot_token = self.credentials.get("bot_token")

        chat_id = self.parameters.chat_id
        message_text = self.parameters.message_text

        if not bot_token:
            raise ValueError("Missing bot_token in credentials for Telegram node")

        api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message_text}

        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload)
            response.raise_for_status()

        print(f"Successfully sent Telegram message to chat_id {chat_id}")
        return {"status": "success", "response": response.json()}
