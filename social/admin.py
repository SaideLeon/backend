# social/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Comment, Like, Share

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_info', 'chronicle_link', 'content_preview', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author__name', 'author__email', 'chronicle__title')
    actions = ['approve_comments', 'unapprove_comments']
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 20
    
    def content_preview(self, obj):
        """Retorna uma prévia do conteúdo do comentário"""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Conteúdo'
    
    def author_info(self, obj):
        """Retorna informações formatadas do autor"""
        return format_html(
            '<div><strong>{}</strong><br><small>{}</small></div>',
            obj.author.name,
            obj.author.email
        )
    author_info.short_description = 'Autor'
    
    def chronicle_link(self, obj):
        """Retorna um link para a crônica relacionada"""
        if obj.chronicle:
            url = reverse('admin:chronicles_chronicle_change', args=[obj.chronicle.id])
            return format_html('<a href="{}">{}</a>', url, obj.chronicle.title)
        elif obj.featured_chronicle:
            url = reverse('admin:chronicles_featuredchronicle_change', args=[obj.featured_chronicle.id])
            return format_html('<a href="{}">{}</a>', url, obj.featured_chronicle.title)
        return "N/A"
    chronicle_link.short_description = 'Crônica'
    
    def approve_comments(self, request, queryset):
        """Ação para aprovar comentários em massa"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comentário(s) aprovado(s) com sucesso.')
    approve_comments.short_description = 'Aprovar comentários selecionados'
    
    def unapprove_comments(self, request, queryset):
        """Ação para desaprovar comentários em massa"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comentário(s) desaprovado(s) com sucesso.')
    unapprove_comments.short_description = 'Desaprovar comentários selecionados'
    
    fieldsets = (
        ('Informações do Comentário', {
            'fields': ('content', 'is_approved')
        }),
        ('Relacionamentos', {
            'fields': ('author', 'chronicle', 'featured_chronicle')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'chronicle_info', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__name', 'user__email', 'chronicle__title', 'featured_chronicle__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 20
    
    def user_info(self, obj):
        """Retorna informações formatadas do usuário"""
        return format_html(
            '<div><strong>{}</strong><br><small>{}</small></div>',
            obj.user.name,
            obj.user.email
        )
    user_info.short_description = 'Usuário'
    
    def chronicle_info(self, obj):
        """Retorna informações da crônica"""
        if obj.chronicle:
            url = reverse('admin:chronicles_chronicle_change', args=[obj.chronicle.id])
            return format_html('<a href="{}">{}</a>', url, obj.chronicle.title)
        elif obj.featured_chronicle:
            url = reverse('admin:chronicles_featuredchronicle_change', args=[obj.featured_chronicle.id])
            return format_html('<a href="{}">{}</a>', url, obj.featured_chronicle.title)
        return "N/A"
    chronicle_info.short_description = 'Crônica'
    
    fieldsets = (
        ('Relacionamentos', {
            'fields': ('user', 'chronicle', 'featured_chronicle')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user_info', 'platform', 'chronicle_info', 'created_at')
    list_filter = ('platform', 'created_at')
    search_fields = ('user__name', 'user__email', 'chronicle__title', 'featured_chronicle__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 20
    
    def user_info(self, obj):
        """Retorna informações formatadas do usuário"""
        return format_html(
            '<div><strong>{}</strong><br><small>{}</small></div>',
            obj.user.name,
            obj.user.email
        )
    user_info.short_description = 'Usuário'
    
    def chronicle_info(self, obj):
        """Retorna informações da crônica"""
        if obj.chronicle:
            url = reverse('admin:chronicles_chronicle_change', args=[obj.chronicle.id])
            return format_html('<a href="{}">{}</a>', url, obj.chronicle.title)
        elif obj.featured_chronicle:
            url = reverse('admin:chronicles_featuredchronicle_change', args=[obj.featured_chronicle.id])
            return format_html('<a href="{}">{}</a>', url, obj.featured_chronicle.title)
        return "N/A"
    chronicle_info.short_description = 'Crônica'
    
    fieldsets = (
        ('Informações do Compartilhamento', {
            'fields': ('platform',)
        }),
        ('Relacionamentos', {
            'fields': ('user', 'chronicle', 'featured_chronicle')
        }),
        ('Informações do Sistema', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )