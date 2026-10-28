from django.urls import path

from . import views

urlpatterns = [
    path('convert', views.convert_text, name="convert"),
    path('convertUI', views.convertUI, name="convertUI"),
    path('history', views.HistoryView, name="history"),
    path('delete', views.delete_history, name="delete_history"),
]
