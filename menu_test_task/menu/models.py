from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True)
    named_url = models.CharField(max_length=255, blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    menu_name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return '#'
        return self.url or '#'

    def str(self):
        return self.name

    class Meta:
        ordering = ['order']
