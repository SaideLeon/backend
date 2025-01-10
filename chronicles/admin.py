from django.contrib import admin
from django.utils.html import format_html
from .models import Chronicle, FeaturedChronicle

@admin.register(Chronicle)
class ChronicleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'created_at', 'pdf_link')
    search_fields = ('title', 'content', 'author__username', 'author__first_name', 'author__last_name')
    list_filter = ('date', 'created_at', 'author', 'updated_at')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informações Principais', {
            'fields': ('title', 'date', 'author')
        }),
        ('Conteúdo', {
            'fields': ('content', 'pdf_file')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">Abrir PDF</a>', obj.pdf_file.url)
        return "Sem PDF"
    pdf_link.short_description = 'PDF'

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(FeaturedChronicle)
class FeaturedChronicleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'created_at', 'pdf_link')
    search_fields = ('title', 'content', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('date', 'created_at', 'user', 'updated_at')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informações Principais', {
            'fields': ('title', 'date', 'user'),
            'description': 'Cada superusuário pode ter apenas uma crônica principal ativa.'
        }),
        ('Conteúdo', {
            'fields': ('content', 'pdf_file'),
            'description': 'O arquivo PDF é obrigatório para crônicas principais.'
        }),
        ('Informações do Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">Abrir PDF</a>', obj.pdf_file.url)
        return "Sem PDF"
    pdf_link.short_description = 'PDF'

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.none()
        return qs

    class Media:
        css = {
            'all': ('admin/css/featured_chronicle.css',)
        }
        js = ('admin/js/featured_chronicle.js',)