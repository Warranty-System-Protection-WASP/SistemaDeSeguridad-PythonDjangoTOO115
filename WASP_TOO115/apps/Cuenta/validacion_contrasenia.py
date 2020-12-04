from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class ValidadorPersonalizado():

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        caracteres_especiales = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if len(password) < 12:
            raise ValidationError(_('La contraseña debe contener una lóngitud de al menos %(min_length)d caracteres.') % {'min_length': 12})
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('La contraseña debe contener al menos %(min_length)d número.') % {'min_length': self.min_length})
        if not any(char.islower() for char in password):
            raise ValidationError(_('La contraseña debe contener al menos %(min_length)d letra minúscula.') % {'min_length': self.min_length})
        if not any(char.isupper() for char in password):
            raise ValidationError(_('La contraseña debe contener al menos %(min_length)d letra mayúscula.') % {'min_length': self.min_length})
        if not any(char in caracteres_especiales for char in password):
            raise ValidationError(_('La contraseña debe contener al menos %(min_length)d caracter especial.') % {'min_length': self.min_length})

    def get_help_text(self):
        return ""
