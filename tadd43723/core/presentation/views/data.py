from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import render

from core.business_logic.services import get_data_all

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class DataTableView(View):
    """
    Displaying a data table. 
    
    Supports only the GET method. Rendering an HTML page with a data table.
    
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        data = get_data_all()
        context = {'data': data}
        return render(request, 'data.html', context=context)
