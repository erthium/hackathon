from fastapi import Body, FastAPI

from app.routers import (
  command_router,
  template_router,
)


app = FastAPI()

# Include routers
app.include_router(command_router)
app.include_router(template_router)


@app.get(
  "/",
  summary="Root",
  description="Root endpoint",
  response_description="Beneath this mask, there is more than flesh...",
)
def get_root():
  return "V"  # V for Vendetta
