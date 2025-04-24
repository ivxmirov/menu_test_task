from django import template
from django.urls import resolve
from menu.models import Menu, MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_slug):
    request = context['request']
    current_path = request.path
    
    try:
        menu = Menu.objects.get(slug=menu_slug)
        items = menu.items.all()
        
        # Определяем активный пункт
        active_item = None
        for item in items:
            if item.url == current_path or (item.named_url and resolve(current_path).url_name == item.named_url):
                active_item = item
                break
        
        return {'items': items, 'active': active_item}
    except Menu.DoesNotExist:
        return {}
