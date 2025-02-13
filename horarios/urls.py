from django.urls import path
from horarios import views
urlpatterns = [
    path('', views.horarios, name = 'horarios'),
    path('formulario_maestros/', views.formulario_maestros, name = 'formulario_maestros'),
    # path('formulario_maestros/nologin/', views.formulario_maestros_nologin, name = 'formulario_maestros')
    path('deleteMateriaUsuario/', views.deleteMateriaUsuario, name = 'deleteMateriaUsuario'),
    path("guardarGrupos/",views.guardarGrupos, name="guardarGrupos"),
    path("actualizarMateria/<int:id>/", views.actualizarMateria, name="actualizarMateria")
]