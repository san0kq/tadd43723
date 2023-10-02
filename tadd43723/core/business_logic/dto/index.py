from dataclasses import dataclass

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class DataJsonDTO:
    attachment: InMemoryUploadedFile
