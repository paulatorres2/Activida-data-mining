from flask import Blueprint, render_template, request
import clustering

analysis_bp = Blueprint('analysis', __name__)


def _resolve_k():
    source = request.form if request.method == 'POST' else request.args
    raw = source.get('k', '').strip()
    try:
        k = int(raw)
    except (ValueError, TypeError):
        return clustering.K_OPTIMO
    return max(clustering.K_MIN, min(k, clustering.K_MAX))


def _charts_for(result):
    r = result
    return {
        'clusters': clustering.clusters_chart(
            r['X_pca'], r['labels'], r['centroids_pca'],
            r['n_clusters'], r['varianza_pca'],
        ),
        'centroids': clustering.centroids_chart(r['centroids_orig'], r['n_clusters']),
        'distribution': clustering.distribution_chart(r['labels'], r['n_clusters']),
        'elbow': clustering.elbow_chart(clustering.elbow_inertias(), clustering.K_OPTIMO),
    }


@analysis_bp.route('/dataset')
def dataset():
    result = clustering.cluster(clustering.K_OPTIMO)
    return render_template('dataset.html', result=result)


@analysis_bp.route('/ejecucion', methods=['GET', 'POST'])
def ejecucion():
    k = _resolve_k()
    result = clustering.cluster(k)
    return render_template('ejecucion.html', result=result, k=k)


@analysis_bp.route('/clusters')
def clusters():
    k = _resolve_k()
    result = clustering.cluster(k)
    return render_template('clusters.html', result=result, charts=_charts_for(result), k=k)


@analysis_bp.route('/centroides')
def centroides():
    k = _resolve_k()
    result = clustering.cluster(k)
    return render_template('centroides.html', result=result, charts=_charts_for(result), k=k)


@analysis_bp.route('/codo')
def codo():
    inertias = clustering.elbow_inertias()
    chart = clustering.elbow_chart(inertias, clustering.K_OPTIMO)
    return render_template('codo.html', inertias=inertias, chart=chart,
                           k_optimo=clustering.K_OPTIMO)


@analysis_bp.route('/interpretacion')
def interpretacion():
    result = clustering.cluster(clustering.K_OPTIMO)
    descs = {
        c: clustering.CLUSTER_DESCRIPTIONS.get(
            c + 1, (f'Clúster {c+1}', 'Perfil de este segmento.')
        )
        for c in range(result['n_clusters'])
    }
    return render_template('interpretacion.html', result=result,
                           charts=_charts_for(result), cluster_descs=descs)
