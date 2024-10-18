import redis
import json
from app.config import settings
from app.models import User

# Initialize Redis client
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def get_user(username: str):
    user_data = redis_client.get(username)
    if user_data:
        return json.loads(user_data)
    return None

def add_user(username: str, hashed_password: str):
    user_data = {
        "username": username,
        "hashed_password": hashed_password
    }
    redis_client.set(username, json.dumps(user_data))

    return User(username=username, hashed_password=hashed_password)