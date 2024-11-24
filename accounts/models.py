from django.db.models import Model, OneToOneField, TextField, CASCADE
from django.contrib.auth.models import User

# Create your models here.
class Profile(Model):
    # OneToOne field insemna ca fiecare user este asociat cu un singur profil si vice-versa
    # on_delete CASCADE inseamna ca atunci cand stergem un user, se va sterge automat
    # si obiectul Profile asociat lui
    user = OneToOneField(User, on_delete=CASCADE)
    biography = TextField()

    def __str__(self):
        return self.user.username
