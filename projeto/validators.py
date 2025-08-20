from django.core.exceptions import ValidationError
import re


# CPF Validator
def validate_cpf(value):
    if not re.match(r"\d{11}$", value):
        raise ValidationError("CPF must contain exactly 11 digits.")


# Phone Validator
def validate_phone(value):
    if not re.match(r"^\(\d{2}\) \d{4,5}-\d{4}$", value):
        raise ValidationError("Phone number must be in the format (XX) XXXXX-XXXX.")


# Add these validation functions at the top of the file
def validate_nota(value):
    if not -100 <= value <= 100:
        raise ValidationError("Nota deve estar entre -100 e 100.")
