from datetime import date, timedelta
from django import forms
from django.forms.widgets import NumberInput, DateInput, SelectDateWidget

from .models import Client, Invoice, Job


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'client_phone', 'client_address', 'client_contact', 
                  'client_email', 'client_account_number', 'rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.fields['client_address'].widget.attrs.update({'rows': '2'})


class InvoiceForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    class Meta:
        model = Invoice
        fields = ['client', 'invoice_date', 'due_date']
        widgets = {
            'invoice_date': SelectDateWidget,
            'due_date': SelectDateWidget
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_date'].initial = date.today()
        self.fields['due_date'].initial = date.today() + timedelta(days=30)
        # for field in self.fields:
        #     new_data = {
        #         "hx-post": ".",
        #         "hx-trigger": "keyup changed delay:500ms",
        #         "hx-target": "#invoice-container",
        #         "hx-swap": "outerHTML"
        #     }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['date_of_work', 'description', 'hours']
        widgets = {
            'date_of_work': SelectDateWidget
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_work'].initial = date.today()
