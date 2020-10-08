from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url


from django.views.generic import TemplateView

# Load demo plotly apps - this triggers their registration
import quote.dash_quote
import quote.dash_pr

# pylint: disable=unused-import

from django_plotly_dash.views import add_to_session

from .views import create_quote
from django.conf import settings
from django.conf.urls.static import static


app_name = 'quote'

urlpatterns = [
    path("create", views.create_quote, name='create_quote'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)