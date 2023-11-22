from datetime import date, timedelta
from django import forms
from django.forms.widgets import NumberInput, DateInput

from .models import Invoice, Job


class InvoiceForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    # name = forms.CharField(help_text='This is your help! <a href="/contact">Contact Us</a>')
    # name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Recipe Name"}))
    # description = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}))
    class Meta:
        model = Invoice
        fields = ['client', 'invoice_date', 'due_date']
        widgets = {
            'invoice_date': DateInput(attrs={
                'placeholder': date.today()
            }),
            'due_date': DateInput(attrs={
                'placeholder': date.today() + timedelta(days=30)
            })
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         new_data = {
    #             "placeholder": f'Invoice {str(field)}{latest_invoice_num + 1}',
    #             "class": 'form-control',
    #         }
    #         self.fields[str(field)].widget.attrs.update(new_data)
    #     # self.fields['name'].label = ''
    #     # self.fields['name'].widget.attrs.update({'class': 'form-control-2'})
    #     self.fields['client'].widget.attrs.update({'rows': '2'})
    #     self.fields['invoice_number'].widget.attrs.update({'rows': '4'})


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['date_of_work', 'description', 'hours']
