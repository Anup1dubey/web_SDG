"""
Pydantic models for MongoDB documents
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# User Model
class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    email: EmailStr
    hashed_password: str
    full_name: str
    organization_type: str
    sdg_interests: List[int] = []
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    notifications_enabled: bool = True
    email_notifications: bool = True

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Digital Twin Model
class DigitalTwinModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    region: str
    country: str
    population: int
    area_km2: float
    description: Optional[str] = None
    baseline_year: int = 2024
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# SDG Indicator Model
class SDGIndicatorModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    digital_twin_id: str
    sdg_number: int
    sdg_name: str
    indicator_code: str
    indicator_name: str
    baseline_value: float
    unit: str
    target_value: float
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Organization Model
class OrganizationModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    type: str
    description: Optional[str] = None
    focus_sdgs: List[int] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Project Model
class ProjectModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    organization_id: str
    digital_twin_id: Optional[str] = None
    title: str
    description: str
    target_sdgs: List[int]
    budget: float
    timeline_months: int
    status: str = "Planning"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Simulation Model
class SimulationModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    digital_twin_id: str
    project_id: Optional[str] = None
    scenario_type: str
    simulation_name: str
    funding_percentage: float = 100.0
    timeline_years: int = 5
    delay_months: int = 0
    scale_factor: float = 1.0
    predicted_outcomes: Dict
    affected_population: int
    confidence_score: float
    explanation: str
    policy_insight: str
    risk_warning: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# Partnership Model
class PartnershipModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    requesting_org_id: str
    target_org_id: str
    project_id: str
    message: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
