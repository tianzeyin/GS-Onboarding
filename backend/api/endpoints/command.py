from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.api.models.request_model import CommandRequest
from backend.api.models.response_model import CommandListResponse, CommandSingleResponse
from backend.data.data_models import Command
from backend.data.engine import get_db

# Prefix: "/commands"
command_router = APIRouter(tags=["Commands"])


@command_router.get("/", response_model=CommandListResponse)
def get_commands(db: Session = Depends(get_db)):
    """
    Gets all the items

    :return: Returns a list of commands
    """
    query = select(Command)
    items = db.exec(query).all()
    return {"data": items}


@command_router.post("/", response_model=CommandSingleResponse)
def create_command(payload: CommandRequest, db: Session = Depends(get_db)):
    """
    Creates an item with the given payload in the database and returns this payload after pulling it from the database 
    :param payload: The data used to create an item
    :return: returns a json object with field of "data" under which there is the payload now pulled from the database 
    """
    # TODO:(Member) Implement this endpoint

    cmd = Command(**payload.model_dump())
    db.add(cmd)
    db.commit()
    db.refresh(cmd)

    return {"data": cmd}


@command_router.delete("/{id}", response_model=CommandListResponse)
def delete_command(id: int, db: Session = Depends(get_db)):
    """
    Deletes the item with the given id if it exists. Otherwise raises a 404 error.
    :param id: The id of the item to delete
    :return: returns the list of commands after deleting the item
    """
    # TODO:(Member) Implement this endpoint
    cmd = db.get(Command, id)

    if cmd is None:
        raise HTTPException(status_code = 404, detail = f"Command with id {id} not found")

    db.delete(cmd)
    db.commit()

    return get_commands(db)
