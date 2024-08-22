from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html


class ClientQuerySet(models.QuerySet):
     def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(client_name__icontains=query) | 
            Q(client_address__icontains=query) |
            Q(rate__icontains=query)
        )
        return self.filter(lookups)

class ClientManager(models.Manager):
     def get_queryset(self):
         return ClientQuerySet(self.model, using=self._db)
     
     def search(self, query=None):
        return self.get_queryset().search(query=query)
     
class InvoiceQuerySet(models.QuerySet):
     def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = (
            Q(invoice_number__icontains=query) | 
            Q(due_date__icontains=query)
        )
        return self.filter(lookups)

class InvoiceManager(models.Manager):
     def get_queryset(self):
         return InvoiceQuerySet(self.model, using=self._db)
     
     def search(self, query=None):
        return self.get_queryset().search(query=query)


class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=15, blank=True)
    client_address = models.TextField(max_length=100, blank=True)
    client_contact = models.CharField(max_length=50, blank=True)
    client_email = models.EmailField(blank=True)
    client_account_number = models.CharField(max_length=20, blank=True)
    rate = models.CharField(max_length=10, default='0')

    objects = ClientManager()

    def __str__(self):
        return self.client_name
    
    @property
    def name(self):
        return self.client_name
    
    def get_absolute_url(self):
        return reverse("invoices:client-detail", kwargs={"id": self.id})
    
    def get_edit_url(self):
        return reverse("invoices:client-update", kwargs={"id": self.id})
    
    def get_hx_url(self):
        return reverse("invoices:hx-client-detail", kwargs={"id": self.id})
    
    def get_invoices_children(self):
        return self.invoice_set.order_by('-invoice_number')
    
    def get_title(self):
        return f"{self.__class__.__name__}: {self.client_name}"
    
    def get_content(self):
        content = {
            "Account: ": self.client_account_number, 
            "Address: ": self.client_address, 
            "Phone: ": self.client_phone, 
            "Email: ": self.client_email, 
            "Rate: ": f"${self.rate}/hr"
        }
        return content

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_number = models.IntegerField()
    invoice_date = models.DateField()
    due_date = models.DateField()

    objects = InvoiceManager()

    def __str__(self):
        return str(self.invoice_number)
    
    @property
    def name(self):
        return self.invoice_number
    
    def get_absolute_url(self):
        return reverse("invoices:detail", kwargs={"id": self.id})
    
    def get_hx_url(self):
        return reverse("invoices:hx-invoice-detail", kwargs={"id": self.id})
    
    def get_edit_url(self):
        return reverse("invoices:update", kwargs={"id": self.id})
    
    def get_jobs_children(self):
        return self.job_set.all()
    
    def get_title(self):
        return f"{self.__class__.__name__} #: {self.invoice_number}"
    
    def get_content(self):
        client_link = reverse("invoices:client-detail", kwargs={"id": self.client.id})
        client_html = format_html('<a href="{}">{}</a>', client_link, self.client.client_name)
        content = {
            "Client: ": client_html,
            "Invoice Date: ": self.invoice_date.strftime('%b. %d, %Y'),
            "Due Date: ": self.due_date.strftime('%b. %d, %Y')
        }
        return content
    
    def get_total_hours(self):
        hours = 0
        for job in self.job_set.all():
            hours += float(job.hours)
        return hours
    
    def get_total_amount(self):
        sub_total = 0
        for job in self.job_set.all():
            sub_total += float(job.product_of_hours_and_rate())
        return f'{sub_total:.2f}'

class Job(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    date_of_work = models.DateField()
    description = models.CharField(max_length=100)
    hours = models.CharField(max_length=10)

    def get_absolute_url(self):
        return self.invoice.get_absolute_url()
    
    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.invoice.id,
            "id": self.id,
        }
        return reverse("invoices:hx-job-detail", kwargs=kwargs)
    
    def product_of_hours_and_rate(self):
        total = float(self.hours) * float(self.invoice.client.rate)
        return f'{total:.2f}'
