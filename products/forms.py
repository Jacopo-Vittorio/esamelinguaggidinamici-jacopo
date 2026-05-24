from crispy_forms.layout import Submit
from django import forms
from django.forms import IntegerField, CharField, ChoiceField

from products.models import Prodotti, Categoria, Review, Report
from crispy_forms.helper import FormHelper

from user_manage.models import Owner


class ProdottiForm(forms.ModelForm):

    helper = FormHelper() #inizializzo un nuovo attributo che inizializza form helper.
    helper.form_id = 'products_crispy_form'
    helper.form_method = 'POST' #questo perchè poi oglio evitare di scrivere i form nell'html con {% crispy %}
    helper.add_input(Submit('submit','Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Prodotti
        #Nelle sllide abbiamo visto mettere le tuple mentre poi a lezione usiamo le liste
        #La situazione è la stessa  e non cambia nulla. Si usa la tupla per evitare i
        # duplicati dello stesso campo
        fields = ['categoria' ,'name', 'dimensione','tipo_materiale', 'price', 'image']

class ReviewForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit','Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Review
        fields = ['comment_name','comment_body','rating_fornitore','rating_prodotto']


class SearchForm(forms.Form):

    nome = CharField(required=True)
    material = CharField(required=False)
    min_price = IntegerField(required=False,min_value=0)
    max_price = IntegerField(required=False,min_value=0)


class Lista_fornitoreForm(forms.Form):
    helper = FormHelper()

    nome = CharField(required=True)

class Lista_RevForm(forms.Form):
    nome = CharField(required=True)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['text']