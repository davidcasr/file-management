from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'files'

urlpatterns = [
    # File 
    path('v1/file', Files_APIView.as_view()), 
    path('v1/file/<int:pk>', Files_APIView_Detail.as_view()),
    path('v1/export1', ExportWithPandas.as_view()),  
    path('v1/export2', ExportWithRestPandas.as_view()),  
]

urlpatterns = format_suffix_patterns(urlpatterns)