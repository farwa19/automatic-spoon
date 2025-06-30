from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import submit_email

urlpatterns = [
    path('', views.home, name='home'),
    path("login", views.login_view, name="login"),
    path("log", views.user_login, name="log"),
    path("upload-audio/", views.upload_audio, name="upload_audio"),
    path("logout", views.logout_view, name="logout"),
    path("have", views.user_login, name="have"),
    path("page", views.page, name="page"),
    path("patient", views.patient, name="patient"),
    path("new", views.new, name="new"),
    path("add", views.add, name="add"),
    path('submit-email', submit_email, name='submit_email'),

    path('more-info/<int:id>/', views.more_info, name='more_info'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

