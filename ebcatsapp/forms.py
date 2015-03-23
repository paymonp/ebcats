from django import forms

class CategoriesForm(forms.Form):
    checkboxes = forms.MultipleChoiceField(required=False,
                              widget=forms.CheckboxSelectMultiple)