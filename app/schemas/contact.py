from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator

#Category enum for classifying contacts
class ContactCategory(str, Enum):
    personal = "personal"
    work = "work"
    family = "family"

#Contact model for representing a contact with name, email, phone, and category
class ContactCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: str 
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: ContactCategory 

    #Custom email validatior
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Email must contain @")
        return value

#Contact update all fields optional
class ContactUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[str] = None
    phone: Optional[str] = Field(default=None, min_length=10, max_length=15)
    category: Optional[ContactCategory] = None

#Updated email validator
@field_validator("email")
@classmethod
def validate_email(cls, value):
    if value is not None and "@" not in value:
        raise ValueError("Email must contain @")
    return value

#Contact response with inheritance; all info + the below fields
class ContactResponse(ContactCreate):
    id: int
    created_at: str  