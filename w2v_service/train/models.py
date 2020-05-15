from typing import Optional

from django.db import models
from django.utils import timezone

from hyperparameters.models import Parameters


# Create your models here.
class TrainSession(models.Model):
    Created = 0
    Loaded = 1
    Running = 2
    Finished = 3
    Error = -1

    STATUS_CHOICES = [(Created, 'Created'), (Loaded, 'Loaded'),
                      (Running, 'Running'), (Error, 'Error'),
                      (Finished, 'Finished')]

    parameters = models.ForeignKey(Parameters, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=Created)
    result = models.FloatField(null=True)
    error = models.TextField(null=True)
    file_name = models.CharField(max_length=255, null=True)

    def set_status(self,
                   status: int,
                   result: Optional[float] = None,
                   error: Optional[str] = None,
                   is_last: bool = False,
                   is_start: bool = False):
        self.status = status
        if result:
            self.result = result
        if is_start and is_last:
            warnings.warn('Setting status with both is_start and is_end')
        if is_start:
            self.start_time = timezone.now()
        if is_last:
            self.end_time = timezone.now()
        if error:
            self.error = error
        self.save()