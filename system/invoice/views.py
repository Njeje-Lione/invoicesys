from django.shortcuts import render, redirect
from .forms import ClientForm, InvoiceForm, InvoiceItemForm
from .models import Invoice,InvoiceItem,Client
from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
import random
from django.http import HttpResponse
from django.db.models import F, Sum
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string 
from xhtml2pdf import pisa


# Create your views here.
@login_required(login_url='login')  
def home(request):
    invoice_count = Invoice.objects.all().count()
    client_count = Client.objects.all().count()
    User = get_user_model()
    admin_count = User.objects.filter(is_superuser=True).count()
    context = {
        'invoice_count':invoice_count,
        'client_count':client_count,
        'admin_count':admin_count,
    }
    return render(request,'dashboard/index.html',context)

@login_required(login_url='login')  
def add_client(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"client saved successfully")
            return redirect('list_objects', app_name='invoice',model_name='Client')
    else:
        form = ClientForm()
    return render(request,'dashboard/addClient.html',{'form':form})

@login_required(login_url='login')  
def list_objects(request,app_name, model_name):
    # Get the model class from the model name
    model = apps.get_model(app_label=app_name, model_name=model_name)
    # Fetch all records from the model
    records = model.objects.all()
    template = f'dashboard/{model_name.lower()}_list.html'
    return render(request, template, {'records': records})

@login_required(login_url='login')  
def delete_client(request, pk):
    client = Client.objects.get(id=pk)
    client.delete()
    messages.success(request, "Client deleted successfully")
    return redirect('list_objects', app_name='invoice',model_name='Client')

@login_required(login_url='login')  
def create_invoice(request):
    records = Invoice.objects.all()
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():

            invoice_no = "INV-" + str(random.randint(100, 9999999))
            
            # # Calculate total amount (example logic)
            # total_amount = 
            
            # Save the form, but don't commit yet
            invoice = form.save(commit=False)
            invoice.invoice_no = invoice_no
            # invoice.total_amount = total_amount
            invoice.save() 
            return redirect('charges',invoice_id=invoice.id)
    else:
        form = InvoiceForm()
    context = {
        'form': form,
        'records':records
    }
    return render(request, 'dashboard/invoice_list.html',context)

@login_required(login_url='login')  
def charges(request,invoice_id):

    if request.method == "POST":
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            form.instance.invoice_id = invoice_id
            form.save()
            messages.success(request,"Item added successfully")
            return redirect('charges',invoice_id=invoice_id)
    else:
        form = InvoiceItemForm()


    charges = InvoiceItem.objects.filter(invoice_id=invoice_id)
    invoice = Invoice.objects.get(id=invoice_id)

    total_charges = InvoiceItem.objects.filter(invoice_id=invoice_id).aggregate(total=Sum(F('price') * F('quantity')))['total']
    

    context = {
        'charges':charges,
        'invoice':invoice,
        'total_charges':total_charges,
        'form':form,
    }
    return render(request,'dashboard/invoice.html',context)

@login_required(login_url='login')  
def delete_invoice(request,pk):
    invoice = Invoice.objects.get(id=pk)
    invoice.delete()
    messages.success(request,'Invoice deleted successfully')
    return redirect('list_objects', app_name='invoice',model_name='Invoice')

@login_required(login_url='login')  
def generate_invoice_pdf(request, invoice_id):
    charges = InvoiceItem.objects.filter(invoice_id=invoice_id)
    invoice = Invoice.objects.get(id=invoice_id)

    total_charges = InvoiceItem.objects.filter(invoice_id=invoice_id).aggregate(total=Sum(F('price') * F('quantity')))['total']

    context = {
        'charges':charges,
        'invoice':invoice,
        'total_charges':total_charges,
    }

    # Render the HTML template with context
    html_string = render_to_string('dashboard/downloadInvoice.html', context)
    
    # Create a PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_'+ str(random.randint(100, 9999))+'.pdf"'
    
    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
    return response