from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import (DetailView, ListView)

import random
from .forms import InvoiceForm, JobForm
from .models import Client, Invoice, Job


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
def invoice_detail_view(request, id=None):
    hx_url = reverse("invoices:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "invoices/invoice_detail.html", context)


# @login_required
def invoice_detail_hx_view(request, id=None):
    try:
        obj = Invoice.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "invoices/partials/detail.html", context)


# @login_required
def invoice_create_view(request):
    form = InvoiceForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        # obj.user = request.user
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "invoices/create-update.html", context)


class ClientListView(ListView):
    model = Client


def invoice_create_update_view(request, id=None):
    obj = get_object_or_404(Invoice, id=id)
    form = InvoiceForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, "invoices/partials/forms.html", context)
    return render(request, "invoices/create-update.html", context)

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
    context = {
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.invoice = parent_obj
        new_obj.save()
        context['object'] = context
        return render(request, "invoices/partials/job-inline.html", context)
    return render(request, "invoices/partials/job-inline.html", context)

