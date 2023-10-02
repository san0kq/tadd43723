from pydantic import BaseModel, constr, validator
from datetime import datetime


class DataJsonSchema(BaseModel):
    name: constr(max_length=49)
    date: str

    @validator('date')
    def date_format_validate(cls, value: str) -> str:
        print(cls)
        print(type(cls))
        date_format = '%Y-%m-%d_%H:%M'
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError('Invalid date format. Use "YYYY-MM-DD_HH:mm".')
        return value
