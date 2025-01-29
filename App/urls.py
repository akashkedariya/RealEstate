from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('example/', views.example_view, name='example'),
    path("user-register/", views.Customuserlist.as_view()),
    path('user-login/',views.UserLoginView.as_view()),
    path('property-add/',views.Propertyview.as_view()),
    path('property-add/<int:pk>/',views.Propertyview.as_view()),
    path('property-list/',views.MultiAPISearchView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    