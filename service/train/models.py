from django.db import models


class TrainSessionModel(models.Model):
    Created = 0
    Queued = 1
    Running = 2
    Finished = 3
    Error = -1

    STATUS_CHOICES = [(Created, 'Created'), (Queued, 'Queued'),
                      (Running, 'Running'), (Error, 'Error'),
                      (Finished, 'Finished')]

    experiment = models.UUIDField()
    param_start_alpha = models.FloatField(null=True)
    param_end_alpha = models.FloatField(null=True)
    param_epochs = models.IntegerField(null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=Created)
    result = models.TextField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
