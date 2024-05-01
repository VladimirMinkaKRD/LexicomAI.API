import json
from typing import Any

from redis.asyncio import Redis

from app.schemas import CreatingLexicomAI


class Cache:
    """
    Класс для создания и работы объектов кэша.
    """

    def __init__(self, redis: Redis, ttl):
        """Инициализация объекта кэша."""
        self.redis = redis
        self.ttl = ttl

    @staticmethod
    def encode_body(body: CreatingLexicomAI) -> bytes:
        """Метод для превращения схемы в строку и дальнейшее ее кодирование в байты, так как Redis хранит данные в
        байтах."""
        return json.dumps(body.model_dump()).encode()

    @staticmethod
    def decode_body(body: bytes) -> json:
        """Метод обратный методу encode_body."""
        return json.loads(body.decode())

    async def set(self, key: str, body: Any) -> None:
        """Метод для записи данных в кэш."""
        body = self.encode_body(body)
        await self.redis.set(key, body)

    async def get(self, key: str) -> str | None:
        """Метод для получения данных из кэша. Получаем сразу же адрес."""
        data = await self.redis.get(key)
        if data is None:
            return None
        return self.decode_body(data)['address']
