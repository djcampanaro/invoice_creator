from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import (DetailView, ListView)

import random
from .forms import ClientForm, InvoiceForm, JobForm
from .models import Client, Invoice, Job
from invoice_creator import renderers


# @login_required
def home_view(request):
    # random_id = random.randint(1, 2)
    # article_obj = Article.objects.get(id=random_id)
    client_qs = Client.objects.all()
    # context = {
    #     "content": article_obj.content,
    #     "id": article_obj.id,
    #     "object": article_obj,
    #     "object_list": article_qs,
    #     "title": article_obj.title,
    # }
    context = {
        "object_list": client_qs,
    }

    HTML_STRING = render_to_string("home-view.html", context=context)
    # HTML_STRING = f"""
    # <h1> {article_obj.title} (id: {article_obj.id})!</h1>
    #  <p>{article_obj.content}!</p>
    # """.format(**context)

    return HttpResponse(HTML_STRING)


class InvoiceListView(ListView):
    model = Invoice


# @login_required
def invoice_list_view(request):
    obj = Invoice.objects.order_by('-invoice_number')
    context = {
        'objects': obj,
    }
    return render(request, "invoices/invoice-list.html", context)


# @login_required
def invoice_detail_view(request, id=None):
    hx_url = reverse("invoices:hx-invoice-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "invoices/detail.html", context)


# @login_required
def invoice_detail_hx_view(request, id=None):
    try:
        obj = Invoice.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "jobs": "jobs"
    }
    return render(request, "invoices/partials/detail.html", context)


def new_invoice_number():
    '''Generates new invoice number based on the last one created'''
    latest_invoice = Invoice.objects.latest('invoice_number')
    latest_invoice_num = latest_invoice.invoice_number
    return latest_invoice_num + 1


# @login_required
def invoice_create_view(request):
    form = InvoiceForm(request.POST or None)
    invoice_num = new_invoice_number()

    context = {
        "form": form,
        "invoice_num": invoice_num,
    }
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.user = request.user
        obj.invoice_number = invoice_num
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "invoices/create-update.html", context)


# @login_required
def client_create_view(request):
    form = ClientForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        print('ok')
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        id = obj.id
        return redirect(obj.get_absolute_url())
    return render(request, "invoices/client-create.html", context)


# @login_required
def client_detail_view(request, id=None):
    hx_url = reverse("invoices:hx-client-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "invoices/detail.html", context)


# @login_required
def client_delete_view(request, id=None):
    obj = get_object_or_404(Client, id=id, user=request.user)
    if request.method == "POST":
        obj.delete()
        success_url = reverse('invoices:')
        return redirect("/clients")
    context = {
        "object": obj
    }
    return render(request, "invoices/detail.html", context)


# @login_required
def client_detail_hx_view(request, id=None):
    try:
        obj = Client.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "invoice": "invoice"
    }
    return render(request, "invoices/partials/detail.html", context)


# @login_required
def client_list_view(request):
    obj = Client.objects.order_by('client_name')
    context = {
        'objects': obj,
    }
    return render(request, "invoices/client-list.html", context)


# @login_required
def client_update_view(request, id=None):
    obj = get_object_or_404(Client, id=id)
    form = ClientForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, "invoices/partials/client-detail.html", context)
    return render(request, "invoices/create-update.html", context)


# @login_required
def invoice_update_view(request, id=None):
    obj = get_object_or_404(Invoice, id=id)
    form = InvoiceForm(request.POST or None, instance=obj)
    new_job_url = reverse("invoices:hx-job-create", kwargs={"parent_id": obj.id})
    if len(obj.job_set.all()) >= 8:
        new_job_url = None
    context = {
        "form": form,
        "new_job_url": new_job_url,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, "invoices/partials/forms.html", context)
    return render(request, "invoices/create-update.html", context)


# @login_required
def job_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Invoice.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")
    
    instance = None
    if id is not None:
        try:
            instance = Job.objects.get(invoice=parent_obj, id=id)
        except:
            instance = None
    form = JobForm(request.POST or None, instance=instance)
    url = reverse("invoices:hx-job-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    # if len(parent_obj.job_set.all()) >= 8:
    #     url = None
    print(url)
    context = {
        "form": form,
        "object": instance,
        "url": url
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.invoice = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "invoices/partials/job-inline.html", context)
    return render(request, "invoices/partials/job-form.html", context)

def advanced_pdf_view(request, id=None):
    try:
        obj = Invoice.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "jobs": "jobs"
    }
    # return render(request, "invoices/partials/detail.html", context)


    invoice_number = id
    # context = {
    #     "customer_name": "Ethan Hunt",
    #     "invoice_number": f"{invoice_number}",
    #     "date": "2021-07-04",
    #     "amount": "$50",
    #     "pdf_title": f"Invoice #{invoice_number}",
    # }
    response = renderers.render_to_pdf("pdfs/invoice-pdf.html", context)
    if response.status_code == 404:
        raise Http404("Invoice not found")

    filename = f"Invoice_{invoice_number}.pdf"
    """
    Tell browser to view inline (default)
    """
    content = f"inline; filename={filename}"
    download = request.GET.get("download")
    if download:
        """
        Tells browser to initiate download
        """
        content = f"attachment; filename={filename}"
    response["Content-Disposition"] = content
    return response
