# Import Django
from django.contrib import admin
# Register your local models here.
from .models import (
    MeasurementsDataFloat,
    
    )
admin.site.site_header = "XXXXXX, S.A. - Mediciones"
admin.site.site_title = "Portal de XXXXX, S.A."
admin.site.index_title = "Bienvenidos al portal de administración"   
# Create your models.Admin here.
# ***********************************************************************************
class MeasurementsDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'data_state',
        'data_tag',
        'data_value',
        'data_unit'
        )
    # __contains (Contenga), __icontains (Contenga,sea mayusculas o minusculas)
    # __date, __date__gt, __year, __year__gte, __iso_year, __iso_year__gte,
    # __month, __month__gte, __day, __week, __week_day, __time, __time__range,
    # __hour, __minute
    search_fields =(
        'created_at',
        )
    # Permite ordenar por una o mas columnas
    ordering = (        
        'id',
        )
    # Permite filtrar los registros o filas en la tabla
    list_filter = ('id',)
    # Permite definir el numero de lias a ver por pagina
    list_per_page = 100
    
admin.site.register(MeasurementsDataFloat,MeasurementsDataAdmin)
