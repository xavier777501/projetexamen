from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class PurchaseCreate(BaseModel):
    product_name: str = Field(..., min_length=1, description="Nom du produit obligatoire")
    price: float = Field(..., gt=0, description="Prix invalide")
    purchase_date: Optional[datetime] = None

    @validator('product_name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Nom du produit obligatoire')
        return v.strip()

    @validator('purchase_date', pre=True, always=True)
    def set_date(cls, v):
        return v or datetime.utcnow()

class PurchaseResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float
    purchase_date: datetime

    class Config:
        orm_mode = True
