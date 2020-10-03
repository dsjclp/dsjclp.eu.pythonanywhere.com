"""dlpsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('logout', TemplateView.as_view(template_name='registration/logout.html'), name="logout"),
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('core/', include('core.urls')),
    path('quote/', include('quote.urls')),
    path('buttons', TemplateView.as_view(template_name='core/buttons.html'), name="buttons"),
    path('cards', TemplateView.as_view(template_name='core/cards.html'), name="cards"),
    path('charts', TemplateView.as_view(template_name='core/charts.html'), name="charts"),
    path('tables', TemplateView.as_view(template_name='core/tables.html'), name="tables"),
    path('animation', TemplateView.as_view(template_name='core/animation.html'), name="animation"),
    path('border', TemplateView.as_view(template_name='core/border.html'), name="border"),
    path('color', TemplateView.as_view(template_name='core/color.html'), name="color"),
    path('other', TemplateView.as_view(template_name='core/other.html'), name="other"),
]

# Add in static routes so daphne can serve files; these should
# be masked eg with nginx for production use

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
