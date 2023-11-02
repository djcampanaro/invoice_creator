from django.conf import settings
from django.db import models
from django.urls import reverse

class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=50)
    client_phone = models.CharField(max_length=15)
    client_address = models.CharField(max_length=100, blank=True)
    client_contact = models.CharField(max_length=50)
    client_email = models.EmailField()
    client_account_number = models.CharField(max_length=20)
    rate = models.CharField(max_length=10, default='0')

    def __str__(self):
        return self.client_name

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_number = models.IntegerField()
    invoice_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return str(self.invoice_number)
    
    def get_absolute_url(self):
        return reverse("invoices:detail", kwargs={"id": self.id})
    
    def get_hx_url(self):
        return reverse("invoices:hx-detail", kwargs={"id": self.id})
    
    def get_edit_url(self):
        return reverse("invoices:update", kwargs={"id": self.id})
    
    def get_jobs_children(self):
        return self.job_set.all()

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
        return reverse("invoices:hx-ingredient-detail", kwargs=kwargs)
