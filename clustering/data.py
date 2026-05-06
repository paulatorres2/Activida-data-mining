import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from .config import FEATURES

_cache = None


def load():
    global _cache
    if _cache is not None:
        return _cache

    df = pd.read_csv('amazon.csv')

    df['discounted_price'] = pd.to_numeric(
        df['discounted_price'].str.replace('[₹,]', '', regex=True), errors='coerce'
    )
    df['actual_price'] = pd.to_numeric(
        df['actual_price'].str.replace('[₹,]', '', regex=True), errors='coerce'
    )
    df['discount_percentage'] = pd.to_numeric(
        df['discount_percentage'].str.replace('%', '', regex=False), errors='coerce'
    )
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_count'] = pd.to_numeric(
        df['rating_count'].str.replace(',', '', regex=False), errors='coerce'
    )

    df = (
        df[FEATURES + ['product_name', 'category']]
        .dropna(subset=FEATURES)
        .query('discounted_price > 0 and actual_price > 0 and rating_count > 0')
        .copy()
        .reset_index(drop=True)
    )
    df['rating_count'] = df['rating_count'].clip(upper=df['rating_count'].quantile(0.99))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[FEATURES].values)

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    _cache = {
        'df': df,
        'X_scaled': X_scaled,
        'X_pca': X_pca,
        'pca': pca,
        'scaler': scaler,
    }
    return _cache
