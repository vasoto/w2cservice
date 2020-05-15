"""w2v_service URL Configuration
"""

from django.urls import path
from django.views.generic import TemplateView

from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.response import Response
from rest_framework.reverse import reverse

from hyperparameters.views import ParametersView
from train.views import TrainView
from monitor.views import MonitorView

parameters_list = ParametersView.as_view({'get': 'list', 'post': 'create'})
train_run_all = TrainView.as_view({'get': 'run'})
train_run_single = TrainView.as_view({'get': 'run'})

train_list = TrainView.as_view({'get': 'list'})
train_detail = TrainView.as_view({'get': 'retrieve'})

monitor_list = MonitorView.as_view({'get': 'list'})


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'hyperparameters':
        reverse('parameter-list', request=request, format=format),
        'train':
        reverse('train-list', request=request, format=format),
        'monitor':
        reverse('monitor-list', request=request, format=format)
    })


urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('hyperparameters/', parameters_list, name='parameter-list'),
    path('train/', train_list, name='train-list'),
    path('train/run/', train_run_all, name='train-run-all'),
    path('train/run/<int:pk>/', train_run_single, name='train-run-single'),
    path('train/<int:pk>/', train_detail, name='train-detail'),
    path('monitor/', monitor_list, name='monitor-list'),
])
