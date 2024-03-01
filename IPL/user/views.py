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
from django.db.models import Sum
# Create your views here.

# Create your views here.
def home(request) :

    upcoming = UpcomingTeam.objects.all()
    teams = TeamDetails.objects.all()
    banners = CarouselItem.objects.all()
    sponser = sponsers.objects.all()

    live = LiveMatchView.objects.order_by("-pk")[:1]
    completed = CompletedMatch.objects.all()


    # Get a list of duplicate match_ids
    duplicate_match_ids = CompletedMatch.objects.values('match_id').annotate(total=models.Count('match_id')).filter(total__gt=1)

    # Loop through duplicate match_ids and keep one record, delete others
    for duplicate in duplicate_match_ids:
        match_id = duplicate['match_id']

        # Get all records with the same match_id
        duplicate_records = CompletedMatch.objects.filter(match_id=match_id)

        # Keep one record (you can choose any logic based on your requirements)
        record_to_keep = duplicate_records.first()

        # Delete other duplicate records
        duplicate_records.exclude(pk=record_to_keep.pk).delete()
    


    # Get a list of duplicate match_ids
    duplicate_match_ids = LiveMatchView.objects.values('matchid').annotate(total=models.Count('matchid')).filter(total__gt=1)

    # Loop through duplicate match_ids and keep one record, delete others
    for duplicate in duplicate_match_ids:
        match_id = duplicate['matchid']

        # Get all records with the same match_id
        duplicate_records = LiveMatchView.objects.filter(matchid=match_id)

        # Keep one record (you can choose any logic based on your requirements)
        record_to_keep = duplicate_records.first()

        # Delete other duplicate records
        duplicate_records.exclude(pk=record_to_keep.pk).delete()
    

    context = {
        'upcoming_match' : upcoming,
        'teams': teams,
        'bannerItems': banners,
        'sponserItem' : sponser,
        'liveMatches' : live,
        # 'teams':team,
        "completeds" : completed


    }
    return render(request, 'index.html', context)


def teams(request) :
    teams = TeamDetails.objects.all()
    return render(request,'teams.html',{ "teams":teams})



def players(request,id) :
    team_id= TeamDetails.objects.filter(id=id).first()
    players_id = PlayersDetails.objects.filter(Player_team_id=id)
    teams = TeamDetails.objects.all()



    context = {
        'players':players_id,
        'team' : team_id,
        'teams':teams,
    
    }

    return render(request, 'players.html',context)



def profile(request,id) :
    team_players_info =PlayersDetails.objects.all()
    player_details = PlayersDetails.objects.filter(id=id).first()

    player_name = player_details.Player_name
    player_score = ClosedBowlerScore.objects.filter(bowler_name=player_name)


    # participat all matchus counyt
    
    if player_score:
        matches_played_count = ClosedBowlerScore.objects.filter(bowler_name=player_name).count()
        print(f"{player_name} has played {matches_played_count} matches.")
    else:
        matches_played_count = 0

    #  Player Got totral runs
    if player_score.exists():
        total_runs = player_score.aggregate(Sum('closed_runs'))['closed_runs__sum']
        print(f"{player_name} scored a total of {total_runs} runs in ")
    else:
        print(f"No records found for {player_name} in ")
        total_runs = 0

    # Total Balls count
    if player_score.exists():
        avg_balls_count =  player_score.aggregate(Sum('closed_balls'))['closed_balls__sum']
        print(f"{player_name} Bowled  a total of {avg_balls_count} bowls in ")
    else :
        avg_balls_count = 0

    # Total wickets count
    if player_score.exists():
        avg_wickets_count =  player_score.aggregate(Sum('closed_wickets'))['closed_wickets__sum']
        print(f"{player_name}  Wickets  a total of {avg_wickets_count} wickets in ")
    else :
        avg_wickets_count = 0






    #  bateed sections 
    player_batsman_score = ClosedScore.objects.filter(batsman_name=player_name)

    if player_batsman_score:
        batsman_played_count = ClosedScore.objects.filter(batsman_name=player_name).count()
        print(f"{player_name} has played {batsman_played_count} matches.")
    else:
        batsman_played_count = 0


    if player_batsman_score.exists():
        batsman_total_runs = player_batsman_score.aggregate(Sum('runs'))['runs__sum']
        print(f"{player_name} has score total runs  {batsman_total_runs} .")
    else :
        batsman_total_runs = 0


    if player_batsman_score.exists():
        batsman_total_strike_rights = player_batsman_score.aggregate(Sum('strike_rate'))['strike_rate__sum']
        print(f"Strike Rate is {round((batsman_total_strike_rights/batsman_played_count),2)}")

    else :
        batsman_total_strike_rights = 0


     # Player's highest score
    if player_batsman_score.exists():
        player_highest_score = player_batsman_score.order_by('-runs').first()
        print(f"{player_name}'s highest score is {player_highest_score.runs}")
    else:
        player_highest_score = None
        print(f"{player_name} has not scored any runs.")  # Adjust the message as needed

    # Player's total sixes
    if player_batsman_score.exists():
        player_sixes =  player_batsman_score.aggregate(Sum('sixes'))['sixes__sum']
        print(f"{player_name} has score total sixes  {player_sixes} .")

    else :
        player_sixes = 0

    
    # Player's total fours
    if player_batsman_score.exists():
        player_fours =  player_batsman_score.aggregate(Sum('fours'))['fours__sum']
        print(f"{player_name} has score total fours  {player_fours} .")

    else :
        player_fours = 0




        


    context = {
        "player" : player_details,
        "team" : team_players_info,
        "matches_played_count" : matches_played_count,
        "total_runs" : total_runs,
        "avg_balls_count" : avg_balls_count,
        "avg_wickets_count" : avg_wickets_count,
        "player_highest_score" : player_highest_score,
        "player_sixes" : player_sixes,
        'player_fours' : player_fours,
        # batted sections 

        "batsman_played_count" : batsman_played_count,
        "batsman_total_runs": batsman_total_runs ,
        "batsman_total_strike_rights" : batsman_total_strike_rights    

    }
    return render(request, 'profile.html',context)




def contact(request) :
    return render(request, 'contact.html')



def sponser(request) :
    sponsers_item = sponsers.objects.all()
    return render(request, 'sponsers.html',{ "sponsers":sponsers_item})





def point_table(request):
    # Get all records from CompletedMatch model
    point_table = CompletedMatch.objects.all()

    # Extract teamids from CompletedMatch records
    team_ids = [team_id.team1.TeamA.pk for team_id in point_table] + [team_id.team2.TeamB.pk for team_id in point_table]

    # Get unique team names from TeamDetails model based on team_ids
    unique_team_ids = set(team_ids)
    teams_name_objects = TeamDetails.objects.filter(id__in=unique_team_ids)

    # Use Counter to count the occurrences of each team ID
    team_id_counter = Counter(team_ids)


    # Create a list of dictionaries containing team names and corresponding points


    teams_with_points = []
        

    for team_name in teams_name_objects:
        print("This is teams: ", team_name.Team_name)  # Print team names

        # Get matches count for the team
        matches_count = team_id_counter.get(team_name.pk, 0)
        print(f"Team ID: {team_name.pk}, Team Name: {team_name.Team_name}, Matches Count: {matches_count}")

        # Calculate how many matches the team has won
        matches_won_count = CompletedMatch.objects.filter(won_team=team_name.pk).count()
        print(f"Team ID: {team_name.pk}, Team Name: {team_name.Team_name}, Matches Won Count: {matches_won_count}")


        matches_lost_count = CompletedMatch.objects.filter(lose_team=team_name.pk).count()

        print(f"Team ID: {team_name.pk}, Team Name: {team_name.Team_name}, Matches Won Count: {matches_won_count}, Matches Lost Count: {matches_lost_count}")


        points_for_win = 2

        total_points = (matches_won_count * points_for_win)







        teams_with_points.append({
            "team_id": team_name.pk,
            "team_name": team_name.Team_name,
            "team_logo": team_name.Team_logo,
            "matches_count": matches_count,
            "matches_won_count" : matches_won_count,
            "matches_lost_count" : matches_lost_count,
            "total_points" : total_points
        })

    context = {
        "teams_with_points": teams_with_points,
    }
    return render(request, 'pointtable.html',context)




def fixtures(request):
    return render(request, 'fixtures.html') 





def upcoming_match(request,id) :
    match_datails = UpcomingTeam.objects.filter(id=id)
    match = UpcomingTeam.objects.get(id=id)# first team
    upcoming_match = UpcomingTeam.objects.filter(id=id).first()
    choice = upcoming_match.Match_status
    toss = match.Match_toss
    batsmen = None
    bowler = None



    if choice == "1":
        if upcoming_match.TeamA == toss:
            batsmen1 = upcoming_match.TeamA
            batsmen = match.TeamA_players.all()
            team1_players = PlayersDetails.objects.filter(Player_team=match.TeamA).all()
            bowler2 = upcoming_match.TeamB
            bowler = match.TeamB_playeres.all()
            team2_players = PlayersDetails.objects.filter(Player_team=match.TeamB).all()
        else:
            batsmen1 = upcoming_match.TeamB
            batsmen = match.TeamB_playeres.all()
            team1_players = PlayersDetails.objects.filter(Player_team=match.TeamB).all()
            bowler2 = upcoming_match.TeamA
            bowler = match.TeamA_players.all()
            team2_players = PlayersDetails.objects.filter(Player_team=match.TeamA).all()

    else:
        if upcoming_match.TeamA == toss: 
            batsmen1 = upcoming_match.TeamB
            batsmen = match.TeamB_playeres.all()
            team1_players = PlayersDetails.objects.filter(Player_team=match.TeamB).all()
            bowler2 = upcoming_match.TeamA
            bowler = match.TeamA_players.all()
            team2_players = PlayersDetails.objects.filter(Player_team=match.TeamA).all()

        else:
            batsmen1 = upcoming_match.TeamA
            batsmen= match.TeamA_players.all()
            team1_players = PlayersDetails.objects.filter(Player_team=match.TeamA).all()
            bowler2 = upcoming_match.TeamB
            bowler = match.TeamB_playeres.all()
            team2_players = PlayersDetails.objects.filter(Player_team=match.TeamB).all()

            
    context = {
        "match_team" : match_datails,
        "team1" : batsmen1,
        "team2" : bowler2,
        "batsmen" : batsmen,
        "bowler" : bowler,
        "upcoming_match" : upcoming_match,
        'team1_players' : team1_players,
        'team2_players' : team2_players

    }

    return render(request,'upcoming.html',context)  




def completed(request,match_id_id):
    # Fetch the upcoming match details
    match = UpcomingTeam.objects.filter(id=match_id_id).first()
    
    # Print some details for debugging
    print("Team One:", match.TeamA.pk)
    print("Team Two:", match.TeamB.pk)
    print("Upcoming Match ID:", match.pk)
    
    # Fetch details of the completed match
    completed_id = CompletedMatch.objects.filter(match_id=match_id_id).first()
    print("Completed Match Team ID:", completed_id.team1.TeamA.pk)
    print("Completed Match ID:", completed_id.match_id.pk)

    # Fetch details of batters and bowlers for a closed match
    batters = ClosedScore.objects.filter(matchID=match_id_id).first()
    print("Batters Team ID:", batters.teamid)

    bowlers = ClosedBowlerScore.objects.filter(matchID=match_id_id).first()
    print("Bowlers Team ID:", bowlers.teamid)

    # More debugging prints
    print("Completed Match TeamB Team ID:", completed_id.team2.TeamB.pk)

    teamPlayers = None
    teamBowlersPlayers = None

    # Check if the completed match details match the upcoming match
    if completed_id.match_id.pk == match.pk:
        if completed_id.team1.TeamA.pk == match.TeamA.pk:
            # Fetch details for TeamA batters and bowlers
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team1.TeamA.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamA: {team_score_sum1}")
            
            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team2.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers}")

        elif completed_id.team2.TeamB.pk == match.TeamB.pk:
            # Fetch details for TeamB batters and bowlers
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team2.TeamB.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamB: {team_score_sum1}")
            
            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team1.TeamA.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers}")

    else:
        # Fetch details for TeamB when the completed match does not match TeamA
        if completed_id.team2.TeamB.pk == match.TeamB.pk:
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.match_id.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamB: {team_score_sum1}")

            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers}")

        elif completed_id.team1.TeamA.pk == match.TeamA.pk:
            teamPlayers = ClosedScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team1.TeamA.pk)
            team_score_sum1 = sum(player.runs for player in teamPlayers)
            print(f"Total score for TeamA: {team_score_sum1}")

            teamBowlersPlayers = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team2.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers}")

    # More fetching and prints for TeamB
    if completed_id.match_id.pk == match.pk:
        if completed_id.team2.TeamB.pk == match.TeamB.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team2.TeamB.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team1.TeamA.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers2}")

        elif completed_id.team1.TeamA.pk == match.TeamA.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team1.TeamA.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team2.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers2}")

    else:
        if completed_id.team1.TeamA.pk == match.TeamA.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team1.TeamA.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team2.TeamB.pk)
            print(f"TeamA Bowlers: {teamBowlersPlayers2}")

        elif completed_id.team2.TeamB.pk == match.TeamB.pk:
            teamPlayers2 = ClosedScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team2.TeamB.pk)
            team_score_sum2 = sum(player.runs for player in teamPlayers2)
            print(f"Total score for TeamB: {team_score_sum2}")

            teamBowlersPlayers2 = ClosedBowlerScore.objects.filter(matchID=completed_id.match_id.pk, teamid=completed_id.team1.TeamA.pk)
            print(f"TeamB Bowlers: {teamBowlersPlayers2}")

    # Compare total scores to determine the winner
    if team_score_sum1 > team_score_sum2:
        winner_team = completed_id.team1.TeamA
        print("Winner is TeamA:", winner_team.Team_name)
    elif team_score_sum1 < team_score_sum2:
        winner_team = completed_id.team2.TeamB
        print("Winner is TeamB:", winner_team.Team_name)
    else:
        winner_team = None  # It's a tie

    # Calculate the runs difference for a tie
    if winner_team:
        runs_difference = abs(team_score_sum1 - team_score_sum2)
        print("It's a tie! Runs difference:", runs_difference)


    

    # Prepare context for rendering
    context = {
        "completed": completed_id,
        "teamPlayers": teamPlayers,
        "teamBowlersPlayers" : teamBowlersPlayers,
        "teamPlayers2" : teamPlayers2,
        "teamBowlersPlayers2" : teamBowlersPlayers2,
        "team_score_sum2" : team_score_sum2,
        "team_score_sum1" : team_score_sum1,
        "winner_team" : winner_team,
        "runs_difference" : runs_difference

    }
    return render(request, 'completed.html',context)



def live(request,id):
    match_id = UpcomingTeam.objects.filter(id=id).first()

    context = {
        'match': match_id,
    }
    return render(request,'user-live.html',context)