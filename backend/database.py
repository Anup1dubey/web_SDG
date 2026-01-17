"""
Database configuration and models for SDG Digital Twin Platform
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration based on environment
DB_TYPE = os.getenv("DB_TYPE", "sqlite")

if DB_TYPE == "mysql":
    # MySQL Configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "sdg_platform")
    
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
else:
    # SQLite Configuration (default)
    SQLITE_FILE = os.getenv("SQLITE_FILE", "sdg_platform.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{SQLITE_FILE}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ScenarioType(enum.Enum):
    """Simulation scenario types"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    DELAY = "delay"
    FAILURE = "failure"
    UNDERFUNDED = "underfunded"


class Organization(Base):
    """Organizations collaborating on SDG projects"""
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    type = Column(String(100))  # NGO, Government, Private, etc.
    description = Column(Text)
    focus_sdgs = Column(JSON)  # List of SDG numbers
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="organization")


class DigitalTwin(Base):
    """Digital Twin - Virtual representation of a region/community"""
    __tablename__ = "digital_twins"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    region = Column(String(255))  # City/Region/Community name
    country = Column(String(100))
    population = Column(Integer)
    area_km2 = Column(Float)
    description = Column(Text)
    baseline_year = Column(Integer, default=2024)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    indicators = relationship("SDGIndicator", back_populates="digital_twin", cascade="all, delete-orphan")
    simulations = relationship("Simulation", back_populates="digital_twin", cascade="all, delete-orphan")


class SDGIndicator(Base):
    """SDG Indicator values for a digital twin"""
    __tablename__ = "sdg_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    digital_twin_id = Column(Integer, ForeignKey("digital_twins.id"), nullable=False)
    sdg_number = Column(Integer, nullable=False)  # 1-17
    sdg_name = Column(String(255))  # e.g., "No Poverty"
    indicator_code = Column(String(50))  # e.g., "SDG1.1"
    indicator_name = Column(String(255))
    baseline_value = Column(Float)  # Current value
    unit = Column(String(50))  # %, count, tons, etc.
    target_value = Column(Float)  # Goal by 2030
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    digital_twin = relationship("DigitalTwin", back_populates="indicators")


class Project(Base):
    """SDG-tagged projects"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    digital_twin_id = Column(Integer, ForeignKey("digital_twins.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    target_sdgs = Column(JSON)  # List of SDG numbers
    budget = Column(Float)
    timeline_months = Column(Integer)
    status = Column(String(50))  # Planning, Active, Completed, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    organization = relationship("Organization", back_populates="projects")
    digital_twin = relationship("DigitalTwin")
    simulations = relationship("Simulation", back_populates="project")


class Simulation(Base):
    """Future Impact Simulation results"""
    __tablename__ = "simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    digital_twin_id = Column(Integer, ForeignKey("digital_twins.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    scenario_type = Column(String(50), nullable=False)  # success, failure, delay, etc.
    simulation_name = Column(String(255))
    
    # Simulation parameters
    funding_percentage = Column(Float, default=100.0)
    timeline_years = Column(Integer, default=5)
    delay_months = Column(Integer, default=0)
    scale_factor = Column(Float, default=1.0)
    
    # Results
    predicted_outcomes = Column(JSON)  # Dict of SDG impacts
    affected_population = Column(Integer)
    confidence_score = Column(Float)
    
    # AI Explanation
    explanation = Column(Text)
    policy_insight = Column(Text)
    risk_warning = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    digital_twin = relationship("DigitalTwin", back_populates="simulations")
    project = relationship("Project", back_populates="simulations")


class Partnership(Base):
    """Partnership requests between organizations"""
    __tablename__ = "partnerships"
    
    id = Column(Integer, primary_key=True, index=True)
    requesting_org_id = Column(Integer, ForeignKey("organizations.id"))
    target_org_id = Column(Integer, ForeignKey("organizations.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    message = Column(Text)
    status = Column(String(50), default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    """User accounts for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    organization_type = Column(String(100))  # Startup, NGO, Government, Researcher
    sdg_interests = Column(JSON)  # List of SDG numbers
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # User preferences
    notifications_enabled = Column(Integer, default=1)
    email_notifications = Column(Integer, default=1)


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
