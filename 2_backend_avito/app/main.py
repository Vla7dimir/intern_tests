from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_session
from app.repository import find_by_code, save_url
from app.schemas import CreateRequest, CreateResponse
from app.utils import check_code, check_url

app = FastAPI(title="URL Shortener", version="1.0.0")


@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)


@app.post("/api/v1/shorten", response_model=CreateResponse, status_code=status.HTTP_201_CREATED)
def shorten(request: CreateRequest, db: Session = Depends(get_session)):
    if not check_url(request.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL"
        )

    if request.code:
        if not check_code(request.code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Code must be 3-50 alphanumeric characters, hyphens, or underscores",
            )

        existing = find_by_code(db, request.code)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Code already exists"
            )

    record = save_url(db, request.url, request.code)

    return CreateResponse(
        short=f"{settings.base_url}/{record.code}",
        original=record.full_url,
        code=record.code,
    )


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_session)):
    record = find_by_code(db, code)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
        )
    return RedirectResponse(url=record.full_url, status_code=status.HTTP_302_FOUND)


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
