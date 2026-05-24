from crispy_forms.layout import Submit
from django import forms
from django.forms import IntegerField, CharField, ChoiceField

from forum.models import Forum, Risposta
from products.models import Prodotti, Categoria, Review, Report
from crispy_forms.helper import FormHelper

class ForumForm(forms.ModelForm):

    helper = FormHelper() #inizializzo un nuovo attributo che inizializza form helper.

    helper.form_method = 'POST' #questo perchè poi oglio evitare di scrivere i form nell'html con {% crispy %}
    helper.add_input(Submit('submit','Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Forum

        fields = ['fornitore','titolo','descrizione','contenuto']

class RispostaForm(forms.ModelForm):

    helper = FormHelper() #inizializzo un nuovo attributo che inizializza form helper.
    helper.form_method = 'POST' #questo perchè poi oglio evitare di scrivere i form nell'html con {% crispy %}
    helper.add_input(Submit('submit','Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Risposta
        fields = ['commento']