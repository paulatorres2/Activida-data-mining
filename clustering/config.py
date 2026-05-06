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

PALETTE = ['#E63946', '#457B9D', '#2A9D8F', '#E9C46A', '#F4A261', '#264653']

CLUSTER_DESCRIPTIONS = {
    0: (
        'Productos económicos con alto descuento',
        'Agrupa productos de bajo precio final con descuentos agresivos. '
        'Son artículos de ticket pequeño que atraen compradores sensibles al precio, '
        'como accesorios y electrónicos básicos.',
    ),
    1: (
        'Productos premium con baja popularidad',
        'Agrupa productos de precio elevado con pocas reseñas. '
        'Son artículos especializados o de nicho que aún no han alcanzado '
        'volúmenes masivos pero mantienen ratings aceptables.',
    ),
    2: (
        'Productos populares y bien valorados',
        'Concentra los productos con mayor número de reseñas y ratings altos. '
        'Son los más vendidos del catálogo y representan el núcleo del negocio.',
    ),
    3: (
        'Productos de precio medio y descuento moderado',
        'Segmento intermedio: precios medios, descuentos razonables y volumen '
        'moderado de reseñas. Artículos equilibrados que combinan accesibilidad '
        'y calidad percibida.',
    ),
}
