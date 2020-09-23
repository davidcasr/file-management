from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileSerializer
from .models import File
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from django.conf import settings
import pandas as pd
from pandas import ExcelWriter
from rest_pandas import PandasView, PandasCSVRenderer, PandasExcelRenderer
    
class Files_APIView(APIView):
    parser_class = (FileUploadParser, )

    def get(self, request, format=None, *args, **kwargs):
        file = File.objects.all()
        serializer = FileSerializer(file, many=True)
        
        return Response(serializer.data)

    """
        Post implementation #1
            - Save one file
            - Use FileSerializer
    """
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Open file         
            open_file = open(settings.BASE_DIR + serializer.data['file'], 'r')
            # Read line per line
            for line in open_file.readlines():
                print(line)
            open_file.close()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Files_APIView_Detail(APIView):

    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file)  
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExportWithPandas(APIView):
    """
        Method to create a file using pandas library
    """
    def get(self, request, format=None):
        file = File.objects.all()
        serializer = FileSerializer(file, many=True)
        
        # In this case the folder is created with anteriority
        writer = pd.ExcelWriter(r'media\export.xlsx')  
        df = pd.DataFrame(serializer.data)      
        df.to_excel(writer,  index=False)
        writer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExportWithRestPandas(PandasView):
    """
        Method to export file with django rest pandas
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    renderer_classes = [PandasExcelRenderer]

    def get_pandas_filename(self, request, format):
        if format in ('xls', 'xlsx'):
            # Use custom filename and Content-Disposition header
            return "Data Export"  # Extension will be appended automatically
        else:
            # Default filename from URL (no Content-Disposition header)
            return None