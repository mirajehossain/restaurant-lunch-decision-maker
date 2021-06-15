from rest_framework.exceptions import ValidationError


class NonNegative(object):
    def __init__(self, field):
        self.field = str(field)

    def __call__(self, value):
        if value < 0:
            raise ValidationError(f'{self.field} cannot be negative.')
