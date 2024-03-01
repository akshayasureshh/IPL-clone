from django.shortcuts import render
from dashboard.models import *

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.db.models import Q
from django.urls import reverse

# Create your views here.

def team_owner_login(request):
    # Check if 'user' key is present in the session, if so, redirect to the team-owner-dashboard
    if 'user' in request.session:
        return redirect('team-owner-dashboard')  # Replace 'team-owner-dashboard' with the actual URL or view name

    else:
        if request.method == 'POST':
            owner = request.POST.get('email')
            password = request.POST.get('password')
            print(owner,password)

            user = TeamDetails.objects.filter(Team_email=owner, Team_phone_number=password).first()

            if user is not None:
                request.session['user'] = user.Team_email
                print("andi")
                return redirect('team-owner-dashboard')

            else:
                return redirect(team_owner_login) 

    return render(request, 'owner-login.html')



def team_owner_dashboard(request):
    # Check if 'user' key is present in the session , if not show login page with error message
    if 'user' in request.session:
        # Retrieve the user's email from the session
        email = request.session['user']

        # Retrieve the Team object based on the email
        user = TeamDetails.objects.filter(Team_email=email).first()

        # Check if a user is found
        if user is not None:
            # Retrieve all upcoming matches involving the team
            matchs = UpcomingTeam.objects.filter(Q(TeamA=user.pk) | Q(TeamB=user.pk))

            # Prepare the context for rendering the template
            context = {
                'user': user,
                'tournaments': matchs
            }
            
        else:
            # Redirect to team_owner_login if no user is found in the database
            return redirect(team_owner_dashboard)  # Replace 'team_owner_login' with the actual URL or view name
    else:
        # Redirect to team_owner_login if 'user' key is not present in the session
        return redirect(team_owner_login)  # Replace 'team_owner_login' with the actual URL or view name

    # Render the owner-dashboard.html template with the context
    return render(request, 'owner-dashboard.html', context)



def team_owner_add_players(request):
    # Check if 'user' key is present in the session
    if 'user' in request.session:
        # Retrieve the user's email from the session
        email = request.session['user']

        # Retrieve the Team object based on the email
        user = TeamDetails.objects.filter(Team_email=email).first()

        # Check if a user is found
        if user is not None:
            # Check if the request method is POST
            if request.method == 'POST':
                # Retrieve player information from the POST data
                name = request.POST.get('name')
                image = request.FILES.get('image')
                team1 = TeamDetails.objects.filter(id=user.pk).first()
                category = request.POST.get('category')
                location = request.POST.get('location')
                address = request.POST.get('address')
                email = request.POST.get('email')
                phone = request.POST.get("phone")

                # Create a new Player instance and save it to the database
                players = PlayersDetails()
                players.Player_name = name
                players.Player_logo = image
                players.Player_team = team1
                players.Player_category = category
                players.Player_location = location
                players.Player_address = address
                players.Player_email = email
                players.Player_phone_number = phone
                players.save()

                # Display success message
                messages.success(request, "Player Added Successfully!")

        else:
            # Display error message if no user is found in the database
            messages.error(request, 'Please make sure you have filled out all fields correctly!')

    else:
        # Redirect to team_owner_login if 'user' key is not present in the session
        return redirect('team_owner_login')  # Replace 'team_owner_login' with the actual URL or view name

    # Prepare the context for rendering the template
    context = {
        "user": user
    }

    # Render the owner-add-players.html template with the context
    return render(request, 'owner-add-players.html', context)



def owner_team_based_all_players(request):
    # Check if 'user' key is present in the session
    if 'user' in request.session:
        # Retrieve the user's email from the session
        email = request.session['user']

        # Retrieve the Team object based on the email
        user = TeamDetails.objects.filter(Team_email=email).first()

        # Check if a user is found
        if user is not None:
            # Retrieve all players belonging to the user's team
            players = PlayersDetails.objects.filter(Player_team_id=user.pk)

        else:
            # Redirect to team_owner_login if no user is found in the database
            return redirect('team_owner_login')  # Replace 'team_owner_login' with the actual URL or view name

    else:
        # Redirect to team_owner_login if 'user' key is not present in the session
        return redirect('team_owner_login')  # Replace 'team_owner_login' with the actual URL or view name

    # Prepare the context for rendering the template
    context = {
        "players": players,
        'user': user
    }

    # Render the owner-all-players.html template with the context
    return render(request, 'owner-all-players.html', context)


def owner_player_delete(request, id):
    # Check if 'user' key is present in the session
    if 'user' in request.session:
        # Retrieve the player object with the given ID and delete it
        player = PlayersDetails.objects.filter(id=id).delete()

        # Redirect to owner_team_based_all_players after deleting the player
        return redirect(owner_team_based_all_players)  # Replace 'owner_team_based_all_players' with the actual URL or view name

    else:
        # Redirect to team_owner_login if 'user' key is not present in the session
        return redirect('team_owner_login')  # Replace 'team_owner_login' with the actual URL or view name

    
def owner_edit_player(request, id):
    # Check if 'user' key is present in the session
    if 'user' in request.session:
        # Retrieve the user's email from the session
        user = request.session['user']

        # Retrieve the Player object with the given ID
        player_id = PlayersDetails.objects.filter(id=id).first()

        # Check if a user and player are found
        if user is not None and player_id is not None:
            # Check if the request method is POST
            if request.method == 'POST':
                # Retrieve player information from the POST data
                name = request.POST.get('name')
                image = request.FILES.get('image')
                team = request.POST.get("team")
                team1 = TeamDetails.objects.filter(id=team).first()
                category = request.POST.get('category')
                location = request.POST.get('location')
                address = request.POST.get('address')
                email = request.POST.get('email')
                phone = request.POST.get("phone")

                # Update the Player object with the new information
                players = PlayersDetails.objects.get(id=id)
                players.Player_name = name
                players.Player_logo = image
                players.Player_team = team1
                players.Player_category = category
                players.Player_location = location
                players.Player_address = address
                players.Player_email = email
                players.Player_phone_number = phone
                players.save()

                # Display success message and redirect to owner_team_based_all_players
                messages.success(request, 'Player has been updated successfully!')
                return redirect('owner_team_based_all_players')
            else:
                # Display error message if the request method is not POST
                messages.error(request, 'Please check the form; something went wrong')
        else:
            # Redirect to team_owner_login if no user or player is found in the database
            return redirect('team_owner_login')  

    else:
        # Redirect to team_owner_login if 'user' key is not present in the session
        return redirect('team_owner_login')  

    # Render the owner_player_update.html template with the player information
    return render(request, "owner_player_update.html", {"player_id": player_id})

    

def owner_team_all_matches(request):
    # Check if 'user' key is present in the session
    if 'user' in request.session:
        # Retrieve the user's email from the session
        user = TeamDetails.objects.filter(Team_email=request.session["user"]).first()

        # Check if a user is found
        if user is not None:
            # Retrieve all upcoming matches involving the team
            matches = UpcomingTeam.objects.filter(Q(TeamA=user.pk) | Q(TeamB=user.pk))

        else:
            # Return a 404 error if no user is found in the database
            raise Http404("Your Team is not found")

    else:
        # Redirect to team_owner_login if 'user' key is not present in the session
        return redirect('team_owner_login')  # Replace 'team_owner_login' with the actual URL or view name

    # Prepare the context for rendering the template
    context = {
        "user": user,
        "matches": matches
    }

    # Render the owner-all-match.html template with the context
    return render(request, 'owner-all-match.html', context)
 


def owner_selecte_players_on_match(request, id):
    # Check if 'user' key is present in the session
    if 'user' in request.session:
        # Retrieve the user's email from the session
        user = request.session["user"]

        # Retrieve match information based on the given ID
        match_info = UpcomingTeam.objects.filter(id=id).first()

        # Retrieve the Team object based on the user's email
        team = TeamDetails.objects.filter(Team_email=user).first()

        # Retrieve all players belonging to the user's team
        players = PlayersDetails.objects.filter(Player_team_id=team.pk)

        # Check if the request method is POST
        if request.method == 'POST':
            # Retrieve selected players from the POST data
            selected_players = request.POST.getlist('team')

            # Check if the user's team is team1 or team2 in the match_info
            if match_info.TeamA == team:
                # Add selected players to team1_players in the match_info
                match_info.TeamA_players.add(*selected_players)
                print("team one")
                return redirect('owner_team_all_matches')  # Replace 'owner_team_all_matches' with the actual URL or view name

            elif match_info.TeamB == team:
                # Add selected players to team2_players in the match_info
                match_info.TeamB_playeres.add(*selected_players)
                print("team two")
                return redirect('owner_team_all_matches')  # Replace 'owner_team_all_matches' with the actual URL or view name

            else:
                # Raise an error if the user doesn't belong to this match
                raise ValueError("The User Doesn't Belong to this Match")

        # Prepare the context for rendering the template
        context = {
            "players": players,
            'user': team
        }

    else:
        # Redirect to team_owner_login if 'user' key is not present in the session
        return redirect('team_owner_login')  # Replace 'team_owner_login' with the actual URL or view name

    # Render the owner-select-players.html template with the context
    return render(request, 'owner-select-players.html', context)

        
   
    
def owner_logout(request):
    # Check if 'user' key is present in the session
    if 'user' in request.session:
        # If present, delete the 'user' key from the session
        del request.session['user']

        # Redirect to the team_owner_login view after logout
        return redirect('team_owner_login')  # Replace 'team_owner_login' with the actual URL or view name

    else:
        # If 'user' key is not present, return a Forbidden response
        return HttpResponseForbidden("Please Login First!")



