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

@register.filter()
def mailing_attempt_filter(mailings):
    mailings.filter(mailing_attempt__isnull=True)
    return mailings

@register.filter()
def mailing_attempt_display(attempt):
    return f"{attempt.date_attempt.strftime("%Y-%m-%d %H:%M:%S")} {attempt.status} {attempt.smtp_service_report}"

@register.filter()
def attempt_count_filter(attempts):
    return len(attempts)

