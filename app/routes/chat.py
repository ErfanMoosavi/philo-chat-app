from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_philo_chat, get_current_user
from ..schemas.chat import ChatCreateReq, MessageCreateReq, ChatNameUpdateReq
from ..services import PhiloChat
from ..core.exceptions import BadRequestError, NotFoundError

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_chat(
    chat: ChatCreateReq,
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.new_chat(username, chat.chat_name, chat.philosopher_id)
        return {"message": "Created chat successfully"}

    except BadRequestError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.get("/", status_code=status.HTTP_200_OK)
def get_chats(
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        chat_list = pc.get_chat_list(username)
        return chat_list

    except NotFoundError:
        return {"message": "No chats found"}
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.patch("/{chat_name}", status_code=status.HTTP_200_OK)
def rename_chat(
    old_chat_name,
    request: ChatNameUpdateReq,
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.rename_chat(username, old_chat_name, request.new_chat_name)

    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))


@router.delete("/{chat_name}", status_code=status.HTTP_200_OK)
def delete_chat(
    chat_name: str,
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        pc.delete_chat(username, chat_name)
        return {"message": "Deleted chat successfully"}

    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


@router.post("/{chat_name}/messages", status_code=status.HTTP_201_CREATED)
def create_message(
    chat_name: str,
    data: MessageCreateReq,
    username: str = Depends(get_current_user),
    pc: PhiloChat = Depends(get_philo_chat),
):
    try:
        ai_msg, user_msg = pc.complete_chat(username, chat_name, data.input_text)
        return {
            "user_message": user_msg.content,
            "philosopher_response": ai_msg.content,
        }

    except BadRequestError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
