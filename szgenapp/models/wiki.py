from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

class Wiki(models.Model):
    title = models.CharField(verbose_name='Title', max_length=150)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Wiki Help Entry'
        verbose_name_plural = 'Wiki Help Entries'

    def __str__(self):
        return '%s' % self.title