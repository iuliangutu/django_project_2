### FORMULARE
import re
from datetime import date

from django.core.exceptions import ValidationError
from django.forms import (
    CharField, DateField, Form, IntegerField, ModelChoiceField, Textarea, DateInput, ModelForm
)
from viewer.models import Genre, Movie


class DateInput(DateInput):
    input_type = 'date'

def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError("first letter must be capitalized!")

class PastDateField(DateField):
    def validate(self, value):
        super().validate(value)
        if value >= date.today():
            raise ValidationError('Movie from future')

    def clean(self, value):
        result = super().clean(value)
        # Extra validation if needed (optional)
        return date(year=result.year, month=result.month, day=result.day)

# class MyDateForm(ModelForm):

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    title = CharField(max_length=128, validators=[capitalized_validator])
    # genre = ModelChoiceField(queryset=Genre.objects)
    rating = IntegerField(min_value=1, max_value=10)
    released = PastDateField(widget=DateInput)
    ### description = CharField(required=False)
    # description = CharField(widget=Textarea)

    def clean_description(self):
        # Force each sentence of the description to be capitalized.
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)


    def clean(self):
        result = super().clean()
        if result['genre'].name == 'Comedy' and result['rating'] > 5:
            self.add_error('genre', 'mesaj eroare la field-ul genre')
            self.add_error('rating', 'mesaj eroare la field-ul rating')
            raise ValidationError(
                "Comedies not funny, rating too high"
            )
        return result
