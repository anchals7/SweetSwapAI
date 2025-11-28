from sqlalchemy.orm import Session

from .. import models, schemas
from .llm import generate_substitution
from .nutrition import enrich_nutrition_data


def find_existing_substitution(db: Session, drink_name: str) -> models.Substitution | None:
    drink = (
        db.query(models.Drink)
        .filter(models.Drink.name.ilike(drink_name))
        .first()
    )
    if not drink:
        return None
    return (
        db.query(models.Substitution)
        .filter(models.Substitution.original_drink_id == drink.id)
        .order_by(models.Substitution.created_at.desc())
        .first()
    )


def create_substitution_record(
    db: Session,
    original_drink_name: str,
    substitute_payload: dict,
    source: str,
) -> models.Substitution:
    drink = (
        db.query(models.Drink)
        .filter(models.Drink.name.ilike(original_drink_name))
        .first()
    )
    if not drink:
        drink = models.Drink(name=original_drink_name, source=source)
        db.add(drink)
        db.flush()

    substitution = models.Substitution(
        original_drink_id=drink.id,
        substitute_name=substitute_payload["name"],
        substitute_notes=substitute_payload.get("notes"),
        sugar_delta=substitute_payload.get("sugar_delta"),
        caffeine_delta=substitute_payload.get("caffeine_delta"),
        source=source,
    )
    db.add(substitution)
    db.commit()
    db.refresh(substitution)
    return substitution


def get_or_create_substitution(
    db: Session,
    request: schemas.SubstituteRequest,
) -> schemas.Substitution:
    existing = find_existing_substitution(db, request.drink_name)
    if existing:
        # Use custom serializer to include original_drink_name
        return schemas.Substitution.from_orm(existing)

    nutrition = enrich_nutrition_data(request.drink_name) if request.include_nutrition else {}
    llm_payload = generate_substitution(request.drink_name, nutrition=nutrition)
    record = create_substitution_record(
        db,
        original_drink_name=request.drink_name,
        substitute_payload=llm_payload,
        source="llm",
    )
    # Reload to get relationships
    db.refresh(record)
    return schemas.Substitution.from_orm(record)

