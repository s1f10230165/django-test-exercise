from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)

    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt