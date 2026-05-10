K_OPTIMO = 4
K_MIN = 2
K_MAX = 10

FEATURES = [
    'discounted_price',
    'actual_price',
    'discount_percentage',
    'rating',
    'rating_count',
]

FEATURE_LABELS = [
    'Precio\nDescontado',
    'Precio\nReal',
    'Descuento\n(%)',
    'Rating',
    'N° Reseñas',
]

PALETTE = [
    '#E63946', '#457B9D', '#2A9D8F', '#E9C46A', '#F4A261', '#264653',
    '#9B5DE5', '#F15BB5', '#00BBF9', '#06D6A0',
]

CLUSTER_DESCRIPTIONS = {
    1: (
        'Segmento intermedio',
        'Precios medios (₹3.000–₹6.000) con descuentos razonables (30–40%) '
        'y popularidad moderada. Representan gran parte del catálogo general '
        'con buena relación calidad-precio.',
    ),
    2: (
        'Productos baratos con alto descuento',
        'Precio final bajo (₹1.000–₹3.000) con descuentos muy agresivos (60–80%). '
        'El descuento es el principal mecanismo de atracción. Contiene la mayor '
        'cantidad de productos del catálogo.',
    ),
    3: (
        'Productos premium de nicho',
        'Precio elevado (> ₹10.000) con descuentos bajos (20–30%) y pocas reseñas. '
        'Son artículos especializados o de lujo con una audiencia reducida pero '
        'con buen desempeño en rating.',
    ),
    4: (
        'Productos estrella — alta popularidad',
        'Concentra los productos con mayor número de reseñas (miles) y ratings altos '
        '(> 4.2). Precios medios (₹500–₹3.000) y descuentos competitivos (40–60%). '
        'Constituyen el núcleo del volumen de ventas del catálogo.',
    ),
}
