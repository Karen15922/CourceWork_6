from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"


@register.filter()
def client_filter(queryset):
    if queryset:
        return ', '.join([client.email for client in queryset])
