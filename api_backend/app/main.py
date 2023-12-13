from fastapi import FastAPI
import uvicorn
from api_backend.app.routes import users
from api_backend.app.routes import sos_rituals
from fastapi.responses import HTMLResponse
app = FastAPI(title="assistant_backend_api")

app.include_router(users.router)
app.include_router(sos_rituals.router)


# TODO figure out future versioning
# TODO will have to add CORS https://fastapi.tiangolo.com/tutorial/cors/
@app.get(
    "/",
    summary="Index page",
    description="Base index page - just links to docs/schemas",
    response_class=HTMLResponse
    )
def root() -> str:
    """Index page"""
    return """<a href="/docs">Swagger documentation</a>"""


def main() -> None:
    print("Running")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80
    )


if __name__ == "__main__":
    main()
