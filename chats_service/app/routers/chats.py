from fastapi import Request, APIRouter

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("/")
def get_chats(request: Request):
    return {"chats": "chats"}