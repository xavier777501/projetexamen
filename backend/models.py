from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)

    # Relation avec les produits
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relations
    category = relationship("Category", back_populates="products")
    purchases = relationship("Purchase", back_populates="product")

    def __repr__(self):
        return f"<Product(name='{self.name}')>"

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=False) # Ajout de la quantité pour plus de réalisme
    purchase_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relation avec le produit
    product = relationship("Product", back_populates="purchases")

    def __repr__(self):
        return f"<Purchase(product_id={self.product_id}, price={self.price}, date={self.purchase_date})>"
