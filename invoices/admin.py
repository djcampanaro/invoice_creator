from django.contrib import admin

from .models import Client, Invoice, Job

class JobInLine(admin.StackedInline):
    model = Job
    extra = 7

class InvoiceInLine(admin.StackedInline):
    inlines = [JobInLine]
    model = Invoice
    extra = 0

class ClientAdmin(admin.ModelAdmin):
    inlines = [InvoiceInLine]


admin.site.register(Client, ClientAdmin)