from django import forms
from .models import *



class TeamInsertForm(forms.ModelForm):
    class Meta:
        model = TeamDetails
        fields =  ["Team_name","Team_logo","Team_owner","Team_address","Team_email","Team_phone_number"] 

        widgets = {
            'Team_name': forms.TextInput(attrs={'placeholder': 'Enter team name ', 'class' : "form-control"}),
            'Team_logo': forms.ClearableFileInput(attrs={'class': 'btn-2', 'class' : 'form-control'}),
            'Team_owner': forms.TextInput(attrs={'placeholder': 'Enter team owner', 'class' : 'form-control'}),
            'Team_address': forms.TextInput(attrs={'placeholder': 'Enter team address', 'class' : 'form-control'}),
            'Team_email': forms.TextInput(attrs={'placeholder': 'Enter team email', 'class' : 'form-control'}),
            'Team_phone_number': forms.TextInput(attrs={'placeholder': 'Enter team phone number', 'class' : 'form-control'}),
        # Add more fields as needed
    }
        
class TeamUpdateForm(forms.ModelForm):
    class Meta :
        model = TeamDetails
        fields = "__all__"


        widgets = {

            'Team_name': forms.TextInput(attrs={'placeholder': 'Enter team name ', 'class' : "form-control"}),
            'Team_logo': forms.ClearableFileInput(attrs={'class': 'btn-2', 'class' : 'form-control'}),
            'Team_owner': forms.TextInput(attrs={'placeholder': 'Enter team owner', 'class' : 'form-control'}),
            'Team_address': forms.TextInput(attrs={'placeholder': 'Enter team address', 'class' : 'form-control'}),
            'Team_email': forms.TextInput(attrs={'placeholder': 'Enter team email', 'class' : 'form-control'}),
            'Team_phone_number': forms.TextInput(attrs={'placeholder': 'Enter team phone number', 'class' : 'form-control'}),
        }


class PlayerInsertForm(forms.ModelForm) :
    class Meta :
        model = PlayersDetails
        fields = "__all__"

        widgets = {

            'Player_name': forms.TextInput(attrs={'placeholder': 'Enter Player name ', 'class' : "form-control"}),
            'Player_team': forms.Select(attrs={ 'class' : 'form-control'}),
            'Player_logo': forms.FileInput(attrs={'placeholder': 'Select Logo', 'class' : 'form-control'}),
            'Player_category': forms.Select(attrs={'placeholder': 'Enter Category', 'class' : 'form-control'}),
            'Player_location': forms.TextInput(attrs={'placeholder': 'Enter Location', 'class' : 'form-control'}),
            'Player_address': forms.TextInput(attrs={'placeholder': 'Enter Addtress', 'class' : 'form-control'}),
            'Player_email': forms.EmailInput(attrs={'placeholder': 'Enter Player Email', 'class' : 'form-control'}),
            'Player_phone_number': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Phone Number'}),
        }


class PlayerUpdateForm(forms.ModelForm) :
    class Meta :
        model = PlayersDetails
        fields = "__all__"

        widgets = {

            'Player_name': forms.TextInput(attrs={'placeholder': 'Enter Player name ', 'class' : "form-control"}),
            'Player_team': forms.Select(attrs={ 'class' : 'form-control'}),
            'Player_logo': forms.FileInput(attrs={'placeholder': 'Select Logo', 'class' : 'form-control'}),
            'Player_category': forms.TextInput(attrs={'placeholder': 'Enter Category', 'class' : 'form-control'}),
            'Player_location': forms.TextInput(attrs={'placeholder': 'Enter Location', 'class' : 'form-control'}),
            'Player_address': forms.TextInput(attrs={'placeholder': 'Enter Addtress', 'class' : 'form-control'}),
            'Player_email': forms.EmailInput(attrs={'placeholder': 'Enter Player Email', 'class' : 'form-control'}),
            'Player_phone_number': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Phone Number'}),
        }


class SeasonAddingForm(forms.ModelForm) :
    class Meta:
        fields = "__all__"
        model = Season

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Season Name ','class' : 'form-control'}),
            
        }


class SeasonUpdateForm(forms.ModelForm) :
    class Meta:
        fields = "__all__"
        model = Season

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Season Name ','class' : 'form-control'}),
            
        }



class MatchedTeamsUpdateForm(forms.ModelForm):
    class Meta :
        model = UpcomingTeam
        fields = ['Match_date','Match_type','Ground_name','TeamA','TeamB','Match_season']


        widgets = {
            'Match_date': forms.DateTimeInput(attrs={'class' : 'form-control'}),
            'Match_type': forms.TextInput(attrs={'class' : 'form-control'}),
            'Ground_name': forms.TextInput(attrs={'class' : 'form-control'}),
            'TeamA': forms.Select(attrs={'class' : 'form-control'}),
            'TeamB': forms.Select(attrs={'class' : 'form-control'}),
            'Match_season': forms.Select(attrs={'class' : 'form-control'}),
            

        }


class SponsersModelForm(forms.ModelForm) :
    class Meta :
        model = sponsers
        fields="__all__"


        widgets = {
            'sponser_logo': forms.FileInput(attrs={'class' : 'form-control'}),
            'sponser_name': forms.TextInput(attrs={'class' : 'form-control'}),
        }



class SponsersUpdateModelForm(forms.ModelForm) :
    class Meta :
        model = sponsers
        fields="__all__"


        widgets = {
            'sponser_logo': forms.FileInput(attrs={'class' : 'form-control'}),
            'sponser_name': forms.TextInput(attrs={'class' : 'form-control'}),
        }


class BannersModelForm (forms.ModelForm):
    class Meta :
        model = CarouselItem
        fields = "__all__"






class BannerUpdateModelForm(forms.ModelForm) :
    class Meta :
        model = CarouselItem
        fields = "__all__"