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

]
# pahth ("", views.funcion, name = "")

