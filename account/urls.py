from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import views
from .forms import ChangePasswordForm

app_name = 'account'
urlpatterns = [
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('registration', views.registration, name='registration'),
    path('user', views.user, name='user'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('update/<int:id>', views.update, name='update'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('update_profile/<int:id>', views.update_profile, name='update_profile'),
    path('change_password/', PasswordChangeView.as_view(template_name='account/change_password.html', success_url=reverse_lazy('account:password_change_done'), form_class=ChangePasswordForm), name='change_password'),
    path('change_password/done/', PasswordChangeDoneView.as_view(template_name='account/change_password_done.html'), name='password_change_done')
]