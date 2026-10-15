from unittest import result

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from db import get_db
from dependencies import get_current_user
from models.library_item_model import ItemFormat, LibraryItem, MediaType
from models.user_model import User
from schemas.library_item_schema import LibraryItemCreate
from models.library_item_model import MediaType

router = APIRouter(prefix="/items")


@router.get("/me")
def get_my_items(
    media_type: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(LibraryItem).filter(
        LibraryItem.owner_id == current_user.id
    )

    if media_type == "currently":
        query = query.filter(
            LibraryItem.currently.is_(True)
        )
    elif media_type in ("book", "comic"):
        query = query.filter(
            LibraryItem.media_type == MediaType(media_type)
        )
    elif media_type not in (None, "", "all"):
        raise HTTPException(
            status_code=400,
            detail="Invalid media_type filter"
        )

    items = query.all()

    print("Requested filter:", media_type)
    print("Returned items:", [
        {
            "id": item.id,
            "title": item.title,
            "currently": item.currently
        }
        for item in items
    ])

    return items


@router.get("/user/{username}")
def get_user_items(
    username: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    items = db.query(LibraryItem).filter(
        LibraryItem.owner_id == user.id
    ).all()

    return items


@router.post("/")
def create_item(
    item: LibraryItemCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    new_item = LibraryItem(
    title=item.title,
    author=item.author,
    genre=item.genre,
    language=item.language,
    media_type=item.media_type,
    read=item.read,
    format=item.format,
    owner_id=user.id,
    currently=item.currently
)

    try:
        print(item)
        ...
    except Exception as e:
        print("CREATE ITEM ERROR:", e)
        raise

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


@router.put("/{item_id}")
def update_item(
    item_id: int,
    updated_item: LibraryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(LibraryItem).filter(
        LibraryItem.id == item_id,
        LibraryItem.owner_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    print("Incoming currently:", updated_item.currently)

    item.title = updated_item.title
    item.author = updated_item.author
    item.genre = updated_item.genre
    item.language = updated_item.language
    item.media_type = updated_item.media_type
    item.read = updated_item.read
    item.format = updated_item.format
    item.currently = updated_item.currently

    db.commit()
    db.refresh(item)

    result = db.execute(
    text("""
        SELECT currently
        FROM library_items
        WHERE id = :item_id
    """),
    {"item_id": item_id}
).scalar()

    print("ORM value after refresh:", item.currently)
    print("Database value after commit:", result)

    print("Saved currently:", item.currently)

    return item