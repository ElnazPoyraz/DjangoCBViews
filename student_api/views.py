from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Student, Path

from .serializers import StudentSerializer, PathSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, mixins, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet


#!#################function based views########################

@api_view(['GET'])
def home(request):
    return Response({"home":"this is home page"})


@api_view(['GET'])
def butun_ograncileri_getir(request):
    ogrenciler_queryset_tipinde_data = Student.objects.all()
    # print(ogrenciler_queryset_tipinde_data)
    tip_donusumu = StudentSerializer(ogrenciler_queryset_tipinde_data, many=True)
    return Response(tip_donusumu.data)


@api_view(['POST'])
def yeni_ogrenci_create_et(request):
    json_formatin_queryset_donum = StudentSerializer(data=request.data)
    if json_formatin_queryset_donum.is_valid():
        json_formatin_queryset_donum.save()
        return Response(json_formatin_queryset_donum.data, status=status.HTTP_201_CREATED)
    return Response(json_formatin_queryset_donum.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view()
def tek_ogrenciyi_goruntuleme_islemi(request, pk):
    # try:
    #     tek_ogrenci = Student.objects.get(id=pk)
    #     serializer = StudentSerializer(tek_ogrenci)
    #     return Response(serializer.data)
    # except:
    #     return Response({"message": "olmayan id numarasi girildi. id numarani kontrol et!!!"})
    
    tek_ogrenci = get_object_or_404(student, id=pk)
    serializer = StudentSerializer(tek_ogrenci)
    return Response(serializer.data)



@api_view(['PUT'])
def ogrenciyi_guncelle(request, pk):
    tek_ogrenci = get_object_or_404(Student, id=pk)
    serializer = StudentSerializer(instance=tek_ogrenci, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def ogrenci_sil(request, pk):
    tek_ogrenci = get_object_or_404(Student, id=pk)
    tek_ogrenci.delete()
    data = {"message": "ogrenci silindi"}
    return Response(data)




#!#################class based views########################

#! APIView

class StudentListCreate(APIView):

    def get(self,request):
        students = Student.objects.all()  # queryset
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class StudentDetail(APIView):

    def get(self, request, pk):
        # student = Student.objects.get(id=pk)
        student = get_object_or_404(Student, id=pk)
        serializer =StudentSerializer(student)
        return Response(serializer.data)
    
    def put(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        student = get_object_or_404(Student, id=pk)
        student.delete()
        data = {
            "message": f"Student {student.last_name} deleted successfully"
        }
        return Response(data)




#! GENERICAPIView and Mixins

""" #? GenericApıView
# One of the key benefits of class-based views is the way they allow you to compose bits of reusable behavior. REST framework takes advantage of this by providing a number of pre-built views that provide for commonly used patterns.

# GenericAPIView class extends REST framework's APIView class, adding commonly required behavior for standard list and detail views.

#? Mixins
# - ListModelMixin
#     - list method
# - CreateModelMixin
#     - create method
# - RetrieveModelMixin
#     - retrieve method
# - UpdateModelMixin
#     - update method
# - DestroyModelMixin
#     - destroy method 
"""

class StudentGAV(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class StudentDetailGAV(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



#! concrete view

class StudentCV(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailCV(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer 



#! model view set

class StudentMVS(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class PathMVS(ModelViewSet):
    queryset = Path.objects.all()
    serializer_class = PathSerializer