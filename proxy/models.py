from django.db import models


class Domain(models.Model):
    domain = models.TextField()

    def __str__(self):
        return f'Domain({self.domain})'


class Document(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    url = models.TextField()
    content = models.BinaryField()
    mime = models.TextField()

    def __str__(self):
        return self.url

