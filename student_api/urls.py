from django.urls import path
from .views import( 


#! function view
home, 
butun_ograncileri_getir, 
yeni_ogrenci_create_et, 
tek_ogrenciyi_goruntuleme_islemi, 
ogrenciyi_guncelle, ogrenci_sil,

#! class view
StudentListCreate,
StudentDetail,


#! generic view
StudentGAV,
StudentDetailGAV,

#! concrete view
StudentCV,
StudentDetailCV,


 #! view set
 StudentMVS,
 PathMVS,

)

 #! view set
from rest_framework import routers

 #! view set
router = routers.DefaultRouter()
router.register("studentmvs", StudentMVS)

router.register("path", PathMVS)


urlpatterns = [

    #! function view

    path('homesayfasinigetir/', home),
    path("ogrencilerinhepsinigetir/", butun_ograncileri_getir),
    path("yeniogrenciolustur/", yeni_ogrenci_create_et),
    path("tekogrenci/<int:pk>/", tek_ogrenciyi_goruntuleme_islemi),
    path("ogrenciyiguncele/<int:pk>/", ogrenciyi_guncelle),
    path("ogrencisil/<int:pk>/", ogrenci_sil),



    #! class view

    path("students/", StudentListCreate.as_view()),
    path("students/<int:pk/", StudentDetail.as_view()),


    #? GenericApıView
    path("students/", StudentGAV.as_view()),
    path("students/<int:pk>/", StudentDetailGAV.as_view()),


    #! concrete view
    path("studentcv/", StudentCV.as_view()),
    path("studentcv/<int:pk>", StudentDetailCV.as_view()),


    #! view set
] + router.urls
