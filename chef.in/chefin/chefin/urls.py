from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.forms import LoginForm
from core.views import index, contact, home, detail, signup

app_name = 'chefin'

urlpatterns = [
    path('', home, name='index'),
    path('contact/', contact, name='contact'),
    path('admin/', admin.site.urls),
    path('recipe/<str:recipe_id>/', detail, name='detail'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
