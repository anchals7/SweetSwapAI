from fastapi import FastAPI, Depends, HTTPException

from . import schemas, models
from .database import get_db, Base, engine
from .services.substitution import get_or_create_substitution

# Create tables on startup; later replace with Alembic migrations
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SweetSwap AI")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/substitute", response_model=schemas.Substitution)
def request_substitute(
    payload: schemas.SubstituteRequest,
    db=Depends(get_db),
):
    return get_or_create_substitution(db, payload)


@app.get("/substitute/{drink_id}", response_model=schemas.Substitution)
def get_substitute(drink_id: int, db=Depends(get_db)):
    record = db.query(models.Substitution).filter(models.Substitution.id == drink_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Substitution not found")
    return schemas.Substitution.from_orm(record)

