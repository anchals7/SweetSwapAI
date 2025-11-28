from datetime import datetime
from pydantic import BaseModel


class DrinkBase(BaseModel):
    name: str
    category: str | None = None
    ingredients: str | None = None
    sugar_content: float | None = None
    caffeine_content: float | None = None
    flavor_profile: str | None = None
    source: str | None = None


class DrinkCreate(DrinkBase):
    pass


class Drink(DrinkBase):
    id: int

    class Config:
        orm_mode = True


class SubstitutionBase(BaseModel):
    substitute_name: str
    substitute_notes: str | None = None


class SubstituteRequest(BaseModel):
    drink_name: str
    include_nutrition: bool = True


class Substitution(SubstitutionBase):
    id: int
    original_drink_name: str
    sugar_delta: float | None = None
    caffeine_delta: float | None = None
    source: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 syntax
        
    @classmethod
    def from_orm(cls, obj):
        """Custom serializer to extract original_drink name from relationship.
        Compatible with both Pydantic v1 (orm_mode) and v2 (from_attributes).
        """
        data = {
            "id": obj.id,
            "substitute_name": obj.substitute_name,
            "substitute_notes": obj.substitute_notes,
            "original_drink_name": obj.original_drink.name if obj.original_drink else "Unknown",
            "sugar_delta": obj.sugar_delta,
            "caffeine_delta": obj.caffeine_delta,
            "source": obj.source,
            "created_at": obj.created_at,
        }
        return cls(**data)

