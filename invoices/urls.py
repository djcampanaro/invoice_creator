from django.urls import path

from .views import (
    home_view,
    invoice_create_view,
    ClientListView,
    invoice_detail_view,
    InvoiceListView,
    invoice_update_view,
    job_update_hx_view,
    invoice_detail_hx_view,
)

app_name = 'invoices'
urlpatterns = [
    path('', home_view, name="home"),
    path('invoices/', InvoiceListView.as_view(), name='invoices'),
    path('create/', invoice_create_view, name='create'),
    path("invoices/hx/<int:parent_id>/job/<int:id>/", job_update_hx_view, name='hx-job-detail'),
    path("invoices/hx/<int:parent_id>/job/", job_update_hx_view, name='hx-job-create'),
    path("invoices/hx/<int:id>/", invoice_detail_hx_view, name='hx-detail'),
    path("invoices/<int:id>/", invoice_detail_view, name='detail'),
    path('invoices/<int:id>/update/', invoice_update_view, name='update'),
    path('clients/', ClientListView.as_view(), name='clients'),
]
