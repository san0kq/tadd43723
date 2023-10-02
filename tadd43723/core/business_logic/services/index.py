from __future__ import annotations

from typing import TYPE_CHECKING
import json
from pydantic import ValidationError

from core.business_logic.exceptions import DataJsonFormatError
from core.business_logic.schemas import DataJsonSchema
from core.models import Record

if TYPE_CHECKING:
     from core.business_logic.dto import DataJsonDTO

def process_and_save_json(data: DataJsonDTO) -> None:
    with data.attachment as file:
        try:
            data = json.loads(file.read().decode('utf-8'))
        except json.JSONDecodeError:
            raise DataJsonFormatError('Invalid format in the file. Something wrong with json.')

        records_to_save: list[Record] = []
        
        if not isinstance(data, list):
            raise DataJsonFormatError('Invalid format in the file. The main JSON object should be an array.')
        
        for record in data:
            try:
                record = DataJsonSchema(**record)
                records_to_save.append(
                    Record(name=record.name, date=record.date)
                )
            except TypeError:
                raise DataJsonFormatError('Invalid format in the file. In the main array, there should be objects '
                                          'with data, not another array.')
            except ValidationError:
                raise DataJsonFormatError('Invalid format in the file. Keys "name" and "date" are required and '
                                          'must be in a specific format.')
            
        Record.objects.bulk_create(records_to_save)
