from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Importa los módulos de vistas
from managecultivo import views

urlpatterns = [
    path('', views.home, name='home'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),    
    path("bienvenida/", views.bienvenida, name="bienvenida"),    

    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),

    path("crear_zonaagricola/", views.crear_zonaagricola, name="crear_zonaagricola"),   
    path("zona/<int:id>/", views.v_zonaagricola.zona_detalle, name="zona_detalle"),
    
    
        # Vista principal: lista de personas, crear y editar
    path("crear_personal/", views.v_personal.crear_personal, name="crear_personal"),
    # Vista auxiliar: devolver datos en JSON para el modal, solo se usa en el boton editar
    path("persona/<int:id>/", views.v_personal.persona_detalle, name="persona_detalle"),


    path("parametrizar_cultivo/", views.parametrizar_cultivo, name="parametrizar_cultivo"),
    path("crear_cultivo/", views.crear_cultivo, name="crear_cultivo"),
    path("crear_actividadcultivo/", views.crear_actividadcultivo, name="crear_actividadcultivo"),
    path("crear_actividad/", views.crear_actividad, name="crear_actividad"),
    path("crear_insumo/", views.crear_insumo, name="crear_insumo"),
    path("crear_actividadcultivo/", views.crear_actividadcultivo, name="crear_actividadcultivo"),
    path("borrar_actividadcultivo/<int:pk>/", views.borrar_actividadcultivo, name="borrar_actividadcultivo"),
    path("crear_ciclo/", views.crear_ciclo, name="crear_ciclo"),
    path("compra_insumos/", views.gestionar_insumos, name="compra_insumos"),
    path("clima/", views.clima, name="clima"),
    path("mover_arriba/<int:pk>/", views.mover_arriba, name="mover_arriba"),
    path("mover_abajo/<int:pk>/", views.mover_abajo, name="mover_abajo"),   
    path("ajustar_ciclo/<int:ciclo_id>/", views.ajustar_ciclo, name="ajustar_ciclo"),  
    path("monitorear_ciclo/", views.ciclo_monitoreo, name="monitorear_ciclo"),
    path("ajustar_ciclo/<int:ciclo_id>/", views.ajustar_ciclo, name="ajustar_ciclo"),
    path("calendario_ciclo/", views.calendario_ciclo, name="calendario_ciclo"), 
    path("borrar_cultivo/", views.borrar_cultivo, name="borrar_cultivo"),
    path("borrar_actividad/", views.borrar_actividad, name="borrar_actividad"),
    path("borrar_insumo/", views.borrar_insumo, name="borrar_insumo"),
]
# pahth ("", views.funcion, name = "")

