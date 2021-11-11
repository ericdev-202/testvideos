from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from main import views as m_views
from . import views

urlpatterns = [
   path('',m_views.home,name="home"),
   path('upload/',m_views.upload,name="upload"),  
   path('video/<int:post_id>/', m_views.watch_video, name='watch'),
   path('video/',m_views.video,name="video"),
   path('plans/<int:pk>', m_views.plan, name='plan'),
   path('join/', m_views.join, name='join'),
   path('checkout/', m_views.checkout, name='checkout'),
   path('signup/',m_views.SignUp,name='sign'),
   path('settings/', m_views.settings, name='settings'),
   # path('signup', m_views.SignUp.as_view(), name='signup'),

   # path('s/',m_views.watch_video,name="watch"),
   path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
   path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),

    # register, confirmation, validation and callback urls
   path('c2b/register', views.register_urls, name="register_mpesa_validation"),
   path('c2b/confirmation', views.confirmation, name="confirmation"),
   path('c2b/validation', views.validation, name="validation"),
   path('c2b/callback', views.call_back, name="call_back"),


]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)