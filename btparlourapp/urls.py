from . import views
from django.urls import path
from .views import *
urlpatterns=[
    path('',views.index,name='index'),
    path('register/', views.user_register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout),
    path('user_index/',views.user_index,name='user_index'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('view_users/', views.view_users, name='view_users'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('user/user_profile/', views.user_profile, name='user_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
     path("send-feedback/", send_feedback, name="send_feedback"),
     path("feedback-success/", feedback_success, name="feedback_success"),
     path('view-feedback/', view_feedback, name='view_feedback'),
     path('add-beauty-service/', add_beauty_service, name='add_beauty_service'),
path('view-beauty-services/', views.view_beauty_services, name='view_beauty_services'),
path('services/edit/<int:service_id>/', views.edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', views.delete_service, name='delete_service'),
path('user_view_beauty_services/', user_view_beauty_services, name='user_view_beauty_services'),
path('book_service/<int:service_id>/', views.book_service, name='book_service'),
path('booking_success/', booking_success, name='booking_success'),  # Add this line
path('payment_page/<int:booking_id>/', payment_page, name='payment_page'),  # Payment page
path('user/bookings/', user_bookings, name='user_bookings'),  # Add this line
path('payment_details/<int:booking_id>/', payment_details, name='payment_details'),  # Payment details
 path('admin/bookings/', all_bookings, name='all_bookings'),  # Admin view for all bookings
 path('payment-details/<int:booking_id>/', payment_details, name='payment_details'),  # Payment details view
  path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),  # Cancel booking view
  # path('notifications/', notifications, name='notifications'),
  path('send-notification/', views.send_notification, name='send_notification'),
  # path('admin/delete-notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
  # path('admin/notifications/', views.admin_notifications_view, name='admin_notifications'),


    path('notifications/', views.admin_notifications_view, name='admin_notifications'),
    path('admin/notifications/delete/<int:notif_id>/', views.delete_admin_notification, name='delete_admin_notification'),
    path('user_notifications/', views.notifications, name='notifications'),  
    path('user_view_notifications/', views.user_notifications, name='user_notifications'),
]