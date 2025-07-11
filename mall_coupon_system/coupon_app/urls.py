from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('login/store/', views.login_store, name='login_store'),
    path('login/user/', views.login_user, name='login_user'),
    path('register/user/', views.register_user, name='register_user'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/store/', views.dashboard_store, name='dashboard_store'),
    path('dashboard/user/', views.dashboard_user, name='dashboard_user'),
    path('upload-dataset/', views.upload_and_train_dataset, name='upload_dataset'),
    path('predict-coupon/', views.predict_coupon_view, name='predict_coupon'),
    path('store/add/', views.add_store, name='add_store'),
    path('logout/', views.logout_view, name='logout'),
    path('store/delete/<int:store_id>/', views.delete_store, name='delete_store'),
    path('store/<int:store_id>/coupons/', views.view_store_coupons, name='view_store_coupons'),
    path('logout/store/', views.logout_store, name='logout_store'),
    path('add-customer/', views.add_customer_to_store, name='add_customer'),
    path('issue-coupon/<int:user_id>/', views.issue_coupon, name='issue_coupon'),
    path('delete-user/<int:user_id>/', views.delete_user_from_store, name='delete_user_from_store'),
    path('user/view-coupons/<int:store_id>/', views.view_user_coupons, name='view_user_coupons'),
    path('user/view-coupons/<int:user_id>/', views.view_user_coupons, name='view_user_coupons'),
    path('admin/store/<int:store_id>/monitor-coupons/', views.monitor_store_coupons, name='monitor_store_coupons'),
    path('delete-coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
]

