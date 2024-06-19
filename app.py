from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}


app = FastAPI(title="My API", description="This is a very fancy project, with auto docs for the API", version="0.0.1")
app.include_router(router)