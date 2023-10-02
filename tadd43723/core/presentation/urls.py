from django.urls import path

from core.presentation.views import IndexView, DataTableView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('table/', DataTableView.as_view(), name='data-table'),
]
