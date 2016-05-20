from __future__ import unicode_literals

from django.db import models


class Task(models.Model):
    task_id = models.CharField(max_length=100)
    input = models.TextField(blank=True)
    output = models.TextField(blank=True)

    def __str__(self):
        return self.task_id