from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import render

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class DataTableView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'data.html')
