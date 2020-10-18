from django.views import generic

class QuotePage(generic.TemplateView):
    template_name = "quote/create_quote.html"

class ReversePage(generic.TemplateView):
    template_name = "quote/create_reverse.html"