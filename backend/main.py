from pathlib import Path
from dotenv import load_dotenv
from contextlib import asynccontextmanager

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.database import check_db_connection, init_db
from backend.api.routes import jogadores, partidas, sincronizacao 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"\nIniciando {settings.APP_NAME} v{settings.APP_VERSION}...")
    
    if check_db_connection():
        print("Conexão com banco de dados estabelecida")
        init_db()
        print("Tabelas verificadas/criadas")
    else:
        print("Falha na conexão com banco de dados")
    
    yield
    
    print(f"\nEncerrando {settings.APP_NAME}...")

app = FastAPI(
    title=settings.APP_NAME,
    description="API para rastrear e analisar partidas de League of Legends",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(jogadores.router)
app.include_router(partidas.router)
app.include_router(sincronizacao.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "api": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }

@app.get("/health", tags=["Health"])
def health_check():
    db_ok = check_db_connection()
    
    return {
        "status": "healthy" if db_ok else "unhealthy",
        "api": "online",
        "database": "connected" if db_ok else "disconnected"
    }

@app.get("/db/info", tags=["Health"])
def database_info():
    from backend.database import get_db_info
    return get_db_info()