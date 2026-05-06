import io
import base64

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from .config import PALETTE, FEATURE_LABELS

_elbow_chart_cache = {}
_clusters_chart_cache = {}
_centroids_chart_cache = {}
_distribution_chart_cache = {}


def _encode(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=110)
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return data


def elbow_chart(inertias, k_optimo):
    if k_optimo in _elbow_chart_cache:
        return _elbow_chart_cache[k_optimo]

    k_range = range(1, len(inertias) + 1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(list(k_range), inertias, 'o-', color='#457B9D', linewidth=2, markersize=7)
    ax.axvline(x=k_optimo, color='#E63946', linestyle='--', linewidth=1.8,
               label=f'K óptimo = {k_optimo}')
    ax.set_xlabel('Número de Clústeres (K)', fontsize=12)
    ax.set_ylabel('Inercia', fontsize=12)
    ax.set_title('Método del Codo — Selección de K', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.set_xticks(list(k_range))
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    _elbow_chart_cache[k_optimo] = _encode(fig)
    return _elbow_chart_cache[k_optimo]


def clusters_chart(X_pca, labels, centroids_pca, n_clusters, variance):
    if n_clusters in _clusters_chart_cache:
        return _clusters_chart_cache[n_clusters]

    fig, ax = plt.subplots(figsize=(9, 6))
    for c in range(n_clusters):
        mask = labels == c
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                   c=PALETTE[c], alpha=0.55, s=40, label=f'Clúster {c}', edgecolors='none')
    ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1],
               c='black', marker='X', s=200, zorder=5, label='Centroides')
    ax.set_xlabel(f'PC1 ({variance[0]}% varianza)', fontsize=11)
    ax.set_ylabel(f'PC2 ({variance[1]}% varianza)', fontsize=11)
    ax.set_title('Visualización de Clústeres (PCA 2D)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()

    _clusters_chart_cache[n_clusters] = _encode(fig)
    return _clusters_chart_cache[n_clusters]


def centroids_chart(centroids_orig, n_clusters):
    if n_clusters in _centroids_chart_cache:
        return _centroids_chart_cache[n_clusters]

    values = centroids_orig.values
    normalized = MinMaxScaler().fit_transform(values)

    x = np.arange(len(FEATURE_LABELS))
    width = 0.8 / n_clusters
    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(n_clusters):
        offset = (i - n_clusters / 2 + 0.5) * width
        ax.bar(x + offset, normalized[i], width, label=f'Clúster {i}',
               color=PALETTE[i], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(FEATURE_LABELS, fontsize=11)
    ax.set_ylabel('Valor normalizado [0–1]', fontsize=11)
    ax.set_title('Perfil de Centroides por Clúster', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, axis='y', alpha=0.3)
    fig.tight_layout()

    _centroids_chart_cache[n_clusters] = _encode(fig)
    return _centroids_chart_cache[n_clusters]


def distribution_chart(labels, n_clusters):
    if n_clusters in _distribution_chart_cache:
        return _distribution_chart_cache[n_clusters]

    counts = np.bincount(labels, minlength=n_clusters)
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(
        [f'Clúster {c}' for c in range(n_clusters)],
        counts, color=PALETTE[:n_clusters], alpha=0.9, edgecolor='white',
    )
    for bar, cnt in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                str(cnt), ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_ylabel('Número de productos', fontsize=11)
    ax.set_title('Distribución por Clúster', fontsize=13, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)
    fig.tight_layout()

    _distribution_chart_cache[n_clusters] = _encode(fig)
    return _distribution_chart_cache[n_clusters]
