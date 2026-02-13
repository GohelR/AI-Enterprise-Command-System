"""Initialize the SQLite database with baseline data."""

import os
import sys

from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.core.security import get_password_hash
from backend.app.db.database import Base, get_engine
from backend.app.models.models import Department, User

engine = get_engine()
if engine is None:
    raise RuntimeError("Database engine is unavailable")

print("Creating database tables...")
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    admin = db.query(User).filter(User.email == "admin@ai-enterprise.com").first()
    if not admin:
        admin = User(
            email="admin@ai-enterprise.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="System Administrator",
            role="admin",
            department="IT",
            is_active=True,
        )
        db.add(admin)

    departments = [
        ("Human Resources", "HR and talent management"),
        ("Finance", "Financial operations and accounting"),
        ("Customer Support", "Customer service and support"),
        ("Marketing", "Marketing and growth"),
        ("Sales", "Sales and CRM"),
        ("Operations", "Operations and automation"),
        ("IT", "Information Technology"),
        ("Security", "Cybersecurity and risk management"),
        ("Data Analytics", "Data science and analytics"),
        ("AI Research", "AI and ML research"),
        ("Legal", "Legal and compliance"),
        ("Strategy", "Business strategy and leadership"),
    ]

    existing_departments = {d.name for d in db.query(Department).all()}
    for name, description in departments:
        if name not in existing_departments:
            db.add(Department(name=name, description=description))

    db.commit()
    print("✅ Database initialized successfully!")
except Exception as exc:
    print(f"❌ Error initializing database: {exc}")
    db.rollback()
finally:
    db.close()
