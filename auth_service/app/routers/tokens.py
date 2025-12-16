from fastapi import APIRouter

tokens_router = APIRouter()

@tokens_router.get("/test")
def test(string: str):
    return {"test": string}