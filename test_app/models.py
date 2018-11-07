from django.db import models

# Create your models here.
from django.utils import timezone
from django.conf import settings
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator


class DateTimeModal(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		abstract = True

	def delete(self):
		self.deleted_at = timezone.now()
		super().save()


class File(DateTimeModal):
	name = models.CharField(max_length=100)
	file = models.FileField(upload_to='files/',
                                validators=[FileExtensionValidator(allowed_extensions=['txt'])])
	threshold = models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(0.9)])

	class Meta:
		ordering = ["created_at"]

	def __str__(self):
		return self.name
