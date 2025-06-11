"""
URL configuration for studentstudyportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from dashboard import views as dash_views
from django.contrib.auth.views import LogoutView
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dashboard.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    # path('register/', dash_views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='dashboard/logout.html'), name='logout'),


    # path('login_page/', dash_views.login_page, name='login_page'),
    # path('logout/', LogoutView.as_view(next_page='login_page'), name='logout'),
    # path('register/', dash_views.register, name='register'),
    

    path('profile/',dash_views.profile,name='profile')
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)