from django.db import models
from django.core.validators import RegexValidator


class Casillero(models.Model):
    # name = models.CharField(max_length=100)
    email = models.EmailField(default="example@example.com")
    password = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='La contraseña debe ser una secuencia de exactamente 4 dígitos',
                code='invalid_password'
            )
        ],
        default = '1234'
    )

    def __str__(self):
        return f"Casillero {self.id}"

# class Controller(models.Model):
#     name = models.CharField(max_length=100)
#     casilleros = models.ManyToManyField(Casillero, limit_choices_to={'id__lte': 4}, related_name='controllers')

#     def casilleros_emails(self):
#         return ", ".join([casillero.email for casillero in self.casilleros.all()])
#     casilleros_emails.short_description = 'Casilleros Emails'

#     def set_casilleros(self, datos):
#         for _ in range(1, 5):
#             print(datos[_])
        

#     def __str__(self):
#         return self.name

# class Controller(models.Model):
#     name = models.CharField(max_length=100)

#     email1 = models.EmailField(default="example@example.com")
#     password1 = models.CharField(
#         max_length=4,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{4}$',
#                 message='La contraseña debe ser una secuencia de exactamente 4 dígitos',
#                 code='invalid_password'
#             )
#         ],
#         default="1234"
#     )

#     email2 = models.EmailField(default="example@example.com")
#     password2 = models.CharField(
#         max_length=4,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{4}$',
#                 message='La contraseña debe ser una secuencia de exactamente 4 dígitos',
#                 code='invalid_password'
#             )
#         ],
#         default="1234"
#     )

#     email3 = models.EmailField(default="example@example.com")
#     password3 = models.CharField(
#         max_length=4,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{4}$',
#                 message='La contraseña debe ser una secuencia de exactamente 4 dígitos',
#                 code='invalid_password'
#             )
#         ],
#         default="1234"
#     )

#     email4 = models.EmailField(default="example@example.com")
#     password4 = models.CharField(
#         max_length=4,
#         validators=[
#             RegexValidator(
#                 regex=r'^\d{4}$',
#                 message='La contraseña debe ser una secuencia de exactamente 4 dígitos',
#                 code='invalid_password'
#             )
#         ],
#         default="1234"
#     )

#     def casilleros_emails(self):
#         return f"{self.email1}, {self.email2}, {self.email3}, {self.email4}"
#     casilleros_emails.short_description = 'Casilleros Emails'
    
