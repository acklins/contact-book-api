from fastapi import APIRouter, HTTPException 
from typing import Optional
from datetime import datetime

from app.schemas.contact import(
    ContactCreate, 
    ContactUpdate, 
    ContactResponse, 
    ContactCategory,
)

router = APIRouter()

#in memory list
contacts = []
_next_id = 1

#Create POST /contacts
@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    global _next_id
    
    new_contact = contact.model_dump(mode="json")
    new_contact["id"] = _next_id
    new_contact["created_at"] = datetime.now().isoformat()

    contacts.append(new_contact)
    _next_id += 1

    return new_contact

#Get all contacts GET /contacts; query param
@router.get("/", response_model=list[ContactResponse])
def list_contacts(category: Optional[ContactCategory] = None):
    if category is None:
        return contacts
    
    return [
        contact 
        for contact in contacts 
        if contact["category"] == category.value
    ]

#GET by ID
@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")

#Create PATCH
@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact_update: ContactUpdate):

    for contact in contacts:
        if contact["id"] == contact_id:
            update_data = contact_update.model_dump(exclude_unset=True)
            contact.update(update_data)
            return contact
        
    raise HTTPException(status_code=404, detail="Contact not found")
