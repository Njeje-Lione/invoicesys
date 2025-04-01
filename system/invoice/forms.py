from django import forms 
from .models import Client, Invoice, InvoiceItem

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email','phone']
    
    def __init__(self, *args, ** kwargs) :
        super(ClientForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client']

    def __init__(self, *args, ** kwargs) :
        super(InvoiceForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['name','quantity','price']

    def __init__(self, *args, ** kwargs) :
        super(InvoiceItemForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'