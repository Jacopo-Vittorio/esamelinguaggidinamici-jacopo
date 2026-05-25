from decimal import Decimal

from django.db import migrations


NEW_PRODUCTS = (
    {
        'name': 'Pacchetto standard',
        'category': 'Cartoni',
        'dimensione': '30x20x15',
        'tipo_materiale': 'cartone',
        'price': Decimal('0.60'),
        'image': 'products/pacchetto-standard/pacchetto-standard.png',
    },
    {
        'name': 'Imballaggio a base fungina',
        'category': 'Biodegradabili',
        'dimensione': '30x20x15',
        'tipo_materiale': 'micelio',
        'price': Decimal('1.20'),
        'image': 'products/imballaggio-fungino/imballaggio-fungino.png',
    },
)


def get_default_owner(apps):
    User = apps.get_model('user_manage', 'User')
    Owner = apps.get_model('user_manage', 'Owner')

    owner = Owner.objects.filter(user__username='fornitore1').first()
    if owner:
        return owner

    owner = Owner.objects.first()
    if owner:
        return owner

    user, _ = User.objects.get_or_create(
        username='fornitore_demo',
        defaults={
            'is_owner': True,
            'is_client': False,
            'is_active': True,
        },
    )
    if not user.is_owner:
        user.is_owner = True
        user.save(update_fields=['is_owner'])

    owner, _ = Owner.objects.get_or_create(user=user)
    return owner


def create_new_products(apps, schema_editor):
    Categoria = apps.get_model('products', 'Categoria')
    Prodotti = apps.get_model('products', 'Prodotti')
    owner = get_default_owner(apps)

    for product_data in NEW_PRODUCTS:
        category, _ = Categoria.objects.get_or_create(nome=product_data['category'])
        Prodotti.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'owner': owner,
                'categoria': category,
                'dimensione': product_data['dimensione'],
                'tipo_materiale': product_data['tipo_materiale'],
                'price': product_data['price'],
                'image': product_data['image'],
            },
        )


def remove_new_products(apps, schema_editor):
    Prodotti = apps.get_model('products', 'Prodotti')
    product_names = [product_data['name'] for product_data in NEW_PRODUCTS]
    Prodotti.objects.filter(name__in=product_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_searchhistory'),
    ]

    operations = [
        migrations.RunPython(create_new_products, remove_new_products),
    ]
