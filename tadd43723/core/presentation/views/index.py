from __future__ import annotations

from typing import TYPE_CHECKING
from logging import getLogger

from django.views import View
from django.shortcuts import redirect, render

from core.presentation.forms import DataForm
from core.presentation.converters import convert_data_from_request_to_dto
from core.business_logic.services import process_and_save_json
from core.business_logic.dto import DataJsonDTO
from core.business_logic.exceptions import DataJsonFormatError

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


logger = getLogger(__name__)


class IndexView(View):
    """
    Controller with a form for uploading a JSON file.

    Responsible for form validation and handling errors from the business logic function. 
    Upon successful validation, redirects to a page with a table.

    """
    def get(self, request: HttpRequest) -> HttpResponse:
        form = DataForm()
        context = {'form': form}
        return render(request, 'index.html', context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = DataForm(request.POST, files=request.FILES)
        if form.is_valid():
            data = convert_data_from_request_to_dto(dto=DataJsonDTO, data_from_request=form.cleaned_data)
            try:
                process_and_save_json(data=data)
            except DataJsonFormatError as err:
                logger.error('Json format error.', extra={'error_message': err})
                form.add_error(error=err, field=None)
                context = {'form': form}
                return render(request, 'index.html', context=context)
            return redirect('data-table')

        else:
            context = {'form': form}
            return render(request, 'index.html', context=context)
