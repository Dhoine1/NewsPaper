from django import template

register = template.Library()

@register.filter()
def censor(value):
    mat_list = ('хуй', 'хуев', 'хуё', 'хуи', 'хуя', 'пизд', 'бля', 'муда', 'пидор', 'пидар')

    for i in mat_list:
        if i in value.lower():
            value = value.replace(i, "***")
    return f'{value}'