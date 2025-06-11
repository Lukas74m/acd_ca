from fastapi import FastAPI
from database import engine
from orm import Base
from routes import setup_routes
from fastapi.middleware.cors import CORSMiddleware


class MicroService:
    def __init__(self):
        self.app = FastAPI(
            title="Note-Microservice",
            version="1.0.0",
            description="Microservice für Notenverwaltung",
        )
        # CORS Middleware für Cross-Origin-Anfragen
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Alle Ursprünge zulassen
            allow_credentials=True,  # Cookies sowie Auth-Header zulassen
            allow_methods=["*"],  # Alle HTTP Methoden zulassen
            allow_headers=["*"],  # Alle Header zulassen
        )
        # Erstelle Datenbankfelder, wenn nicht vorhanden
        Base.metadata.create_all(bind=engine, checkfirst=True)
        # Richte Routen ein
        setup_routes(self.app)


if __name__ == "__main__":
    import uvicorn

    service = MicroService()
    # FastAPI-Anwendung starten
    uvicorn.run(service.app, host="0.0.0.0", port=8001)
