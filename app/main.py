from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import imports, data, authentification

app = FastAPI()
app.include_router(imports.router, prefix="/imports", tags=["imports"])
app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(authentification.router, prefix="/authentification", tags=["authentification"])

origins = ["https://lavieillesardine.netlify.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("__main__:app", host="localhost", port=8000, reload=True)
