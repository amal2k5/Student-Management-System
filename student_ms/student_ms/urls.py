from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from sms.views import dashboard, home
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


class MyPasswordChangeView(PasswordChangeView):
    def form_valid(self):
        messages.success(self.request, "Password updated successfully!")
        return redirect('sms:student_dashboard')

urlpatterns = [

    
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    
    path(
        'accounts/password_change/',
        MyPasswordChangeView.as_view(),
        name='password_change'
    ),

    
    path(
    'logout/',
    LogoutView.as_view(next_page='/accounts/login/'),
    name='logout'
),


    
    path('sms/', include('sms.urls')),
    path('admin/', admin.site.urls),

    
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    
    
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
