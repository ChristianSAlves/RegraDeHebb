from django.contrib import admin
from django.urls import path
from .views import PerceptronPredictView, PerceptronTrainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/train/', PerceptronTrainView.as_view(), name='perceptron-train'),
    path('api/recognize/', PerceptronPredictView.as_view(), name='perceptron-recognize'),
]