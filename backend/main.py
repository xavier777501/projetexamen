from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
import models, database, schemas
from typing import List

# Création des tables dans la base de données
models.Base.metadata.create_all(bind=database.engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Family Grocery API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En production, remplacez par l'URL du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de gestion des courses familiales"}

@app.post("/purchases", response_model=schemas.PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(database.get_db)):
    # ... (code existant)
    db_product = db.query(models.Product).filter(models.Product.name == purchase.product_name).first()
    
    if not db_product:
        db_product = models.Product(name=purchase.product_name)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    
    new_purchase = models.Purchase(
        product_id=db_product.id,
        price=purchase.price,
        purchase_date=purchase.purchase_date
    )
    
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    
    return {
        "id": new_purchase.id,
        "product_id": db_product.id,
        "product_name": db_product.name,
        "price": new_purchase.price,
        "purchase_date": new_purchase.purchase_date
    }

@app.get("/purchases", response_model=List[schemas.PurchaseResponse])
def get_purchases(db: Session = Depends(database.get_db)):
    # Jointure pour récupérer le nom du produit et tri par date décroissante
    purchases = db.query(
        models.Purchase.id,
        models.Purchase.product_id,
        models.Product.name.label("product_name"),
        models.Purchase.price,
        models.Purchase.purchase_date
    ).join(models.Product).order_by(models.Purchase.purchase_date.desc()).all()
    
    return purchases

# Endpoint de test pour vérifier la connexion DB
@app.get("/db-check")
def check_db(db: Session = Depends(database.get_db)):
    try:
        # Tente une requête simple
        db.execute(database.text("SELECT 1"))
        return {"status": "success", "message": "Connexion à la base de données établie"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
