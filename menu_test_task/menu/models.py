from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    menu_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, blank=True)
    named_url = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        if self.named_url:
            return reverse(self.named_url)
        return self.url

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['menu_name', 'order']
