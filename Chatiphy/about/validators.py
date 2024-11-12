from django import forms
# Forms validate

def validate_not_empty(value):
    if value == "":
        raise forms.ValidationError("The field shouldn't be empty!", params={"value": value})
