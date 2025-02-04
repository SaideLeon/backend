from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from chronicles.views import ChronicleViewSet, FeaturedChronicleViewSet

# Configuração do schema view para drf_yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Crônicas API",
        default_version='v1',
        description="API para gerenciar crônicas, comentários, curtidas e compartilhamentos",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="saideomarsaid@gmail.com"),
        license=openapi.License(name="Licença BSD"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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

    # URLs da documentação da API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuração para servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Opcional: Adiciona URLs do debug_toolbar se estiver instalado
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
