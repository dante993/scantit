from django.forms import Form, CharField, TextInput

class LoginForm(Form):
    username = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "placeholder": "Nombre de usuario",
                                                           "autofocus": True}))
    password = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "form-control",
                                                           "type": "password",
                                                           "placeholder": "Contrasenia"}))
