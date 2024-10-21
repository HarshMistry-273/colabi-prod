import os
import nltk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

if not os.path.exists("static"):
    os.mkdir("static")


app = FastAPI(
    title="Colabi",
    # Disable OpenAPI docs in production to reduce startup time
    # openapi_url=False,
    # docs_url=False,
    # redoc_url=False,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
