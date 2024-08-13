# urls.py
from django.urls import path
from . import views

# api/ - returns jsonresponse
# regular url - returns template rendering

urlpatterns = [
    # for debug or viewing
    path('raw-envi-data/', views.SensorDataListView.as_view(), name='sensor_data'),
    # different temp comparisons
    path('temp-diff-graph/', views.temp_diff_graph, name='sensor_data'),


    # Latest sensor data from the database
    path('api/latest-envi-data/', views.latest_envi_data, name='latest_envi_data'),
    path('realtime-envi-data/', views.realtime_envi_data, name='realtime_envi_data'),

    # Graphing using matplotlib
    path('graph/', views.graph_data, name='graph_data'),
    path('graph/<int:year>/', views.graph_data, name='graph_data_year'),
    path('graph/<int:year>/<int:month>/', views.graph_data, name='graph_data_month'),
    path('graph/<int:year>/<int:month>/<int:day>/', views.graph_data, name='graph_data_day'),
    
    # Vital Signs
    path('add_vital_signs/', views.add_vital_signs, name='add_vital_signs'),
    path('api/authorization/', views.handle_auth_request, name='handle_auth_request'),
]