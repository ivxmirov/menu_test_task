from .models import MenuItem


def menus(request):
    return {
        'all_menus': MenuItem.objects.values_list(
            'menu_name', flat=True).distinct()
    }
