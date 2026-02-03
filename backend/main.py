from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text, and_
from sqlalchemy.orm import Session
import models, database, schemas, utils
from typing import List, Optional
from datetime import date

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

@app.get("/stats/top-product")
def get_top_product(
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Product.name).join(models.Purchase)
    
    filters = []
    if start_date:
        filters.append(models.Purchase.purchase_date >= start_date)
    if end_date:
        filters.append(models.Purchase.purchase_date <= end_date)
        
    if filters:
        query = query.filter(and_(*filters))
        
    product_names = [row[0] for row in query.all()]
    
    top_products = utils.get_most_frequent_products(product_names)
    
    if not top_products:
        return {"message": "Aucun produit acheté dans cette période", "top_products": []}
        
    return {
        "period": {"start": start_date, "end": end_date},
        "top_products": top_products
    }

# Endpoint de test pour vérifier la connexion DB
@app.get("/db-check")
def check_db(db: Session = Depends(database.get_db)):
    try:
        # Tente une requête simple
        db.execute(database.text("SELECT 1"))
        return {"status": "success", "message": "Connexion à la base de données établie"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
