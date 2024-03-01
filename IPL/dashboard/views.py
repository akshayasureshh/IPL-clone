from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate,login,logout
from dashboard.forms import *
from .models import *
from django.contrib import messages
from django.http import Http404
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from collections import Counter

# Create your views here.
def admin_dashboard(request) :
    if request.user.is_authenticated :
        return render(request, 'dashboard.html')
    else :
        return redirect('IPL-admin-login')

# Admin Login 
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('IPL-admin-dashboard')
    else:
        if request.method == 'POST' :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username,password=password)
            if user is not None :
                login(request,user)
                messages.success(request,"Logged in successfuly completed")
                return redirect('IPL-admin-dashboard')
            else :
                messages.error(request,"Invalid username or Password")
                return redirect('IPL-admin-login')
    return render(request, 'login.html')



def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('IPL-admin-login')
    else:
        return redirect("IPL-admin-dashboard")
    

def admin_reset_password(request) : # completed
    if request.user.is_authenticated:
        print("already Logged This Person",request.user.username)
        if request.method == "POST":
            user = request.user
            current_password = request.POST["Current"]
            new_password = request.POST["New"]
            repeat_password = request.POST["Confirm"]
            if new_password == repeat_password:
                try:
                    user = authenticate(username=user.username, password = current_password)
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password resetted successfully.")
                    return redirect(admin_login)
                except Http404:
                    messages.error(request, "W")
                    return redirect(admin_reset_password)
            else:
                messages.error(request, "New passwords are not matching.")
                return redirect(admin_reset_password)
        return render(request, 'reset-psw.html')
    else :
        return redirect(admin_login)


def create_team(request):
    if request.user.is_authenticated:
        if request.method == "POST" :
            # Create teams 
            form = TeamInsertForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,"Team Adding successfuly completed")
                return redirect(create_team)
            else :
                messages.error(request,"Error Please check the form")
        else:
            form = TeamInsertForm()
        return render(request, 'team.html',{'form' : form})
    else :
       return redirect(admin_login)
    

def all_team(request):
    if request.user.is_authenticated:
        team_info = TeamDetails.objects.all()
        return render(request, 'admin-all-teams.html',{"team_info" : team_info})
    else : 
        return render(request, 'login.html')
    



def admin_update_team(request,id):
    if request.user.is_authenticated:
        team_info = TeamDetails.objects.filter(id=id).first()
        if request.method == 'POST' :
            form = TeamUpdateForm(request.POST,request.FILES, instance=team_info)
            if form.is_valid():
                form.save()
                return redirect(all_team)
        else : 
            form = TeamUpdateForm(instance=team_info)
            data = {"form" :form, "team_info" : team_info}
        return render(request, 'update-team.html', data)
    else :
        return redirect(admin_login)
    


def admin_delete_team(request,id):
    if request.user.is_authenticated:
        team_details = TeamDetails.objects.get(id=id)
        team_details.delete()
        return redirect(all_team)
    else:
        return render(admin_login)
    




def admin_add_players(request):
    if request.user.is_authenticated:
        if request.method == 'POST' :
            form = PlayerInsertForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Player adding successfuly completed')
                return redirect(admin_add_players)
            else:
                messages.error(request,"Error in adding player")
        else :
            form = PlayerInsertForm()   
        return render(request, 'player.html',{"form" : form})     
    else :
       return redirect(admin_login)



def all_players(request) :
    if request.user.is_authenticated:
        player_info = PlayersDetails.objects.all()
        return render(request, 'admin-all-player.html',{"palyers" :player_info })
    else : 
        return redirect(admin_login)
    


def admin_players_update(request, id):
    if request.user.is_authenticated:
        player_info = PlayersDetails.objects.filter(id=id).first()
        if request.method == 'POST':
            form = PlayerUpdateForm(request.POST, request.FILES, instance=player_info)
            if form.is_valid():  # Corrected: Added parentheses after is_valid
                form.save()
                messages.success(request,'Profile updated successfully!')
                return redirect(all_players)
            else :
                messages.error(request, "Please correct the error below.")
        else:
            form = PlayerUpdateForm(instance=player_info)
        return render(request, 'player-update.html', {"form": form})
    else:
        return redirect(admin_login)



def admin_players_delete(request,id):
    player_info = PlayersDetails.objects.get(id=id)
    player_info.delete()
    return redirect(all_players)




def admin_season_adding(request):
    if request.user.is_authenticated :
        season = Season.objects.all().values()
        if request.method == 'POST':
            form = SeasonAddingForm(request. POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Season Adding Successfully Completed')
                return redirect(admin_season_adding)
            else :
                messages.error(request, 'Somthing Is wrong')
        else :
            form = SeasonAddingForm()
        context = {
            "form" : form,
            'seasons' : season
        }
        return render(request, 'season.html',context)
    else :
        return redirect(admin_login)
    



def admin_season_delete(request,id) :
    season = Season.objects.filter(id=id)
    season.delete()
    return redirect(admin_season_adding)



def admin_season_update(request,id):
    if request.user.is_authenticated :
        season_id = Season.objects.filter(id=id).first()
        if request.method == 'POST' :
            form = SeasonUpdateForm(request.POST, instance=season_id)
            if form.is_valid():
                form.save()
                messages.success(request,'Season Data Updated Successfully')
                return redirect(admin_season_adding)
            else :
                messages.warning(request,"Please Check Your Input")
        else :
            form = SeasonUpdateForm(instance=season_id)
    else :
        return redirect(admin_login)

    return render(request, 'season-update.html',{"form":form})




def match_schedule(request):
    if request.user.is_authenticated:
        team= TeamDetails.objects.all()
        seasons = Season.objects.all()
        if request.method == "POST":
            date_and_time = request.POST.get('date')
            match_type = request.POST.get('type')
            match_season = request.POST.get('season')
            match_season = Season.objects.filter(pk = match_season).first()
            ground = request.POST.get('ground')
            team1 = request.POST.get('team1')
            team1 = TeamDetails.objects.filter(pk = team1).first()
            team2 = request.POST.get('team2')
            team2 = TeamDetails.objects.filter(pk = team2).first()
            tournament_data = UpcomingTeam()
            tournament_data.Match_date=date_and_time
            tournament_data.Match_type=match_type
            tournament_data.Ground_name=ground
            tournament_data.Match_season=match_season
            tournament_data.TeamA=team1
            tournament_data.TeamB=team2
            tournament_data.save()
            messages.success(request,"Tournament Creating  successfuly completed")
            return redirect(match_schedule)
        return render(request, 'match.html',{"teams" : team, "seasons" : seasons})
    else :
        return redirect(admin_login)
    


# Admin createdv tournaments  view
def matched_teams(request):
    if request.user.is_authenticated:
        matched_team_info = UpcomingTeam.objects.all()
        return render(request, 'all-matches.html',{"matches" : matched_team_info})
    else :
       return redirect(admin_login)
    


def matched_team_update(request,id):
    if request.user.is_authenticated:
        match_info = UpcomingTeam.objects.filter(id=id).first()
        if request.method == 'POST' :
            form=MatchedTeamsUpdateForm(request.POST, instance=match_info)
            if form.is_valid :
                form.save()
                return redirect(matched_teams)
        else :
            form=MatchedTeamsUpdateForm(instance=match_info)
            data = {
                "form" : form,
                "match_info" : match_info
            }
        return render(request, 'match-update.html',data)
    else :
        return redirect(admin_login)
    


def match_team_delete(request,id):
    if request.user.is_authenticated:
        upcoming_team_instance = UpcomingTeam.objects.filter(pk=id)
        upcoming_team_instance.delete()
        return redirect(matched_teams)
    else : 
        return redirect(admin_login)
    


# Admin adding players matched team 
def admin_select_team_players_on_match(request):
    if request.user.is_authenticated:
        matched_team_info = UpcomingTeam.objects.all()
        return render(request, 'match-player-selection.html',{"matches" : matched_team_info})
    else :
        return redirect(admin_login)
    

def admin_matched_teams_players_selection(request, id):
    if request.user.is_authenticated:
        match = UpcomingTeam.objects.filter(id=id).first()
        team1_players = PlayersDetails.objects.filter(Player_team = match.TeamA)
        team2_players = PlayersDetails.objects.filter(Player_team = match.TeamB)
        print(team1_players)
        print(team2_players)

        context = {
            "team" : match,
            "team1" : team1_players,
            "team2": team2_players
        }

        if request.method == "POST":
            Player_One_Team = request.POST.getlist("team1")     
            Player_Two_Team = request.POST.getlist('team2')
            print(f"stage1: {Player_One_Team}, {Player_Two_Team}")
            Match_data = UpcomingTeam.objects.get(id=id)
            print(f"stage2: {Match_data}")
            Match_data.TeamA_players.add(*Player_One_Team)
            Match_data.TeamB_playeres.add(*Player_Two_Team)

            return redirect(admin_select_team_players_on_match)

        return render(request, 'player_team.html',context)
    else :
        return redirect(admin_login)
    






#Admin start live 
def admin_start_live(request) :
    if request.user.is_authenticated:
        matched_team_info = UpcomingTeam.objects.all()
        return render(request, 'admin-start-live.html',{"tournament_info" : matched_team_info})
    else :
        return redirect(admin_login)
    


def matched_team_toss_selection(request,id):
    if request.user.is_authenticated:
        upcoming_team = UpcomingTeam.objects.filter(id=id).first()
        print(upcoming_team.pk)
        if request.method == 'POST' :
            data = LiveMatchView()
            data.matchid = UpcomingTeam.objects.get(id=id)
            data.Match_date =  UpcomingTeam.objects.get(id=id)
            data.Match_season = UpcomingTeam.objects.get(id=id)
            print("baaaaaaaaaga",data.Match_season)
            data.Match_type = UpcomingTeam.objects.get(id=id)
            data.Match_toss = UpcomingTeam.objects.get(id=id)
            data.Match_status = UpcomingTeam.objects.get(id=id)
            data.Ground_name = UpcomingTeam.objects.get(id=id)
            data.TeamA = UpcomingTeam.objects.get(id=id)
            data.TeamB = UpcomingTeam.objects.get(id=id)
            data.save()


            # completed = CompletedMatch()
            # completed.match_id = UpcomingTeam.objects.get(id=id)
            # completed.season = UpcomingTeam.objects.get(id=id)
            # completed.toss = UpcomingTeam.objects.get(id=id)
            # completed.type = UpcomingTeam.objects.get(id=id)
            # completed.status = UpcomingTeam.objects.get(id=id)
            # completed.ground = UpcomingTeam.objects.get(id=id)
            # completed.team1 = UpcomingTeam.objects.get(id=id)
            # completed.team2 = UpcomingTeam.objects.get(id=id)
            # completed.save()





            tosswinner = request.POST.get('win1')
            Choice = request.POST.get('choice')
            upt = UpcomingTeam.objects.get(id=id)
            upt.Match_toss = tosswinner
            upt.Match_status = Choice
            upt.save()
        All_data  = {

            "team" : upcoming_team
        }
        return render(request, 'toss-selection.html',All_data)
        
    else :
        return redirect(admin_login)
    



def AdminUpcomingMatchScoreUpdate(request, id):
    match_details = UpcomingTeam.objects.filter(id=id)
    match = UpcomingTeam.objects.get(id=id)


    match = UpcomingTeam.objects.filter(id=id).first()
    
    # Print some details for debugging
    print("Team One:", match.TeamA.pk)
    print("Team Two:", match.TeamB.pk)
    print("Upcoming Match ID:", match.pk)
    
    # Fetch details of the completed match
    completed_id = UpcomingTeam.objects.filter(id=id).first()
    print("Completed Match Team ID:", completed_id.TeamA.pk)
    print("Completed Match ID:", completed_id.pk)

    # Fetch details of batters and bowlers for a closed match
    # batters = ClosedScore.objects.filter(matchID=id).first()
    # print("Batters Team ID:", batters.teamid)

    # bowlers = ClosedBowlerScore.objects.filter(matchID=id).first()
    # print("Bowlers Team ID:", bowlers.teamid)

    # More debugging prints
    print("Completed Match TeamB Team ID:", completed_id.TeamB.pk)

    teamPlayers = None
    teamBowlersPlayers = None

    # Check if the completed match details match the upcoming match
    if completed_id.pk == match.pk:
        if completed_id.TeamA.pk == match.TeamA.pk:
            # Fetch details for TeamA batters and bowlers
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamA.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamA: {team_score_sum1}")
            
            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers}")

        elif completed_id.TeamB.pk == match.TeamB.pk:
            # Fetch details for TeamB batters and bowlers
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamB.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamB: {team_score_sum1}")
            
            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamA.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers}")

    else:
        # Fetch details for TeamB when the completed match does not match TeamA
        if completed_id.TeamB.pk == match.TeamB.pk:
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamB: {team_score_sum1}")

            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers}")

        elif completed_id.TeamA.pk == match.TeamA.pk:
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamA.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamA: {team_score_sum1}")

            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers}")

    # More fetching and prints for TeamB
    if completed_id.pk == match.pk:
        if completed_id.TeamB.pk == match.TeamB.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamB.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamA.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers2}")

        elif completed_id.TeamA.pk == match.TeamA.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamA.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers2}")

    else:
        if completed_id.TeamA.pk == match.TeamA.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamA.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers2}")

        elif completed_id.TeamB.pk == match.TeamB.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamB.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.pk, teamid=completed_id.TeamA.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers2}")

    # Compare total scores to determine the winner
    if team_score_sum1 > team_score_sum2:
        winner_team = completed_id.TeamA
        print("Winner is TeamA:", winner_team.Team_name)
    elif team_score_sum1 < team_score_sum2:
        winner_team = completed_id.TeamB
        print("Winner is TeamB:", winner_team.Team_name)
    else:
        winner_team = None  # It's a tie

    # Calculate the runs difference for a tie
    if winner_team:
        runs_difference = abs(team_score_sum1 - team_score_sum2)
        print("It's a tie! Runs difference:", runs_difference)

    upcoming_match = UpcomingTeam.objects.filter(id=id).first()
    choice = upcoming_match.Match_status
    toss = match.Match_toss
    batsmen = None
    bowler = None

    if choice == "1":
        if upcoming_match.TeamA == toss:
            batsmen1 = upcoming_match.TeamA
            batsmen = match.TeamA_players.all()
            bowler2 = upcoming_match.TeamB
            bowler = match.TeamB_playeres.all()
        else:
            batsmen1 = upcoming_match.TeamB
            batsmen = match.TeamB_playeres.all()
            bowler2 = upcoming_match.TeamA
            bowler = match.TeamA_players.all()
    else:
        if upcoming_match.TeamA == toss:
            batsmen1 = upcoming_match.TeamB
            batsmen = match.TeamB_playeres.all()
            bowler2 = upcoming_match.TeamA
            bowler = match.TeamA_players.all()
        else:
            batsmen1 = upcoming_match.TeamA
            batsmen = match.TeamA_players.all()
            bowler2 = upcoming_match.TeamB
            bowler = match.TeamB_playeres.all()

    # Check if the request is a POST request and handle switching logic
    if request.method == 'POST':

        if "complete_match" in request.POST:
            completed = CompletedMatch()

            completed.match_id = UpcomingTeam.objects.get(id=id)
            completed.season = UpcomingTeam.objects.get(id=id)
            completed.type = UpcomingTeam.objects.get(id=id)
            completed.toss = UpcomingTeam.objects.get(id=id)
            completed.status = UpcomingTeam.objects.get(id=id)
            completed.ground = UpcomingTeam.objects.get(id=id)
            completed.team1 = UpcomingTeam.objects.get(id=id)
            completed.team2= UpcomingTeam.objects.get(id=id)
            completed.won_team = winner_team
            completed.save()
            print("keri makkalee")
            return redirect(matched_teams)


            


        # Assuming you have some form of condition to determine when to switch
        switch_condition = True  # Replace with your actual condition
        print("Switch condition:", switch_condition)

        if switch_condition:
            # Swap the batsmen and bowler variables
            batsmen, bowler = bowler, batsmen
            batsmen1, bowler2 = bowler2, batsmen1
            print("Batsmen and bowler switched successfully.")

            # Swap the team IDs
            upcoming_match.TeamA, upcoming_match.TeamB = upcoming_match.TeamB, upcoming_match.TeamA
            print("Team IDs switched successfully.")

            # Save the changes to the database
            upcoming_match.save()

            # Update the player lists and team IDs in the response
            response_data = {
                'switched': True,
                'team1': upcoming_match.TeamA.pk,
                'team2': upcoming_match.TeamB.pk,
                'batsmen': list(batsmen.values('Player_name')),
                'bowler': list(bowler.values('Player_name')),
            }

            return JsonResponse({'data': response_data})

    context = {
        "match_team": match_details,
        "team1": batsmen1,
        "team2": bowler2,
        "batsmen": batsmen,
        "bowler": bowler,
        'match': match
    }
    return render(request, 'live.html', context)




def getScores(request):
    queryset = LiveBattingScore.objects.all()
    return JsonResponse({"scores":list(queryset.values())})



# views.py# views.pyimport jsonfrom django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LiveScore
import json
import traceback  # Import traceback module for error logging

@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            batsman_name = data['batsman_name']
            runs = data['runs']
            balls = data['balls']
            ones = data['ones']
            twos = data['twos']
            threes = data['threes']
            fours = data['fours']
            sixes = data['sixes']
            wides = data['wides']
            leg_byes = data['leg_byes']
            no_balls = data['no_balls']
            strike_rate = data['strike_rate']
            match_id = data['match_id']
            team_id = data['team_id']

            # Try to get the existing record based on the batsman's name
            live_score, created = LiveScore.objects.get_or_create(batsman_name=batsman_name)

            # Update the fields with the new data
            live_score.runs = runs
            live_score.balls = balls
            live_score.ones = ones
            live_score.twos = twos
            live_score.threes = threes
            live_score.fours = fours
            live_score.sixes = sixes
            live_score.wides = wides
            live_score.leg_byes = leg_byes
            live_score.no_balls = no_balls
            live_score.strike_rate = strike_rate
            live_score.matchID = match_id
            live_score.teamid = team_id

            # Save the updated record
            live_score.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            # Log the error for debugging
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'errors': str(e)})

    return JsonResponse({'status': 'error', 'errors': 'Invalid request method'})





# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import LiveScore, ClosedScore

# @csrf_exempt
# def close_score(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             batsman_name = data['batsman_name']
#             runs = data['runs']
#             balls = data['balls']
#             ones = data['ones']
#             twos = data['twos']
#             threes = data['threes']
#             fours = data['fours']
#             sixes = data['sixes']
#             wides = data['wides']
#             leg_byes = data['leg_byes']
#             strike_rate = data['strike_rate']

#             # Save data to ClosedScore model
#             closed_score, created = ClosedScore.objects.get_or_create(batsman_name=batsman_name)

#             closed_score.runs = runs
#             closed_score.balls = balls
#             closed_score.ones = ones
#             closed_score.twos = twos
#             closed_score.threes = threes
#             closed_score.fours = fours
#             closed_score.sixes = sixes
#             closed_score.wides = wides
#             closed_score.leg_byes = leg_byes
#             closed_score.strike_rate = strike_rate

#             closed_score.save()

#             # Delete corresponding entry from LiveScore model
#             live_score_instance = LiveScore.objects.filter(batsman_name=batsman_name).first()
#             if live_score_instance:
#                 live_score_instance.delete()

#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'errors': str(e)})

#     return JsonResponse({'status': 'error', 'errors': 'Invalid request method'})







from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import LiveScore
import json
from django.db import transaction

@csrf_exempt
@transaction.atomic
def save_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            batsman_name = data['batsman_name']
            runs = data['runs']
            balls = data['balls']
            ones = data['ones']
            twos = data['twos']
            threes = data['threes']
            fours = data['fours']
            sixes = data['sixes']
            wides = data['wides']
            leg_byes = data['leg_byes']
            no_balls = data['no_balls']
            strike_rate = data['strike_rate']
            match_id = data['match_id']
            team_id = data['team_id']
            # out_mode = data['outMode']
            # out_took_player = data['outTookPlayer']

            # Try to get the existing record based on the batsman's name
            live_score, created = LiveScore.objects.get_or_create(batsman_name=batsman_name)

            # Update the fields with the new data
            live_score.runs = runs
            live_score.balls = balls
            live_score.ones = ones
            live_score.twos = twos
            live_score.threes = threes
            live_score.fours = fours
            live_score.sixes = sixes
            live_score.wides = wides
            live_score.leg_byes = leg_byes
            live_score.no_balls = no_balls
            live_score.strike_rate = strike_rate
            live_score.matchID = match_id
            live_score.teamid = team_id
            # live_score.out_mode = out_mode
            # live_score.out_took_player = out_took_player

            # Save the updated record
            live_score.save()
 
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': str(e)})

    return JsonResponse({'status': 'error', 'errors': 'Invalid request method'})



import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LiveScore, ClosedScore


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import LiveScore, ClosedScore

@csrf_exempt
def save_to_closed_score(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))

            batsman_name = data['batsman_name']

            # Check if there is an existing record for the batsman in ClosedScore
            existing_record = ClosedScore.objects.filter(batsman_name=batsman_name).first()

            if existing_record:
                # Update existing record by adding up the values
                existing_record.runs += data['runs']
                existing_record.balls += data['balls']
                existing_record.ones += data['ones']
                existing_record.twos += data['twos']
                existing_record.threes += data['threes']
                existing_record.fours += data['fours']
                existing_record.sixes += data['sixes']
                existing_record.wides += data['wides']
                existing_record.leg_byes += data['leg_byes']
                existing_record.no_balls += data['no_balls']
                existing_record.dead_ball += data['dead_ball']
                existing_record.matchID = data['match_id']
                existing_record.teamid = data['team_id']
                # Update other fields as needed
                existing_record.save()
            else:
                # Save data to ClosedScore model
                closed_score_instance = ClosedScore(
                    batsman_name=batsman_name,
                    runs=data['runs'],
                    balls=data['balls'],
                    ones=data['ones'],
                    twos=data['twos'],
                    threes=data['threes'],
                    fours=data['fours'],
                    sixes=data['sixes'],
                    wides=data['wides'],
                    leg_byes=data['leg_byes'],
                    no_balls=data['no_balls'],
                    dead_ball=data['dead_ball'],
                    strike_rate=data['strike_rate'],
                    matchID =  data['match_id'],
                    teamid  = data['team_id']
                    # ... other fields ...
                )
                closed_score_instance.save()

            # Delete the corresponding row from LiveScore
            LiveScore.objects.filter(batsman_name=batsman_name).delete()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': str(e)})

    return JsonResponse({'status': 'error', 'errors': 'Invalid request method'})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def update_scores_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract relevant data from the request
        batsman_name = data.get('batsman_name')
        runs = data.get('runs', 0)
        balls = data.get('balls', 0)

        # Process the data as needed, update bowler scores, etc.

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
    else:
        # Return an error response for other HTTP methods
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})








from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Bowler

@csrf_exempt
def update_bowler_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            

            # Extract bowler data
            bowler_name = data['bowler']
            runs = int(data['runs'])
            balls = int(data['balls'])
            maiden_overs = int(data['maidenOvers'])
            # no_balls = int(data.get('noBalls', 0))
            wickets = int(data['wickets'])
            overs = float(data['overs'])
            matchID = data['match_id']
            teamid = data['team_id']

            
            similar_bowler =  Bowler.objects.filter(name = bowler_name).first()
            if similar_bowler:
        
            # bowler,created = Bowler.objects.get_or_create(name=bowler_name)
                similar_bowler.name = bowler_name
                similar_bowler.runs = runs
                similar_bowler.balls = balls
                similar_bowler.maidens = maiden_overs
                similar_bowler.wickets = wickets
                # similar_bowler.no_balls = no_balls
                similar_bowler.overs = overs
                similar_bowler.matchID =  matchID
                similar_bowler.teamid = teamid
                similar_bowler.save()

            else:
                new_bowler =  Bowler.objects.create(name = bowler_name)
                # new_bowler.name = bowler_name
                new_bowler.runs = runs
                new_bowler.balls = balls
                new_bowler.maidens = maiden_overs
                new_bowler.wickets = wickets
                # new_bowler.no_balls = no_balls
                new_bowler.overs = overs
                new_bowler.matchID = matchID
                new_bowler.teamid = teamid
                new_bowler.save()



            # Save the bowler instance
        

            

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError as e:
            print('JSON Decode Error:', e)
            return JsonResponse({'status': 'error', 'errors': 'Invalid JSON data'}, status=400)
        except KeyError as e:
            print('KeyError:', e)
            return JsonResponse({'status': 'error', 'errors': f'Missing key in JSON data: {str(e)}'}, status=400)
        except Exception as e:
            print('Exception:', e)
            return JsonResponse({'status': 'error', 'errors': f'Error saving bowler data: {str(e)}'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'errors': 'Invalid request method'}, status=405)






import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import OutMode

@csrf_exempt
@require_POST
def save_live_score(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        # Extract data from the request
        out_mode = data.get('selected_option')  # Adjust field names
        out_took_player = data.get('selected_player')  # Adjust field names
        selected_batsman = data.get('selectedbatsman')

        # Create a new OutMode instance and save the data
        out_mode_instance = OutMode(
            out_mode=out_mode,
            out_took_player=out_took_player,
            selected_batsman = selected_batsman
            # Add other fields accordingly
        )
        out_mode_instance.save()

        return JsonResponse({'message': 'Data saved successfully'})
    except json.JSONDecodeError as e:
        return JsonResponse({'message': f'Error decoding JSON: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'message': f'Error: {str(e)}'}, status=500)





def getBowlerScore(request):
    queryset = Bowler.objects.all()
    return JsonResponse({"scoresball":list(queryset.values())})





@csrf_exempt
def transfer_bowler_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            bowler_name = data['bowler_name']            
            print("STAGE1")
            live_table_bowler = Bowler.objects.filter(name = bowler_name).first()
           
            closed_bowler_object = ClosedBowlerScore.objects.filter(bowler_name=bowler_name).first()
            
            if closed_bowler_object:

            
                try:
                    print("ENTERED FIRST IF")
                    # closed_bowler_object.bowler_name =live_table_bowler.name
                    closed_bowler_object.closed_overs += live_table_bowler.overs
                    closed_bowler_object.closed_maidens += live_table_bowler.maidens
                    closed_bowler_object.closed_runs += live_table_bowler.runs
                    closed_bowler_object.closed_balls += live_table_bowler.balls
                    closed_bowler_object.closed_wickets += live_table_bowler.wickets
                    closed_bowler_object.matchID = live_table_bowler.matchID
                    closed_bowler_object.teamid = live_table_bowler.teamid
                    # closed_bowler_object.closed_no_balls += live_table_bowler.no_balls
                    # closed_bowler_object.closed_fours += live_table_bowler.fours
                    # closed_bowler_object.closed_sixes += live_table_bowler.sixes
                    # closed_bowler_object.closed_economy += live_table_bowler.economy
                    print("Hola Senior")
                
                    closed_bowler_object.save()
                    
                except Exception as e:
                    print(e)
                

                # if live_table_bowler:
                try:
                    print("Entered First try")
                    live_table_bowler.delete()
                except Exception as e:
                    print("nothing")
                    print(e)
                    # return redirect(transfer_bowler_data)
            

            else:
                print("Entered Else")
                ClosedBowlerScore.objects.create(
                    bowler_name = live_table_bowler.name,
                    closed_overs = live_table_bowler.overs,
                    closed_maidens = live_table_bowler.maidens,
                    closed_runs = live_table_bowler.runs,
                    closed_balls = live_table_bowler.balls,
                    closed_wickets = live_table_bowler.wickets,
                    matchID=live_table_bowler.matchID,
                    teamid = live_table_bowler.teamid,
                    # closed_no_balls = live_table_bowler.no_balls,
                    # closed_fours = live_table_bowler.fours,
                    # closed_sixes = live_table_bowler.sixes,
                    # closed_economy = live_table_bowler.economy,
                )
                print('lallalalalal')

                closed_bowler_object = ClosedBowlerScore.objects.filter(bowler_name = bowler_name).first()
                if closed_bowler_object:
                    live_table_bowler.delete()
                    return redirect(transfer_bowler_data)
                    
                    
            
        except Exception as e:
            print(e)
        
    
    return JsonResponse({'status': 'error', 'errors': 'Invalid request method'})


def getScores(request):
    queryset = LiveScore.objects.all()
    return JsonResponse({"scores":list(queryset.values())})




from django.http import JsonResponse
from .models import LiveScore, ClosedScore, Bowler, ClosedBowlerScore

def second_half_notification(request):
    if request.method == 'POST':
        try:
            
            live_scores = LiveScore.objects.all()

            for live_score in live_scores:
                
                closed_score_instance, created = ClosedScore.objects.get_or_create(
                    matchID=live_score.matchID,
                    teamid=live_score.teamid,
                    batsman_name=live_score.batsman_name,
                )

                
                closed_score_instance.runs += live_score.runs
                closed_score_instance.balls += live_score.balls
                closed_score_instance.ones += live_score.ones
                closed_score_instance.twos += live_score.twos
                closed_score_instance.threes += live_score.threes
                closed_score_instance.fours += live_score.fours
                closed_score_instance.sixes += live_score.sixes
                closed_score_instance.wides += live_score.wides
                closed_score_instance.leg_byes += live_score.leg_byes
                closed_score_instance.no_balls += live_score.no_balls
                closed_score_instance.dead_ball += live_score.dead_ball
                closed_score_instance.strike_rate = live_score.calculate_strike_rate()
                closed_score_instance.save()

            
                LiveScore.objects.all().delete()

            
            bowler_scores = Bowler.objects.all()

            for bowler_score in bowler_scores:
                
                closed_bowler_score_instance, created = ClosedBowlerScore.objects.get_or_create(
                    matchID=bowler_score.matchID,
                    teamid=bowler_score.teamid,
                    bowler_name=bowler_score.name,
                )

                
                closed_bowler_score_instance.closed_overs += bowler_score.overs
                closed_bowler_score_instance.closed_maidens += bowler_score.maidens
                closed_bowler_score_instance.closed_runs += bowler_score.runs
                closed_bowler_score_instance.closed_balls += bowler_score.balls
                closed_bowler_score_instance.closed_wickets += bowler_score.wickets
                closed_bowler_score_instance.closed_no_balls += bowler_score.no_balls
                closed_bowler_score_instance.closed_fours += bowler_score.fours
                closed_bowler_score_instance.closed_sixes += bowler_score.sixes
                closed_bowler_score_instance.closed_economy += bowler_score.economy
                closed_bowler_score_instance.save()

            
            Bowler.objects.all().delete()





            return JsonResponse({'status': 'success', 'message': 'Data transferred and deleted successfully'})

        except Exception as e:
            
            return JsonResponse({'status': 'error', 'message': str(e)})

    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})





# live view of batsman score

def getScoreslive(request):
    queryset = LiveScore.objects.all()
    return JsonResponse({"scores":list(queryset.values())})





def admin_add_sponser(request):
    if request.user.is_authenticated :
        if request.method == "POST":
            form = SponsersModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Sponsers added successfully")
                return redirect(admin_add_sponser)
            else :
                messages.error(request, "Error in adding sponser")
        else :
            form = SponsersModelForm()
        return render(request, 'sponser.html' , {'form':form })
    else :
        return redirect(login)


def admin_all_sponsers(request) :
    if request.user.is_authenticated :
        sponser = sponsers.objects.all()
        return render(request, 'all-sponsers.html', {"sponsers" : sponser})
    else :
        return redirect(login)
    

def  delete_sponser(request,id):
    if request.user.is_authenticated:
        sponser = sponsers.objects.filter(id=id).first()
        sponser.delete()
        return redirect(admin_all_sponsers)
    else:
        return redirect(login)
    

def update_sponsers(request,id):
    if request.user.is_authenticated:
        sponser = sponsers.objects.filter(id=id).first()
        if request.method == 'POST':
            form = SponsersUpdateModelForm(request.POST, request.FILES, instance=sponser)
            if form.is_valid():
                form.save()
                messages.success(request,"Sponser updated Successfully!")
                return redirect(admin_all_sponsers)
            else:
                messages.error(request,'Please correct the error below')
        else :
            form =  SponsersUpdateModelForm(instance=sponser)
        return render(request, 'update-sponser.html',{ 'form' : form } )
    else:
        return redirect(login)
    




def admin_add_banner(request) :
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BannersModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,"Banner added successfully!")
                return redirect(admin_add_banner)
            else:
                messages.error(request,'Error in adding banner')
        else :
            form = BannersModelForm()
        return render(request, 'banner.html',{"form" : form})
    else :
        return redirect(login)
    

def admin_all_banner(request):
    if request.user.is_authenticated:
        carousals = CarouselItem.objects.all()
        return render(request , "all-banners.html" , {"carousals":carousals })
    else:
        return redirect(login)
    


def update_banner(request,id):
    if request.user.is_authenticated:
        banner = CarouselItem.objects.filter(id=id).first()
        if request.method == 'POST':
            form = BannerUpdateModelForm(request.POST,request.FILES, instance=banner)
            if form.is_valid():
                form.save()
                messages.success(request,"Banner updated Successfully!")
                return redirect(admin_all_banner)
            else:
                messages.error(request,"Please correct the error below.")
        else:
            form = BannerUpdateModelForm(instance=banner)
        return render(request, 'update-banner.html', {'form' : form}) 
    else:
        return redirect(login)  
    


def delete_banner(request,id):
    if request.user.is_authenticated :
        banner = CarouselItem.objects.filter(id=id).first()
        banner.delete()
        return redirect(admin_all_banner)
    else:
        return redirect(login)     
