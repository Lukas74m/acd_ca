from fastapi import FastAPI
from database import engine
from orm import Base
from routes import setup_routes
from fastapi.middleware.cors import CORSMiddleware


class MicroService:
    def __init__(self):

        self.app = FastAPI(title="Exams Microservice", version="1.0.0")

        # CORS-Middleware hinzu, um Anfragen von anderen Ursprüngen zu erlauben
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Alle Tabellen in der Datenbank erstellen, falls sie noch nicht existieren
        Base.metadata.create_all(bind=engine, checkfirst=True)

        setup_routes(self.app)


# Starte den fastAPI-Server mit uvicorn
if __name__ == "__main__":
    import uvicorn

    service = MicroService()
    uvicorn.run(service.app, host="0.0.0.0", port=8002)  # Server auf Port 8002, erreichbar über alle IPs im Cluster
