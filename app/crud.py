from datetime import date, datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from . import models, schemas

# CRUD-операції для Contact

def create_contact(db: Session, data: schemas.ContactCreate) -> models.Contact:
    # Перевірка унікальності email
    exists = db.scalar(select(func.count()).select_from(models.Contact).where(models.Contact.email == data.email))
    if exists:
        raise ValueError("Contact with this email already exists")
    obj = models.Contact(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_contact(db: Session, contact_id: int) -> Optional[models.Contact]:
    return db.get(models.Contact, contact_id)

def list_contacts(db: Session, skip: int = 0, limit: int = 100,
                  first_name: Optional[str] = None,
                  last_name: Optional[str] = None,
                  email: Optional[str] = None) -> List[models.Contact]:
    stmt = select(models.Contact)
    conditions = []
    if first_name:
        conditions.append(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        conditions.append(models.Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        conditions.append(models.Contact.email.ilike(f"%{email}%"))
    if conditions:
        stmt = stmt.where(or_(*conditions))
    stmt = stmt.offset(skip).limit(min(limit, 1000))
    return list(db.scalars(stmt).all())

def update_contact(db: Session, contact_id: int, data: schemas.ContactUpdate) -> Optional[models.Contact]:
    obj = db.get(models.Contact, contact_id)
    if not obj:
        return None
    payload = data.model_dump(exclude_unset=True)
    # Якщо змінюємо email — перевіряємо унікальність
    if "email" in payload and payload["email"] != obj.email:
        exists = db.scalar(select(func.count()).select_from(models.Contact).where(models.Contact.email == payload["email"]))
        if exists:
            raise ValueError("Contact with this email already exists")
    for k, v in payload.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_contact(db: Session, contact_id: int) -> bool:
    obj = db.get(models.Contact, contact_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def upcoming_birthdays(db: Session, days: int = 7) -> List[models.Contact]:
    """
    Повертає контакти з днем народження в найближчі N днів.
    Логіка: обчислюємо найближчу дату народження (з поточним або наступним роком) на Python-рівні
    — простіше і крос-СУБД без складних SQL.
    """
    today = date.today()
    end = today + timedelta(days=days)
    # Вибираємо всіх; для продуктивності можна оптимізувати через SQL-фільтри по місяцю/дню
    contacts = list(db.scalars(select(models.Contact)).all())
    result = []
    for c in contacts:
        try:
            next_bd = c.birthday.replace(year=today.year)
        except ValueError:
            # 29 лютого: переносимо на 28 лютого в невисокосні роки
            next_bd = date(today.year, 2, 28)
        if next_bd < today:
            # якщо в цьому році вже минув — беремо наступний рік
            try:
                next_bd = c.birthday.replace(year=today.year + 1)
            except ValueError:
                next_bd = date(today.year + 1, 2, 28)
        if today <= next_bd <= end:
            result.append(c)
    return result