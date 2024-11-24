from django.contrib.auth.forms import UserCreationForm
from django.db.models.expressions import result
from django.db.transaction import atomic
from django.forms import CharField, Textarea, ModelForm
from django.http import request

from accounts.models import Profile, AdminRequestMessage


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name']

    biography = CharField(label='Tell us your story: ', widget=Textarea)

    # @atomic o sa ne asigure ca nu se intampla schimbari in baza de date
    # doar daca nu sunt erori
    @atomic
    def save(self, commit=True):
        # Salvam obiectul User care vine la pachet cu Django
        result = super().save(commit)

        biography = self.cleaned_data['biography']

        # Cream un obiect Profil in care adaugam datele noastre in plus
        # fata de un utilizator simplu (biography) + user-ul creat inainte
        # si il salvam
        profile = Profile(biography=biography, user=result)
        if commit:
            profile.save()
        return result

class AdminRequestMessageForm(ModelForm):
    class Meta:
        model = AdminRequestMessage
        fields = ['message']
        widgets = {
            'message': Textarea(attrs={'placeholder': 'Write your message here...'}),
        }