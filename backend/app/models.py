from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base


class Drink(Base):
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=True)
    ingredients = Column(String, nullable=True)
    sugar_content = Column(Float, nullable=True)
    caffeine_content = Column(Float, nullable=True)
    flavor_profile = Column(String, nullable=True)
    source = Column(String, default="seed")

    substitutions = relationship(
        "Substitution",
        back_populates="original_drink",
        foreign_keys="Substitution.original_drink_id",
    )


class Substitution(Base):
    __tablename__ = "substitutions"

    id = Column(Integer, primary_key=True, index=True)
    original_drink_id = Column(Integer, ForeignKey("drinks.id"), nullable=False)
    substitute_drink_id = Column(Integer, ForeignKey("drinks.id"), nullable=True)
    substitute_name = Column(String, nullable=False)
    substitute_notes = Column(String, nullable=True)
    sugar_delta = Column(Float, nullable=True)
    caffeine_delta = Column(Float, nullable=True)
    source = Column(String, default="manual")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    original_drink = relationship(
        "Drink",
        foreign_keys=[original_drink_id],
        back_populates="substitutions",
    )
    substitute_drink = relationship(
        "Drink",
        foreign_keys=[substitute_drink_id],
        lazy="joined",
    )

