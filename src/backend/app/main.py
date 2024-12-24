from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app import github

app = FastAPI()

app.include_router(github.github_router)


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <a href="/redoc">redoc</a>
    <a href="/openapi.json">redoc</a>
"""


# class WebhookBody(BaseModel):
#     repository: object
#     model_config = {"extra": "allow"}


# @app.post("/")
# async def webhook_ex(body: WebhookBody, x_github_event: Annotated[str, Header()]):
#     print(x_github_event)
#     print(json.dumps(body.repository, indent=2))
#     if body.action == "created":
#         subprocess.run(["gh", "repo", "clone", body.repository["clone_url"]])
