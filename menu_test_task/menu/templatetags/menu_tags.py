from django import template
from ..models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('order')

    menu_tree = {}
    for item in items:
        if item.parent_id is None:
            menu_tree[item.id] = {'item': item, 'children': []}
        else:
            menu_tree[item.parent_id]['children'].append({'item': item, 'children': []})

    active_item = None
    for item in items:
        if item.get_absolute_url() == current_path:
            active_item = item
            break

    html = render_menu_tree(menu_tree, active_item)
    return html


def render_menu_tree(tree, active_item, level=0):
    html = ''
    for key, node in tree.items():
        is_active = node['item'].id == active_item.id if active_item else False
        is_parent_active = active_item and active_item.parent_id == node['item'].id

        html += f'<li class="{"active" if is_active or is_parent_active else ""}">'
        html += f'<a href="{node["item"].get_absolute_url()}">{node["item"].title}</a>'

        if node['children'] or (is_active or is_parent_active):
            html += '<ul>'
            html += render_menu_tree({c['item'].id: c for c in node['children']}, active_item, level+1)
            html += '</ul>'

        html += '</li>'
    return html
