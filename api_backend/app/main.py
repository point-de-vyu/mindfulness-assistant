from fastapi import FastAPI
import uvicorn
from api_backend.app.routes import users
from api_backend.app.routes import sos_rituals
from fastapi.responses import HTMLResponse
from api_backend.app.logger import set_up_logger

app = FastAPI(title="Assistant API")

logger = set_up_logger(set_up_stdout=True)

app.include_router(users.router, prefix="/v1")
app.include_router(sos_rituals.router, prefix="/v1")


# TODO figure out future versioning
# TODO will have to add CORS https://fastapi.tiangolo.com/tutorial/cors/
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
    uvicorn.run("main:app", host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()
