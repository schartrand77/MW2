from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pyotp

from ....config import settings
from ....db import get_db
from ....models import User
from ....security import (
    CSRF_COOKIE,
    create_csrf_token,
    create_session,
    get_current_user,
    get_password_hash,
    verify_csrf,
    verify_password,
)

router = APIRouter()


class SignUp(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(data: SignUp, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, hashed_password=get_password_hash(data.password))
    db.add(user)
    db.commit()
    return {"id": user.id, "email": user.email}


class SignIn(BaseModel):
    email: str
    password: str
    otp: str | None = None


@router.post("/signin")
def signin(
    data: SignIn, response: Response, db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(email=data.email).first()
    if (
        not user
        or not user.hashed_password
        or not verify_password(data.password, user.hashed_password)
    ):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if user.twofa_secret:
        totp = pyotp.TOTP(user.twofa_secret)
        if not data.otp or not totp.verify(data.otp):
            raise HTTPException(status_code=400, detail="Invalid OTP")
    session_token = create_session(user.id)
    csrf_token = create_csrf_token()
    response.set_cookie(
        "session", session_token, httponly=True, samesite="lax"
    )
    response.set_cookie(CSRF_COOKIE, csrf_token, samesite="lax")
    return {"id": user.id, "email": user.email}


@router.post("/signout")
def signout(response: Response, request: Request):
    verify_csrf(request)
    response.delete_cookie("session")
    response.delete_cookie(CSRF_COOKIE)
    return {"status": "signed_out"}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email}


@router.post("/totp/setup")
def totp_setup(user: User = Depends(get_current_user)):
    if user.twofa_secret:
        raise HTTPException(status_code=400, detail="already enabled")
    secret = pyotp.random_base32()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email, issuer_name="MakerWorks"
    )
    return {"secret": secret, "uri": uri}


class TotpVerify(BaseModel):
    secret: str
    code: str


@router.post("/totp/verify")
def totp_verify(
    data: TotpVerify, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    totp = pyotp.TOTP(data.secret)
    if not totp.verify(data.code):
        raise HTTPException(status_code=400, detail="invalid code")
    user.twofa_secret = data.secret
    db.add(user)
    db.commit()
    return {"status": "ok"}


@router.get("/oauth/{provider}")
def oauth_start(provider: str):  # pragma: no cover - stub
    if provider not in {"google", "github", "apple"}:
        raise HTTPException(status_code=404)
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/oauth/{provider}/callback")
def oauth_callback(provider: str):  # pragma: no cover - stub
    if provider not in {"google", "github", "apple"}:
        raise HTTPException(status_code=404)
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
