from django import forms


class DateTimeForm(forms.Form):
    datetime = forms.DateTimeField(required=True)

    class Meta:
        widgets = {
            'datetime': forms.widgets.DateTimeInput(attrs={'type': 'date'})
        }
