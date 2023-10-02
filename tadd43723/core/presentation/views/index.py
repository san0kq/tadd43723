from __future__ import annotations

from typing import TYPE_CHECKING

from django.views import View
from django.shortcuts import redirect, render

from core.presentation.forms import DataForm
from core.presentation.converters import convert_data_from_request_to_dto
from core.business_logic.services import process_and_save_json
from core.business_logic.dto import DataJsonDTO

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = DataForm()
        context = {'form': form}
        return render(request, 'index.html', context=context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        form = DataForm(request.POST, files=request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            data = convert_data_from_request_to_dto(dto=DataJsonDTO, data_from_request=form.cleaned_data)
            process_and_save_json(data=data)
            return redirect('data-table')

        else:
            context = {'form': form}
            return render(request, 'index.html', context=context)
