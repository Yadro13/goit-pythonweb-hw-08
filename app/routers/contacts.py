from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud, models
from sqlalchemy import text

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("", response_model=schemas.ContactOut, status_code=status.HTTP_201_CREATED)
def create_contact(payload: schemas.ContactCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_contact(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[schemas.ContactOut])
def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    first_name: Optional[str] = Query(None, description="Пошук за іменем (ILike)"),
    last_name: Optional[str] = Query(None, description="Пошук за прізвищем (ILike)"),
    email: Optional[str] = Query(None, description="Пошук за email (ILike)"),
    db: Session = Depends(get_db),
):
    return crud.list_contacts(db, skip=skip, limit=limit, first_name=first_name, last_name=last_name, email=email)

@router.get("/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    obj = crud.get_contact(db, contact_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Contact not found")
    return obj

@router.put("/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, payload: schemas.ContactUpdate, db: Session = Depends(get_db)):
    try:
        obj = crud.update_contact(db, contact_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not obj:
        raise HTTPException(status_code=404, detail="Contact not found")
    return obj

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_contact(db, contact_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None

@router.get("/birthdays/upcoming", response_model=List[schemas.ContactOut])
def birthdays_upcoming(days: int = Query(7, ge=1, le=365), db: Session = Depends(get_db)):
    return crud.upcoming_birthdays(db, days=days)