import threading
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from .config import FEATURES, K_MAX
from .data import load

_elbow_cache = None
_cluster_cache = {}
_elbow_lock = threading.Lock()
_cluster_lock = threading.Lock()


def elbow_inertias():
    global _elbow_cache
    if _elbow_cache is not None:
        return _elbow_cache
    with _elbow_lock:
        if _elbow_cache is not None:
            return _elbow_cache
        data = load()
        _elbow_cache = [
            KMeans(n_clusters=k, random_state=42, n_init=10).fit(data['X_scaled']).inertia_
            for k in range(1, K_MAX + 1)
        ]
    return _elbow_cache


def cluster(n_clusters):
    if n_clusters in _cluster_cache:
        return _cluster_cache[n_clusters]
    with _cluster_lock:
        if n_clusters in _cluster_cache:
            return _cluster_cache[n_clusters]

        data = load()
        df = data['df'].copy()
        X_scaled = data['X_scaled']
        X_pca = data['X_pca']
        pca = data['pca']
        scaler = data['scaler']

        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        df['cluster'] = labels

        centroids_scaled = km.cluster_centers_
        centroids_orig = pd.DataFrame(
            scaler.inverse_transform(centroids_scaled), columns=FEATURES
        )

        result = {
            'labels': labels,
            'X_pca': X_pca,
            'centroids_pca': pca.transform(centroids_scaled),
            'centroids_orig': centroids_orig,
            'centroids_rows': centroids_orig.round(2).to_dict(orient='records'),
            'summary': _build_summary(df, labels, n_clusters),
            'tabla': _build_tabla(df),
            'n_clusters': n_clusters,
            'varianza_pca': [round(v * 100, 1) for v in pca.explained_variance_ratio_],
            'total_registros': len(df),
        }
        _cluster_cache[n_clusters] = result
    return result


def _build_summary(df, labels, n_clusters):
    return {
        c: {
            'count': int(np.sum(labels == c)),
            'precio_promedio': round(df.loc[labels == c, 'discounted_price'].mean(), 0),
            'rating_promedio': round(df.loc[labels == c, 'rating'].mean(), 2),
            'descuento_promedio': round(df.loc[labels == c, 'discount_percentage'].mean(), 1),
            'resenas_promedio': round(df.loc[labels == c, 'rating_count'].mean(), 0),
        }
        for c in range(n_clusters)
    }


def _build_tabla(df):
    t = df[['product_name', 'category'] + FEATURES + ['cluster']].copy()
    t.columns = [
        'Producto', 'Categoría',
        'Precio Dto. (₹)', 'Precio Real (₹)', 'Descuento (%)',
        'Rating', 'N° Reseñas', 'Clúster',
    ]
    t['Precio Dto. (₹)'] = t['Precio Dto. (₹)'].round(0).astype(int)
    t['Precio Real (₹)'] = t['Precio Real (₹)'].round(0).astype(int)
    t['Descuento (%)'] = t['Descuento (%)'].round(1)
    t['Rating'] = t['Rating'].round(2)
    t['N° Reseñas'] = t['N° Reseñas'].round(0).astype(int)
    t['Producto'] = t['Producto'].str[:60] + '...'
    return t.to_dict(orient='records')
