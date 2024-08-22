from django.urls import path

from .views import (
    home_view,
    invoice_create_view,
    client_create_view,
    client_delete_view,
    client_detail_view,
    client_detail_hx_view,
    client_list_view,
    client_update_view,
    invoice_detail_view,
    invoice_list_view,
    invoice_update_view,
    job_update_hx_view,
    invoice_detail_hx_view,
    advanced_pdf_view,
)

app_name = 'invoices'
urlpatterns = [
    path('', home_view, name="home"),
    path('invoices/', invoice_list_view, name='invoices'),
    path('create/', invoice_create_view, name='create'),
    path("invoices/hx/<int:parent_id>/job/<int:id>/", job_update_hx_view, name='hx-job-detail'),
    path("invoices/hx/<int:parent_id>/job/", job_update_hx_view, name='hx-job-create'),
    path("invoices/hx/<int:id>/", invoice_detail_hx_view, name='hx-invoice-detail'),
    path("invoices/<int:id>/", invoice_detail_view, name='detail'),
    path('invoices/<int:id>/update/', invoice_update_view, name='update'),
    path('clients/', client_list_view, name='clients'),
    path("clients/hx/<int:id>/", client_detail_hx_view, name='hx-client-detail'),
    path('clients/<int:id>/delete/', client_delete_view, name='client-delete'),
    path('clients/<int:id>/', client_detail_view, name='client-detail'),
    path('clients/<int:id>/update/', client_update_view, name='client-update'),
    path('clients/create/', client_create_view, name='client-create'),
    path('invoices/<int:id>/pdf/', advanced_pdf_view, name='invoice-pdf'),
]
