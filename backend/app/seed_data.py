"""
Script to load seed_substitutions.csv into the database.
Run with: python -m backend.app.seed_data
"""
import csv
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models


def parse_nutrition(nutrition_str: str) -> dict:
    """Parse nutrition string like 'sugar_grams=38;caffeine_mg=60' into dict."""
    result = {"sugar_grams": None, "caffeine_mg": None}
    if not nutrition_str:
        return result
    
    for part in nutrition_str.split(";"):
        if "=" in part:
            key, value = part.strip().split("=", 1)
            try:
                if key == "sugar_grams":
                    result["sugar_grams"] = float(value)
                elif key == "caffeine_mg":
                    result["caffeine_mg"] = float(value)
            except ValueError:
                pass
    return result


def get_or_create_drink(
    db: Session,
    name: str,
    category: str = None,
    sugar: float = None,
    caffeine: float = None,
    flavor_profile: str = None,
    source: str = "seed",
) -> models.Drink:
    """Get existing drink or create new one."""
    drink = db.query(models.Drink).filter(models.Drink.name == name).first()
    if drink:
        return drink
    
    drink = models.Drink(
        name=name,
        category=category,
        sugar_content=sugar,
        caffeine_content=caffeine,
        flavor_profile=flavor_profile,
        source=source,
    )
    db.add(drink)
    db.flush()
    return drink


def load_seed_data():
    """Load CSV data into database."""
    csv_path = project_root / "data" / "seed_substitutions.csv"
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        return
    
    db: Session = SessionLocal()
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            
            for row in reader:
                original_name = row["original_item"].strip()
                substitute_name = row["substitute_item"].strip()
                
                if not original_name or not substitute_name:
                    continue
                
                # Parse nutrition data
                orig_nutrition = parse_nutrition(row.get("nutrition_info", ""))
                sub_nutrition = parse_nutrition(row.get("sub_nutrition_info", ""))
                
                # Get or create original drink
                original_drink = get_or_create_drink(
                    db=db,
                    name=original_name,
                    category=row.get("category"),
                    sugar=orig_nutrition.get("sugar_grams"),
                    caffeine=orig_nutrition.get("caffeine_mg"),
                    flavor_profile=row.get("flavor_profile"),
                    source=row.get("source", "manual"),
                )
                
                # Get or create substitute drink
                substitute_drink = get_or_create_drink(
                    db=db,
                    name=substitute_name,
                    category=row.get("category"),
                    sugar=sub_nutrition.get("sugar_grams"),
                    caffeine=sub_nutrition.get("caffeine_mg"),
                    flavor_profile=row.get("flavor_profile"),
                    source=row.get("source", "manual"),
                )
                
                # Calculate deltas
                sugar_delta = None
                if orig_nutrition.get("sugar_grams") is not None and sub_nutrition.get("sugar_grams") is not None:
                    sugar_delta = sub_nutrition["sugar_grams"] - orig_nutrition["sugar_grams"]
                
                caffeine_delta = None
                if orig_nutrition.get("caffeine_mg") is not None and sub_nutrition.get("caffeine_mg") is not None:
                    caffeine_delta = sub_nutrition["caffeine_mg"] - orig_nutrition["caffeine_mg"]
                
                # Check if substitution already exists
                existing = (
                    db.query(models.Substitution)
                    .filter(models.Substitution.original_drink_id == original_drink.id)
                    .filter(models.Substitution.substitute_name == substitute_name)
                    .first()
                )
                
                if not existing:
                    substitution = models.Substitution(
                        original_drink_id=original_drink.id,
                        substitute_drink_id=substitute_drink.id,
                        substitute_name=substitute_name,
                        substitute_notes=f"Flavor: {row.get('flavor_profile', 'N/A')}",
                        sugar_delta=sugar_delta,
                        caffeine_delta=caffeine_delta,
                        source=row.get("source", "manual"),
                    )
                    db.add(substitution)
                    count += 1
            
            db.commit()
            print(f"✅ Successfully loaded {count} substitutions into database!")
            print(f"   Original drinks: {db.query(models.Drink).count()}")
            print(f"   Substitutions: {db.query(models.Substitution).count()}")
    
    except Exception as e:
        db.rollback()
        print(f"❌ Error loading seed data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    load_seed_data()

