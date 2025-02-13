from django.db import models
import random
from django.contrib.auth.models import User

class Color(models.Model):
    nombre = models.CharField(max_length=40, default=None)
    color = models.CharField(max_length=20, default=None)

    class Meta:
        verbose_name='Color'
        verbose_name_plural='Colores'
    
    def __str__(self):
        return self.color


class Materia(models.Model):
    clave = models.IntegerField(default=0000)
    nombre = models.CharField(max_length=100)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Materia'
        verbose_name_plural='Materias'
        ordering = ['clave']
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Asigna un color aleatorio si no se ha definido
        if self.color is None:
            colores_disponibles = Color.objects.all()
            if colores_disponibles.exists():
                random_color = random.choice(colores_disponibles)
                self.color = random_color
        super(Materia, self).save(*args, **kwargs)

class grupo(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    grupo = models.IntegerField()
    nombre = models.CharField(max_length=300)
    tipo = models.CharField(max_length=1)
    horas = models.CharField(max_length=20)
    dias = models.CharField(max_length=100)
    cupo = models.IntegerField()
    calificacion = models.FloatField(default=0.0)
    salon = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        verbose_name='Grupo'
        verbose_name_plural='Grupos'
        ordering = ['-calificacion']
    
    def __str__(self):
        return self.nombre
    



class MateriasAlumno(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    materias = models.ManyToManyField(Materia)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='MateriasAlumno'
        verbose_name_plural='MateriasDeAlumnos'
    
    def __str__(self):
        return str(self.alumno)
    
class GruposAlumno(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    grupos = models.ManyToManyField(grupo)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='GruposDeAlumno'
        verbose_name_plural='GruposDeAlumnos'
    
    def __str__(self):
        return str(self.alumno)
    


    