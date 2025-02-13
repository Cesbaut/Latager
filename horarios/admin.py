from django.contrib import admin
from .models import MateriasAlumno, GruposAlumno, Color , Materia, grupo

class MateriasAlumnoAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')
class GruposAlumnoAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')
    

# Register your models here.


admin.site.register(MateriasAlumno, MateriasAlumnoAdmin)
admin.site.register(GruposAlumno, GruposAlumnoAdmin)
admin.site.register(Color)
admin.site.register(Materia)
admin.site.register(grupo)

