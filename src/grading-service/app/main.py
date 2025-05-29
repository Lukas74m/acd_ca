from fastapi import FastAPI
from database import engine
from orm import Base
from routes import setup_routes


class MicroService:
    def __init__(self):
        self.app = FastAPI(title="Notes Microservice", version="1.0.0")

        Base.metadata.create_all(bind=engine, checkfirst=True)

        setup_routes(self.app)


if __name__ == "__main__":
    import uvicorn

    service = MicroService()
    uvicorn.run(service.app, host="localhost", port=8000)
