from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import Org, OrgMember, User
from ....security import get_current_user
from ....audit import log_event

router = APIRouter()


class OrgCreate(BaseModel):
    name: str


@router.post("/")
def create_org(
    data: OrgCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    org = Org(name=data.name)
    db.add(org)
    db.flush()
    member = OrgMember(org_id=org.id, user_id=user.id, role="owner")
    db.add(member)
    db.commit()
    log_event(db, user.id, "org_created", {"org_id": org.id})
    return {"id": org.id, "name": org.name}


@router.get("/")
def list_orgs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    orgs = (
        db.query(Org)
        .join(OrgMember)
        .filter(OrgMember.user_id == user.id)
        .all()
    )
    return [{"id": o.id, "name": o.name} for o in orgs]
