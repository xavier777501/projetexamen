import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home'); // 'home', 'add-purchase'
  const [formData, setFormData] = useState({
    product_name: '',
    price: '',
    purchase_date: new Date().toISOString().split('T')[0]
  });
  const [message, setMessage] = useState({ type: '', text: '' });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!formData.product_name.trim()) newErrors.product_name = "Nom du produit obligatoire";
    if (!formData.price || isNaN(formData.price) || parseFloat(formData.price) <= 0) {
      newErrors.price = "Prix invalide";
    }
    if (!formData.purchase_date) newErrors.purchase_date = "Date invalide";
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });

    if (!validate()) return;

    try {
      const response = await fetch('http://localhost:8000/purchases', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_name: formData.product_name,
          price: parseFloat(formData.price),
          purchase_date: formData.purchase_date
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage({ type: 'success', text: 'Produit ajouté avec succès' });
        setFormData({
          product_name: '',
          price: '',
          purchase_date: new Date().toISOString().split('T')[0]
        });
      } else {
        if (data.detail && Array.isArray(data.detail)) {
          const apiErrors = {};
          data.detail.forEach(err => {
            if (err.loc.includes('product_name')) apiErrors.product_name = "Nom du produit obligatoire";
            if (err.loc.includes('price')) apiErrors.price = "Prix invalide";
          });
          setErrors(apiErrors);
        } else {
          setMessage({ type: 'error', text: data.message || 'Une erreur est survenue' });
        }
      }
    } catch (err) {
      setMessage({ type: 'error', text: 'Impossible de contacter le serveur' });
    }
  };

  const renderHome = () => (
    <div className="home-container">
      <h1>🛒 Family Grocery</h1>
      <p className="subtitle">Modernisez la gestion de vos courses quotidiennes</p>
      
      <div className="actions-grid">
        <div className="action-card" onClick={() => setCurrentView('add-purchase')}>
          <div className="icon-box">➕</div>
          <h3>Ajouter un achat</h3>
          <p>Enregistrez vos nouvelles dépenses</p>
        </div>
        
        <div className="action-card disabled">
          <div className="icon-box">📜</div>
          <h3>Historique</h3>
          <p>Consultez vos achats passés</p>
        </div>
        
        <div className="action-card disabled">
          <div className="icon-box">📊</div>
          <h3>Statistiques</h3>
          <p>Analysez vos habitudes</p>
        </div>
        
        <div className="action-card disabled">
          <div className="icon-box">💰</div>
          <h3>Budget</h3>
          <p>Suivez vos dépenses totales</p>
        </div>
      </div>
    </div>
  );

  const renderAddPurchase = () => (
    <div className="form-container">
      <div className="header-row">
        <button className="btn-back" onClick={() => {
          setCurrentView('home');
          setMessage({ type: '', text: '' });
          setErrors({});
        }}>← Retour</button>
        <h2>Nouvel Achat</h2>
      </div>

      <form onSubmit={handleSubmit} noValidate>
        <div className="form-group">
          <label>Nom du produit</label>
          <input
            type="text"
            value={formData.product_name}
            onChange={(e) => setFormData({...formData, product_name: e.target.value})}
            className={errors.product_name ? 'error' : ''}
            placeholder="Ex: Lait, Pain, Pommes..."
          />
          {errors.product_name && <span className="error-text">{errors.product_name}</span>}
        </div>

        <div className="form-group">
          <label>Prix (€)</label>
          <input
            type="number"
            step="0.01"
            value={formData.price}
            onChange={(e) => setFormData({...formData, price: e.target.value})}
            className={errors.price ? 'error' : ''}
            placeholder="0.00"
          />
          {errors.price && <span className="error-text">{errors.price}</span>}
        </div>

        <div className="form-group">
          <label>Date d'achat</label>
          <input
            type="date"
            value={formData.purchase_date}
            onChange={(e) => setFormData({...formData, purchase_date: e.target.value})}
            className={errors.purchase_date ? 'error' : ''}
          />
          {errors.purchase_date && <span className="error-text">{errors.purchase_date}</span>}
        </div>

        <button type="submit" className="btn-submit">Confirmer l'ajout</button>
      </form>

      {message.text && (
        <div className={`alert ${message.type}`}>
          {message.text}
        </div>
      )}
    </div>
  );

  return (
    <div className="app-wrapper">
      <div className="glass-panel">
        {currentView === 'home' && renderHome()}
        {currentView === 'add-purchase' && renderAddPurchase()}
      </div>
    </div>
  );
}

export default App;
