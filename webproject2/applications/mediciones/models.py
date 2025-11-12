# Import Model Django
from django.db import models

# Import Local Managers
from .managers import MeasurementsDataManager

# Create your models here.
# ***********************************************************************************  
class MeasurementsDataFloat(models.Model):
    created_at = models.DateTimeField(db_column='datatime_db',auto_now=True)
    data_state = models.IntegerField('state', unique=True)
    data_tag = models.CharField('tag', max_length=25)
    data_value = models.FloatField(db_column='value',default=0)
    data_unit = models.CharField('unit', max_length=25)
    
    # Importo modelos avanzados de Manager
    objects = MeasurementsDataManager()
    # Defino algunas caracteristicas para el admin. de Django
    class Meta:
      verbose_name = 'Measurement'  # Nombre de Columna singular
      verbose_name_plural = 'Measurements'  # Nombre en plural
    # Defino los titulos de las columnas del admin. de Django
    def __str__(self):
      return str(self.id) + ' - ' + str(self.created_at)+ ' - ' + str(self.data_tag)+ ' - ' + str(self.data_value)+ ' - ' + str(self.data_unit)+ ' - ' + str(self.data_state)
# ***********************************************************************************  
