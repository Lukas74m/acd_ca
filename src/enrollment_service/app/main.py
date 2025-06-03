from fastapi import FastAPI
from database import engine
from orm import Base
from routes import setup_routes
from fastapi.middleware.cors import CORSMiddleware


class MicroService:
    def __init__(self):
        self.app = FastAPI(title="Exams Microservice", version="1.0.0")

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        Base.metadata.create_all(bind=engine, checkfirst=True)

        setup_routes(self.app)


if __name__ == "__main__":
    import uvicorn

    service = MicroService()
    uvicorn.run(service.app, host="localhost", port=8002)
