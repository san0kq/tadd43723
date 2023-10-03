from __future__ import annotations

from typing import TYPE_CHECKING
import json
from logging import getLogger
from pydantic import ValidationError

from core.business_logic.exceptions import DataJsonFormatError
from core.business_logic.schemas import DataJsonSchema
from core.models import Record

if TYPE_CHECKING:
     from core.business_logic.dto import DataJsonDTO


logger = getLogger(__name__)


def process_and_save_json(data: DataJsonDTO) -> None:
    """
    Validation and database insertion.

    The function accepts a DTO with a JSON file, opens it, 
    and validates it against multiple parameters. Upon successful 
    validation, it proceeds to write the data into the database.

    """
    with data.attachment as file:
        try:
            data = json.loads(file.read().decode('utf-8'))
            logger.info('File opened', extra={'file_name': file.name})
        except json.JSONDecodeError as err:
            logger.error('Json decode error.', extra={'error_message': err})
            raise DataJsonFormatError('Invalid format in the file. Something wrong with json.')

        records_to_save: list[Record] = []

        if not isinstance(data, list):
            logger.error('The main JSON object Error.')
            raise DataJsonFormatError('Invalid format in the file. The main JSON object should be an array.')

        for record in data:
            try:
                record = DataJsonSchema(**record)
                records_to_save.append(
                    Record(name=record.name, date=record.date)
                )
            except TypeError as err:
                logger.error('Json format error.', extra={'error_message': err})
                raise DataJsonFormatError('Invalid format in the file. In the main array, there should be objects '
                                          'with data, not another array.')
            except ValidationError as err:
                logger.error('Json format error.', extra={'error_message': err})
                raise DataJsonFormatError('Invalid format in the file. Keys "name" and "date" are required and '
                                          'must be in a specific format.')

        Record.objects.bulk_create(records_to_save)
        logger.info('Created new records.')
