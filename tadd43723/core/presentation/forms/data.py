from django import forms

from core.presentation.validators import ValidateFileSize, ValidateFileExtension


class DataForm(forms.Form):
    attachment = forms.FileField(
        label='JSON File',
        allow_empty_file=False,
        validators=[ValidateFileExtension(['json']), ValidateFileSize(max_size=5_000_000)]
    )
