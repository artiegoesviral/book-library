from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from db import get_db

from dependencies import get_current_user

from models.library_item_model import LibraryItem

from models.user_model import User

router = APIRouter(prefix="/items")


@router.get("/me")
def get_my_items(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    return db.query(LibraryItem).filter(
        LibraryItem.owner_id == user.id
    ).all()


@router.get("/user/{username}")
def get_user_items(
    username: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.name == username
    ).first()

    if not user:
        raise HTTPException(status_code=404)

    return db.query(LibraryItem).filter(
        LibraryItem.owner_id == user.id
    ).all()


@router.post("/")
def create_item(
    item: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    new_item = LibraryItem(
        title=item["title"],
        author=item["author"],
        genre=item["genre"],
        media_type=item["media_type"],
        read=item["read"],
        format=item["format"],
        owner_id=user.id
    )

    db.add(new_item)

    db.commit()

    db.refresh(new_item)

    return new_item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    item = db.query(LibraryItem).filter(
        LibraryItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(status_code=404)

    if item.owner_id != user.id:
        raise HTTPException(status_code=403)

    db.delete(item)

    db.commit()

    return {"message": "Deleted"}