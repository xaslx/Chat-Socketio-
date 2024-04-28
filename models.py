from pydantic import BaseModel
from typing import Literal


class User(BaseModel):
    room: Literal['Общая', 'Спорт', 'Игры', 'Книги']
    name: str