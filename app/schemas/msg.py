from pydantic import BaseModel


class Msg(BaseModel):
    """
    消息响应模型
    """
    msg: str 