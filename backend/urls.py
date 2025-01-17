from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from chronicles.views import ChronicleViewSet, FeaturedChronicleViewSet

# Configuração do router principal
router = DefaultRouter()
router.register(r'chronicles', ChronicleViewSet)
router.register(r'featured-chronicles', FeaturedChronicleViewSet)

# Customização do admin
admin.site.site_header = 'Administração do Site'
admin.site.site_title = 'Portal Admin'
admin.site.index_title = 'Bem-vindo ao Portal Administrativo'

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/', include(router.urls)),
    path('api/', include("visitors.urls")),
        path('api/', include("social.urls")),

    
    # DRF auth URLs (opcional - para interface de navegação da API)
    path('api-auth/', include('rest_framework.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuração para servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    # Adiciona URLs para servir arquivos estáticos em desenvolvimento
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Opcional: Adiciona URLs do debug_toolbar se estiver instalado
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

