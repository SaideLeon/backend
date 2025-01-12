# chronicles/models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Chronicle(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        limit_choices_to={'is_superuser': True},
        help_text="Apenas superusuários podem criar crônicas"
    )

    class Meta:
        ordering = ['-date']
        verbose_name = "Crônica"
        verbose_name_plural = "Crônicas"

    def __str__(self):
        return self.title

class FeaturedChronicle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_superuser': True},
        help_text="Apenas superusuários podem criar crônicas principais"
    )
    date = models.DateField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    pdf_file = models.FileField(
        upload_to='featured_pdfs/',
        help_text="Upload do arquivo PDF da crônica principal"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Crônica Principal"
        verbose_name_plural = "Crônicas Principais"
        ordering = ['-date']

    def __str__(self):
        return f"Crônica Principal - {self.title} ({self.user.email})"  # Changed to email since that's our username field

    def save(self, *args, **kwargs):
        if not self.pk:
            FeaturedChronicle.objects.filter(user=self.user).delete()
        super().save(*args, **kwargs)

# Signal para garantir que apenas superusuários possam criar crônicas
@receiver(pre_save, sender=Chronicle)
@receiver(pre_save, sender=FeaturedChronicle)
def ensure_superuser(sender, instance, **kwargs):
    user = instance.author if sender == Chronicle else instance.user
    if not user.is_superuser:
        raise ValueError("Apenas superusuários podem criar crônicas")