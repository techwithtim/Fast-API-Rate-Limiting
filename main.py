from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from app.api.routes import router
from app.config import limiter

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
