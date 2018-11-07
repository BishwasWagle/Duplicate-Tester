from django.conf.urls import url, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'test_app'

urlpatterns = [
    url(r'^$', DashBoard.as_view(), name='dashboard'),
    url(r'^file/upload/$', FileCreate.as_view(), name='file_create'),
    url(r'^file/list/$', FileList.as_view(), name='file_list'),
    url(r'^extract/(?P<file_id>\d+)$', FileExtract.as_view(), name='file_extract'),
	url(r'^update/threshold/(?P<pk>\d+)/$', UpdateThreshold.as_view(), name='update_threshold'),
    ]
    # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)