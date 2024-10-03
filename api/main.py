from fastapi import FastAPI

# from .kitten.router import router

app = FastAPI(
    title="Kittens API", description="A Test Task About Kittens", version="1.0.0"
)

# app.include_router(router, tags=["Kitten"])
