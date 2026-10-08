from sqlmodel import SQLModel, Field
from pydantic import BaseModel, ConfigDict
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    input_text: str
    result: str

class PredictionCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    input_text: str
