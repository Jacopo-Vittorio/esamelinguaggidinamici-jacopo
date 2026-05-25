from django.db.models import Case, IntegerField, Q, Value, When

from checkout.models import OrderItem
from products.models import Prodotti, SearchHistory


def get_suggested_products(user, limit=8):
    if not user.is_authenticated:
        return Prodotti.objects.none()

    bought_items = OrderItem.objects.filter(order__user=user).select_related(
        'product',
        'product__categoria',
    )

    if not bought_items.exists():
        return (
            Prodotti.objects
            .select_related('owner__user', 'categoria')
            .order_by('?')[:min(3, limit)]
        )

    bought_product_ids = list(bought_items.values_list('product_id', flat=True))
    bought_category_ids = list(
        bought_items.values_list('product__categoria_id', flat=True).distinct()
    )
    bought_materials = [
        material for material in bought_items.values_list('product__tipo_materiale', flat=True).distinct()
        if material
    ]
    recent_searches = SearchHistory.objects.filter(user=user)[:5]

    search_query = Q()
    for search in recent_searches:
        if search.query:
            search_query |= Q(name__icontains=search.query)
        if search.material:
            search_query |= Q(tipo_materiale__icontains=search.material)

    signals = Q()
    if bought_category_ids:
        signals |= Q(categoria_id__in=bought_category_ids)
    if bought_materials:
        signals |= Q(tipo_materiale__in=bought_materials)
    signals |= search_query

    if not signals:
        return Prodotti.objects.none()

    queryset = (
        Prodotti.objects
        .select_related('owner__user', 'categoria')
        .filter(signals)
        .exclude(id__in=bought_product_ids)
        .distinct()
    )

    return queryset.annotate(
        suggestion_score=Case(
            When(categoria_id__in=bought_category_ids, then=Value(3)),
            When(tipo_materiale__in=bought_materials, then=Value(2)),
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('-suggestion_score', 'name')[:limit]
