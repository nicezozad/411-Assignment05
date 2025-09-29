from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel
from typing import Optional, Literal, List
from datetime import date

class PersonalDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    user_type: str          
    phone_number: str
    email: str              
    idcard_file: str
    id_number: str
    birth: date
    religion: str
    village_name: str
    house_number: str
    road: str
    alley: str
    province: str
    district: str
    subdistrict: str

class Personal(BaseModel):
    name: str
    surname: str
    user_type: Literal["individual", "group"]   
    phone_number: str
    email: EmailStr                             
    idcard_file: str
    id_number: str
    birth: date
    religion: str
    village_name: str
    house_number: str
    road: str
    alley: str
    province: str
    district: str
    subdistrict: str

class PersonalOut(Personal):
    id: int