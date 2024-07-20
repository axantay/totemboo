from django import template
from ..models import Category, FavouriteProducts

register = template.Library()


@register.simple_tag()
def get_categories():
    categories = Category.objects.filter(parent=None)
    return categories


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Price',
            'sorters': [
                ['price', 'ascending'],
                ['-price', 'descending']
            ]
        },
        {
            'title': 'Colour',
            'sorters': [
                ['colour', 'A-Z'],
                ['-colour', 'Z-A']
            ]
        },
        {
            'title': 'Size',
            'sorters': [
                ['size', 'ascending'],
                ['-size', 'descending']
            ]
        }
    ]
    return sorters


@register.simple_tag()
def get_favourite_products(user):
    fav = FavouriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products
