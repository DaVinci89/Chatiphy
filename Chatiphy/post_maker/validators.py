from django import forms


def validate_not_empty(value):
    if value == "":
        raise forms.ValidationError("The field shouldn't be empty!", params={"value": value})
