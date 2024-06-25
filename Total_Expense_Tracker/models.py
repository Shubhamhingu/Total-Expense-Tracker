from django.db import models # type: ignore

class Transaction(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    debit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_cash = models.BooleanField()
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"{str(self.date_created) + self.type}"

class Shift(models.Model):
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_cash = models.BooleanField()
    tip = models.ForeignKey(Transaction, related_name='tip_transactions', on_delete=models.CASCADE)
    ride = models.ForeignKey(Transaction, related_name='ride_transactions', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.shift_start and self.shift_end:
            time_diff = self.shift_end - self.shift_start
            self.hours_worked = time_diff.total_seconds() / 3600  # convert seconds to hours
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date_created}"

class GlobalVariable(models.Model):
    key = models.CharField(max_length=10)
    value = models.FloatField()

    def __str__(self):
        return f"{self.key}"