from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.core.files import File

from django.core.exceptions import ValidationError


class ValidateFileExtension:
    """
    File extension validation. 
    
    It receives a list of permitted extensions and validates the file's extension against it.

    """
    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, file: File) -> None:
        if '.' not in file.name:
            raise ValidationError(message='File must have extension.')
        file_extension = file.name.split('.')[-1]
        if file_extension not in self._available_extensions:
            raise ValidationError(message=f'Accept only {self._available_extensions}')


class ValidateFileSize:
    """
    File size validation. 
    
    Accepts a number in bytes, the maximum allowable file size.

    """
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, file: File) -> None:
        if file.size > self._max_size:
            max_size_in_mb = int(self._max_size / 1_000_000)
            raise ValidationError(message=f'Max file size is {max_size_in_mb} MB')
