import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    created_on = models.DateTimeField(default=timezone.now, db_index=True)
    modified_on = models.DateTimeField(default=None, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(default=None, null=True)

    def save(self, *args, **kwargs):
        self.modified_on = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_on = timezone.now()
        self.save()



class Author(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("pk",)


class Book(BaseModel):
    title = models.CharField(max_length=200)
    published_on = models.DateField(default=None, blank=True, null=True)
    description = models.TextField()
    author = models.ManyToManyField(Author)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("pk",)

    def author_list(self):
        return [auth.name for auth in self.author.all()]