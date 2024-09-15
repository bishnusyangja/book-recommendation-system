import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(default=None, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(default=None, null=True)

    def save(self, *args, **kwargs):
        self.modified_on = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ("pk", )


class Author(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    published_on = models.DateField(default=None, blank=True, null=True)
    description = models.TextField()
    author = models.ManyToManyField(Author)

    def __str__(self):
        return self.title