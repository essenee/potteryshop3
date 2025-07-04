from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.views.generic.base import TemplateView
from home.models import HomePage


from search import views as search_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('search/', search_views.search, name='search'),
    path('profile/', TemplateView.as_view(template_name="profile.html")),
    # path('gallery/', TemplateView.as_view(template_name="gallery.html")),
    # Creates urls like yourwebsite.com/login/
    path('payments/', include('payments.urls')),  # Add payments app URLs
    path('category/<str:category_id>/', HomePage().get_products_by_category, name='category_filter'),
    path('', include('payments.urls')),     # Add this to handle /cart/ and /cart/add/
    path('', include('allauth.urls')),
    path('', include('home.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
