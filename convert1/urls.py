from django.urls import path

from . import views
app_name = 'convert1'
urlpatterns = [
    path('convert', views.convert_api, name="convert"),
    path('convertUI', views.convertUI, name="convertUI"),

    path('historyCenter/', views.history_center, name='historyCenter'),
    path('historyUI', views.HistoryUI, name="historyUI"),
    path('delete', views.delete_history, name="delete_history"),

    path('xiaozhuanUI', views.xiaozhuanUI, name="xiaozhuanUI"), #小篆页面
    path('xiaozhuan', views.xiaozhuan_api, name="xiaozhuan_api"), #小篆查询接口
    path('xiaozhuanhistoryUI', views.xiaozhuanhistoryUI, name="xiaozhuanhistoryUI"),
    path('del_xz', views.del_xz_history, name="del_xz"),

    path('evolution/', views.evolution, name='evolution'),

]
