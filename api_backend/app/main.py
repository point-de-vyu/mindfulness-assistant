from fastapi import FastAPI
import uvicorn
from api_backend.app.routes import users
from api_backend.app.routes import sos_rituals
from fastapi.responses import HTMLResponse
from api_backend.app.logger import set_up_logger
import os


app = FastAPI(title="Assistant API")

logger = set_up_logger(set_up_stdout=True)

app.include_router(users.router, prefix="/v1")
app.include_router(sos_rituals.router, prefix="/v1")


@app.get(
    "/",
    summary="Index page",
    description="Base index page - just links to docs/schemas",
    response_class=HTMLResponse,
)
def root() -> str:
    """Index page"""
    logger.info("Accessing index page")
    return """<a href="/docs">Swagger documentation</a>"""


def main() -> None:
    logger.info("Start api_backend service locally")
    uvicorn.run("main:app", host=os.environ["HOST"], port=int(os.environ["PORT"]))


if __name__ == "__main__":
    main()
