from django.urls import path
from owner import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # Owner --------------------------
    path('',views.team_owner_login, name="owner-login"),
    path('team-owner-dashboard/',views.team_owner_dashboard,name='team-owner-dashboard'),
    # Team Members
    path('team-owner-players-adding-own-team/',views.team_owner_add_players,name='owner-player-adding'),
    path('team-all-platers/',views.owner_team_based_all_players, name="show-all-players"),
    path("owner-player-delete/<int:id>/",views.owner_player_delete, name="player_delete"),
    path("owner-player-update/<int:id>/",views.owner_edit_player, name="player_update"),
    path('owner-view-all-matches/',views.owner_team_all_matches, name="owner-team-matches"),
    path('match-platers-selection/<int:id>/',views.owner_selecte_players_on_match, name="match-player-selection"),
    path('owner-logout-session',views.owner_logout, name="logout"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)