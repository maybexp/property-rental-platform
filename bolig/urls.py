from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('', include('index.urls')),
                  path('log-ind', auth_views.LoginView.as_view(), name='login'),

                  # Logout URL
                  path('log-ud', auth_views.LogoutView.as_view(), name='logout'),

                  # Password change URLs
                  path('password_change', auth_views.PasswordChangeView.as_view(), name='password_change'),
                  path('password_change/done', auth_views.PasswordChangeDoneView.as_view(),
                       name='password_change_done'),

                  # Password reset URLs
                  path('glemt-adgangskode', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
