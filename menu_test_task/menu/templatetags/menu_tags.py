from django import template
from django.urls import resolve
from ..models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path
    
    # Получаем все элементы меню одним запросом
    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('order')
    
    # Создаем древовидную структуру
    menu_tree = {}
    for item in items:
        if item.parent_id is None:
            menu_tree[item.id] = {'item': item, 'children': []}
        else:
            if item.parent_id in menu_tree:
                menu_tree[item.parent_id]['children'].append({'item': item, 'children': []})
    
    # Определяем активный элемент
    active_item = None
    for item in items:
        if item.get_absolute_url() == current_path:
            active_item = item
            break
    
    # Формируем HTML
    html = ''
    for root in menu_tree.values():
        html += render_menu_item(root, active_item, 0)
    
    return html

def render_menu_item(item_data, active_item, level):
    item = item_data['item']
    is_active = item == active_item
    has_active_child = any(child['item'] == active_item for child in item_data['children'])
    
    # Определяем, нужно ли показывать подменю
    show_children = is_active or has_active_child or (active_item and item.id == active_item.parent_id)
    
    html = f'<li class="menu-item level-{level}{" active" if is_active or has_active_child else ""}">'
    html += f'<a href="{item.get_absolute_url()}">{item.name}</a>'
    
    if show_children and item_data['children']:
        html += '<ul class="submenu">'
        for child in item_data['children']:
            html += render_menu_item(child, active_item, level + 1)
        html += '</ul>'
    
    html += '</li>'
