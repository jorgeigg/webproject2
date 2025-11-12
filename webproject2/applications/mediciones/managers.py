# Import Django
from django.db import models

# models avanzados de Manager
# ***********************************************************************************
class MeasurementsDataManager(models.Manager):
    
    def Measurements_by_id(self,id):
        return self.filter(
            id = id
        )