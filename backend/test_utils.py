import pytest
from utils import get_most_frequent_products

def test_get_most_frequent_products_single_winner():
    # Scénario demandé : ["pomme", "poire", "pomme"] -> pomme
    products = ["pomme", "poire", "pomme"]
    result = get_most_frequent_products(products)
    assert len(result) == 1
    assert result[0]["name"] == "pomme"
    assert result[0]["count"] == 2

def test_get_most_frequent_products_empty():
    assert get_most_frequent_products([]) == []

def test_get_most_frequent_products_ex_aequo():
    # Cas de plusieurs gagnants
    products = ["pomme", "poire", "pomme", "poire", "banane"]
    result = get_most_frequent_products(products)
    assert len(result) == 2
    names = [r["name"] for r in result]
    assert "pomme" in names
    assert "poire" in names
    assert result[0]["count"] == 2

def test_get_most_frequent_products_all_same():
    products = ["pomme", "pomme", "pomme"]
    result = get_most_frequent_products(products)
    assert len(result) == 1
    assert result[0]["name"] == "pomme"
    assert result[0]["count"] == 3
