from django.db import models


# Create your models here.
class Parameters(models.Model):
    start_alpha = models.FloatField(null=True)
    end_alpha = models.FloatField(null=True)
    epochs = models.IntegerField(null=True)

    def __str__(self):
        return f"start_alpha={self.start_alpha}, end_alpha={self.end_alpha}, epochs={self.epochs}"

    class Meta:
        unique_together = ['start_alpha', 'end_alpha', 'epochs']