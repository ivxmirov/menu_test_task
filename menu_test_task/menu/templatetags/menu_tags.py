from django import template
from django.urls import resolve, Resolver404
from ..models import MenuItem

register = template.Library()


@register.inclusion_tag('menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path_info

    try:
        resolved_url = resolve(current_url)
        resolved_url_name = resolved_url.url_name
    except Resolver404:
        resolved_url_name = None

    menu_items = MenuItem.objects.filter(
        menu_name=menu_name).select_related('parent')

    active_items = []
    for item in menu_items:
        if (
            item.url == current_url
                or item.named_url and item.named_url == resolved_url_name
                ):
            active_items.append(item)

    parent_ids = set()
    for item in active_items:
        parent = item.parent
        while parent:
            parent_ids.add(parent.id)
            parent = parent.parent

    return {
        'menu_items': menu_items,
        'active_items': active_items,
        'parent_ids': parent_ids,
        'menu_name': menu_name,
        'current_url': current_url,
        'resolved_url_name': resolved_url_name,
    }
