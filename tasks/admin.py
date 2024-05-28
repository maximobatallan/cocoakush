from django.contrib import admin
from .models import Task, Producto, Categoria, DatosPersonales
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
    
admin.site.register(Task,TaskAdmin)

admin.site.register(Producto)

admin.site.register(Categoria)

admin.site.register(DatosPersonales)
