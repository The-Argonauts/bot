from configs.redis import RedisClient

class Authorization:
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client.get_connection()

    def store_user_token(self, telegram_id: str, user_id: int):
        self.redis_client.hset("users", telegram_id, str(user_id))

    def store_business_token(self, telegram_id: str, user_id: int):
        self.redis_client.hset("business", telegram_id, str(user_id))

    def delete_user_token(self, telegram_id: str):
        self.redis_client.hdel("users", telegram_id)

    def delete_business_token(self, telegram_id: str):
        self.redis_client.hdel("business", telegram_id)

    def authorize_user(self, telegram_id: str) -> bool:
        if self.redis_client.hexists("business", telegram_id):
            raise ValueError("You have to logout from business account first")
        return self.redis_client.hexists("users", telegram_id)

    def authorize_business(self, telegram_id: str) -> bool:
        if self.redis_client.hexists("users", telegram_id):
            raise ValueError("You have to logout from user account first")
        return self.redis_client.hexists("business", telegram_id)

    def get_user_id(self, telegram_id: str) -> int:
        return int(self.redis_client.hget("users", telegram_id))

    def get_business_id(self, telegram_id: str) -> int:
        return int(self.redis_client.hget("business", telegram_id))