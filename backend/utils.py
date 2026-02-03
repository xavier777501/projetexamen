from typing import List, Dict

def get_most_frequent_products(product_names: List[str]) -> List[Dict]:
    """
    Calcule le(s) produit(s) le(s) plus fréquent(s) dans une liste.
    Retourne une liste de dictionnaires avec 'name' et 'count'.
    """
    if not product_names:
        return []
    
    counts = {}
    for name in product_names:
        counts[name] = counts.get(name, 0) + 1
    
    max_count = max(counts.values())
    
    top_products = [
        {"name": name, "count": count} 
        for name, count in counts.items() 
        if count == max_count
    ]
    
    return top_products
