from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....db import get_db
from ....models import Model3D, User
from ....security import get_current_user
from ....thumbnail import generate_thumbnail

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[6]
UPLOAD_DIR = BASE_DIR / 'uploads'
THUMB_DIR = BASE_DIR / 'thumbnails'
UPLOAD_DIR.mkdir(exist_ok=True)
THUMB_DIR.mkdir(exist_ok=True)


@router.get('/')
def list_models(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    models = db.query(Model3D).filter_by(user_id=user.id).all()
    return [
        {
            'id': m.id,
            'filename': m.filename,
            'thumbnail': m.thumbnail,
            'meta': m.meta,
        }
        for m in models
    ]


@router.post('/')
def upload_model(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    ext = Path(file.filename).suffix.lower()
    if ext not in {'.stl', '.3mf'}:
        raise HTTPException(status_code=400, detail='unsupported format')
    model = Model3D(user_id=user.id, filename=file.filename, meta={})
    db.add(model)
    db.commit()
    db.refresh(model)
    path = UPLOAD_DIR / f"{model.id}{ext}"
    with open(path, 'wb') as f:
        f.write(file.file.read())
    thumb = THUMB_DIR / f"{model.id}.png"
    generate_thumbnail(path, thumb)
    model.thumbnail = str(thumb.relative_to(BASE_DIR))
    db.add(model)
    db.commit()
    return {'id': model.id, 'filename': model.filename, 'thumbnail': model.thumbnail}


@router.get('/{model_id}')
def get_model(model_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    model = db.get(Model3D, model_id)
    if not model or model.user_id != user.id:
        raise HTTPException(status_code=404)
    return {
        'id': model.id,
        'filename': model.filename,
        'thumbnail': model.thumbnail,
        'meta': model.meta,
    }


@router.get('/{model_id}/file')
def get_model_file(model_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    model = db.get(Model3D, model_id)
    if not model or model.user_id != user.id:
        raise HTTPException(status_code=404)
    ext = Path(model.filename).suffix
    path = UPLOAD_DIR / f"{model.id}{ext}"
    return FileResponse(path)


class ColorIn(BaseModel):
    color: str


@router.post('/{model_id}/color')
def set_color(
    model_id: str,
    data: ColorIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    model = db.get(Model3D, model_id)
    if not model or model.user_id != user.id:
        raise HTTPException(status_code=404)
    meta = model.meta or {}
    meta['color'] = data.color
    model.meta = meta
    ext = Path(model.filename).suffix
    path = UPLOAD_DIR / f"{model.id}{ext}"
    thumb = THUMB_DIR / f"{model.id}.png"
    generate_thumbnail(path, thumb, color=data.color)
    model.thumbnail = str(thumb.relative_to(BASE_DIR))
    db.add(model)
    db.commit()
    return {'status': 'ok', 'thumbnail': model.thumbnail}


@router.post('/{model_id}/rethumb')
def rethumb(model_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    model = db.get(Model3D, model_id)
    if not model or model.user_id != user.id:
        raise HTTPException(status_code=404)
    ext = Path(model.filename).suffix
    path = UPLOAD_DIR / f"{model.id}{ext}"
    thumb = THUMB_DIR / f"{model.id}.png"
    color = (model.meta or {}).get('color', '#888888')
    generate_thumbnail(path, thumb, color=color)
    model.thumbnail = str(thumb.relative_to(BASE_DIR))
    db.add(model)
    db.commit()
    return {'status': 'ok', 'thumbnail': model.thumbnail}
