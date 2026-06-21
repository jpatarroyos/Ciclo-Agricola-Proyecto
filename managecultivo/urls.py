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
    
        # Vista principal: lista de personas, crear y editar
    path("crear_personal/", views.v_personal.crear_personal, name="crear_personal"),
    # Vista auxiliar: devolver datos en JSON para el modal, solo se usa en el boton editar
    path("persona/<int:id>/", views.v_personal.persona_detalle, name="persona_detalle"),
]
# pahth ("", views.funcion, name = "")

