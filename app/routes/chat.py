from fastapi import APIRouter, Depends

from ..dependencies import get_philo_chat
from ..schemas.chat import ChatCreateReq, MessageCreateReq
from ..services import PhiloChat

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/")
def create_chat(chat: ChatCreateReq, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.new_chat(chat.chat_name, chat.philosopher_id)

    except Exception:
        pass


@router.get("/")
def get_chats(pc: PhiloChat = Depends(get_philo_chat)):
    try:
        chat_list = pc.list_chats()
        return chat_list

    except Exception:
        pass


@router.delete("/{chat_name}")
def delete_chat(chat_name: str, pc: PhiloChat = Depends(get_philo_chat)):
    try:
        pc.delete_chat(chat_name)

    except Exception:
        pass


@router.post("/{chat_name}/messages")
def create_message(
    chat_name: str, data: MessageCreateReq, pc: PhiloChat = Depends(get_philo_chat)
):
    try:
        ai_msg, user_msg = pc.complete_chat(data.input_text)
        return ai_msg, user_msg

    except Exception:
        pass
