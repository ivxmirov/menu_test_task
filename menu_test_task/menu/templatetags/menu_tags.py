from django import template
from menu.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_path = request.path

    items = MenuItem.objects.filter(
        menu_name=menu_name).select_related('parent').order_by('order')

    root_items = [item for item in items if item.parent is None]

    active_item = next((item for item in items if item.get_absolute_url(
    ) == current_path), None)

    html = render_menu_recursive(root_items, active_item)
    return html


def render_menu_recursive(items, active_item, level=0):
    html = ''

    for item in items:
        is_active = item == active_item
        is_parent_active = active_item and active_item.parent_id == item.id

        html += f'<li class="{
            "active" if is_active or is_parent_active else ""
        }">'
        html += f'<a href="{item.get_absolute_url()}">{item.title}</a>'

        if item.children.exists() or (is_active or is_parent_active):
            html += '<ul>'
            html += render_menu_recursive(
                item.children.all(), active_item, level+1)
            html += '</ul>'

        html += '</li>'

    return html
