from django.urls import path
from  .views import *
from dashboard import views
from dashboard .views import save_data,save_to_closed_score,save_live_score,second_half_notification,transfer_bowler_data
from dashboard import views as admin_panal



urlpatterns = [

     #################### Admin  Information #################

    path("",views.admin_dashboard, name="IPL-admin-dashboard"),
    path("IPL-admin-login-page/",views.admin_login,name="IPL-admin-login"),
    path("IPL-admin-logout/",views.admin_logout, name="IPL-admin-logout"),
    path("IPL-admin-password-reset/",views.admin_reset_password, name="IPL-admin-password-reset"),

    #################### Team  Information #################

    path("IPL-team-adding/", views.create_team, name="add_team"),
    path("IPL-admin-all-team/",views.all_team, name= "show_teams"),
    path("IPL-team-update/<int:id>/",views.admin_update_team, name="update-team"),
    path("IPL-team-delete/<int:id>/",views.admin_delete_team, name="delete-team"),


    #################### Season  Information #################

    path('IPL-season-creation/',views.admin_season_adding, name='Season_Adding'),
    path("IPL-season-update/<int:id>/",views.admin_season_update, name="season-update"),
    path('IPL-season-delete/<int:id>/',views.admin_season_delete, name="season-delete"),


     #################### Players  Information #################
     
    path("IPL-player-adding/",views.admin_add_players, name="add_players"),
    path("IPL-all-players-view/",views.all_players, name="show_players"),
    path("IPL-player-update/<int:id>/",views.admin_players_update, name="update-player"),
    path("IPL-player-delete/<int:id>/",views.admin_players_delete, name="delete-player"),


     #################### Players  Information #################
    path("IPL-tournament-creation/",views.match_schedule, name="tournament-creation"),
    path("IPL-all-tournaments",views.matched_teams, name="all-matches"),
    path("IPL-match-Update/<int:id>/",views.matched_team_update,name="match-update"),
    path("IPL-match-delete/<int:id>/",views.match_team_delete, name="match-delete"),
    path("IPL-matched-players-/",views.admin_select_team_players_on_match,name="match-player-selection"),
    path("IPL-match-players-selectrion/<int:id>/",views.admin_matched_teams_players_selection, name="player-selected"),



    #################### Live section  Information #################
    path("IPL-admin-start-live/",views.admin_start_live, name="StartLiveMatch"),
    path("IPL-team-toss-selection/<int:id>/",views.matched_team_toss_selection, name="TossSelection"),
    path("adminscoreupdate/<int:id>/",views.AdminUpcomingMatchScoreUpdate, name="adminscoreupdate"),
    path('ajax/getScores',views.getScores,name='getScores'),
    path('save_data/',save_data, name='save_data'),
    path('save_to_closed_score/',save_to_closed_score, name='save_to_closed_score'),
    path('update_bowler_data/',views.update_bowler_data, name='update_bowler_data'),
    path('save-form-data/', save_live_score, name='save_form_data'),
    path('ajax/getBowlerScore',admin_panal.getBowlerScore,name='getBowlerScore'),
    path('transfer_bowler_data/', transfer_bowler_data, name='transfer_bowler_data'),
    path('ajax/getScores',views.getScores,name='getScores'),
    path('second_half_notification/', second_half_notification, name='second_half_notification'),
    path('ajax/getScoreslive',admin_panal.getScoreslive,name="getScoreslive"),



    #################### sponsers  Information #################


    path("IPL-admin-add-sponsers/",views.admin_add_sponser,name="sponsers"),
    path("IPL-all-sponsers/",views.admin_all_sponsers, name= "all-sponsers"),
    path("IPL-sponser-delete/<int:id>/",views.delete_sponser, name= 'delete-sponser'),
    path("IPL-sponser-update/<int:id>/",views.update_sponsers, name ='update-sponser'),


    #################### Carousal  Information #################


    path("IPL-Carousal-adding/",views.admin_add_banner, name= "banner"),
    path("IPL-all-carousal/",views.admin_all_banner,name="all-banner"),
    path("IPL-banner-Delete/<int:id>/",views.delete_banner,name="banner-delete"),
    path("IPL-Carousal-update/<int:id>/",views.update_banner,name="banner-update"),


   














]

# Add a URL to the urlpattern
