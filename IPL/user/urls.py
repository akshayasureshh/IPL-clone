from django.urls import path
from  .views import *
from user import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    #path for individual team page
    path('IPL-teams/',views.teams,name='user-side-teams'),
    path('IPL-team-based-players/<int:id>/',views.players, name="player_detail"),
    path('IPL-team-based-player-profile/<int:id>/',views.profile, name="profile"),
    path('IPL-based-contact-page/',views.contact, name="contact"),
    path('IPL-side-sponsers/',views.sponser, name="sponsers"),
    path("IPL-point-table/",views.point_table,name= 'point_table' ),
    path("IPL-fixtures/",views.fixtures, name= "fixtures" ),
    path("IPL-upcoming-match/<int:id>/",views.upcoming_match, name="upcoming"),
    path("IPL-completed-match/<int:match_id_id>/",views.completed,name="completed"),
    path('IPL-live/<int:id>/',views.live,name="user-live"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)