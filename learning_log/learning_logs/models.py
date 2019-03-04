from django.db import models


# Create your models here.
class Topic(models.Model):
    """learning theme"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return model string"""
        return self.text

class Entry(models.Model):
    """the learning detail"""
    topic = models.ForeignKey(Topic, False)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + "..."
