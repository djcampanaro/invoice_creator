from django.shortcuts import render
from invoices.models import Client, Invoice


SEARCH_TYPE_MAPPING = {
    'client': Client,
    'clients': Client,
    'invoice': Invoice,
    'invoices': Invoice,
}


def search_view(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    Klass = Client
    if search_type in SEARCH_TYPE_MAPPING.keys():
        Klass = SEARCH_TYPE_MAPPING[search_type]
    qs = Klass.objects.search(query=query)
    context = {
        "queryset": qs,
    }
    template = "search/results-view.html"
    if request.htmx:
        context['queryset'] = qs[:5]
        template = "search/partials/results.html"
    return render(request, template, context)