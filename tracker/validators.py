from django.core.exceptions import ValidationError

def validate_summary_length(value):
        if len(value) < 5:
            raise ValidationError(
                'Описание должно содержать минимум 5 символов'
            )

def validate_no_test_word(value):
    if 'testo' in value.lower():
        raise ValidationError(
            'Слово testo использовать нельзя'
        )