import django_filters
from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Category


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='cat_subject',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='любая'

    )

    added_after = DateTimeFilter(
        field_name='create_date',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
        label='Создана позже чем:',
    )

    title = django_filters.CharFilter(
        field_name='article_header',
        label='Содержит в заголовке',
        lookup_expr='icontains',
    )
