from django.contrib import admin
from django.urls import path
from .views import HebbTrainView, HebbPredictView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/train/', HebbTrainView.as_view(), name='hebb-train'),
    path('api/recognize/', HebbPredictView.as_view(), name='hebb-recognize'),
]