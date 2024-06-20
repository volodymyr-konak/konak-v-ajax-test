from datetime import datetime
from django.db import models


class TestResult(models.Model):
    device_type = models.CharField(max_length=100)
    operator = models.CharField(max_length=100)
    time = models.DateTimeField()
    success = models.BooleanField()

    # def __init__(self, device_type, operator, time, success):
    #     self.device_type = device_type
    #     self.operator = operator
    #     self.time = datetime.strptime(time, "YYYY-MM-DD HH:mm:ss")
    #     self.success = success
