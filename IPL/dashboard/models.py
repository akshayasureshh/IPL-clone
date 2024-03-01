from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class TeamDetails(models.Model):

    Team_name = models.CharField(max_length=100,null=True)
    Team_logo = models.ImageField(upload_to='images/',null=True, default="images/team.jpg")
    Team_owner = models.CharField(max_length=100,null=True)
    Team_address = models.CharField(max_length=255,null=True)
    Team_email = models.EmailField(max_length=100,null=True)
    Team_phone_number = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.Team_name
    
    def getImage(self, *args, **kwargs):
        if not self.Team_logo:
            self.Team_logo="images/team.jpg"
        super().save(*args,**kwargs)  # Call the real

    class Meta:
        db_table = 'Teams'



class Season(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "SEASON"



class PlayersDetails(models.Model):

    Player_name = models.CharField(max_length=100)
    Player_team = models.ForeignKey(TeamDetails, on_delete=models.CASCADE)
    Player_logo = models.ImageField(upload_to='images/' , default='images/batsmen.jpg')
    Category = [
        ('', 'Select category'),
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All rounder', 'All rounder'),
        ('Wicket', 'Wicket keeper,Batsman')
    ]
    Player_category = models.CharField(max_length=100, choices=Category)
    Player_location = models.CharField(max_length=255)
    Player_address = models.CharField(max_length=255)
    Player_email = models.EmailField(max_length=100)
    Player_phone_number = models.CharField(max_length=10)

    def _str_(self):
        return self.Player_name
    
    class Meta :
        db_table = 'Players_details'


# Tournament Shedule 
class UpcomingTeam(models.Model) :
    Match_date = models.DateTimeField()
    Match_season = models.ForeignKey(Season, on_delete=models.CASCADE,null=True)
    Match_type = models.CharField(max_length = 100,null=True)
    Match_toss = models.CharField(max_length = 100,null=True)
    Match_status = models.CharField(max_length = 100,null=True)
    Ground_name = models.CharField(max_length= 100,null=True)
    TeamA = models.ForeignKey(TeamDetails,max_length = 100,on_delete=models.CASCADE,related_name = 'team1')
    TeamA_players = models.ManyToManyField(PlayersDetails, max_length=100, related_name="Team1_palyers")
    TeamB = models.ForeignKey(TeamDetails,max_length = 100,on_delete = models.CASCADE,related_name = "team2")
    TeamB_playeres = models.ManyToManyField(PlayersDetails, max_length=100, related_name="Team2_name")


    class Meta :
        db_table = 'Tournament'




class LiveMatchView(models.Model) :
    matchid = models.ForeignKey(UpcomingTeam,on_delete=models.CASCADE,null=True ,related_name="matchid")
    Match_date = models.ForeignKey(UpcomingTeam,on_delete=models.CASCADE,null=True,related_name="date")
    Match_season = models.ForeignKey(UpcomingTeam, on_delete=models.CASCADE,null=True,related_name="season")
    Match_type = models.ForeignKey(UpcomingTeam,on_delete=models.CASCADE,max_length = 100,null=True,related_name="type")
    Match_toss = models.ForeignKey(UpcomingTeam,on_delete=models.CASCADE,max_length = 100,null=True,related_name="toss")
    Match_status = models.ForeignKey(UpcomingTeam,on_delete=models.CASCADE,max_length = 100,null=True,db_column='Status',related_name="live_status")
    Ground_name = models.ForeignKey(UpcomingTeam,on_delete=models.CASCADE,max_length= 100,null=True,related_name='ground')
    TeamA = models.ForeignKey(UpcomingTeam,max_length = 100,on_delete=models.CASCADE,related_name = 'teamA')
    # TeamA_players = models.ManyToManyField(PlayersDetails, max_length=100, related_name="Team1_palyers")
    TeamB = models.ForeignKey(UpcomingTeam,max_length = 100,on_delete = models.CASCADE,related_name = "teamB")
    # TeamB_playeres = models.ManyToManyField(PlayersDetails, max_length=100, related_name="Team2_name")


    class Meta :
        db_table = 'live'


class LiveBattingScore(models.Model):
    batsman_name = models.CharField(max_length=255)
    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    ones = models.IntegerField(default=0)
    twos = models.IntegerField(default=0)
    threes = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    wides = models.IntegerField(default=0)
    leg_byes = models.IntegerField(default=0)
    dead_ball = models.IntegerField(default=0)
    strike_rate = models.FloatField(default=0.0)

    def calculate_strike_rate(self):
        if self.balls > 0:
            return round((self.runs / self.balls) * 100, 2)
        else:
            return 0.0000000000000
    
    class Meta :
        db_table = "liveBatting"





class CarouselItem(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(
        upload_to='carousel_images/')

    def _str_(self):
        return self.title
    class Meta :
        db_table = "CarouselItem"







class sponsers(models.Model):

    sponser_logo = models.ImageField(upload_to='sponser_logos/', default="images/batsmen.jpg")
    sponser_name = models.CharField(max_length = 255)


    def _str_(self):
        return self.sponser_name
    
    class Meta :
        db_table = "Sponsers"

class Team_login(models.Model):
    ownerEmail = models.EmailField(max_length=255)
    ownerPassword = models.CharField(max_length=255)


    




#akshaya
class LiveScore(models.Model):
    matchID = models.CharField(default=0,max_length=300)
    teamid = models.CharField(max_length=300,null=True)
    batsman_name = models.CharField(max_length=255)
    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    ones = models.IntegerField(default=0)
    twos = models.IntegerField(default=0)
    threes = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    wides = models.IntegerField(default=0)
    leg_byes = models.IntegerField(default=0)
    no_balls = models.IntegerField(default=0)
    dead_ball = models.IntegerField(default=0)
    out_mode = models.CharField(max_length=400,null=True)
    out_took_player = models.CharField(max_length=400,null=True)
    strike_rate = models.FloatField(default=0.0)

    def calculate_strike_rate(self):
        if self.balls > 0:
            return round((self.runs / self.balls) * 100, 2)
        else:
            return 0.0
        
    class Meta :
        db_table = "LiveScore"


class Bowler(models.Model):
    matchID = models.CharField(default=0,max_length=300)
    teamid = models.CharField(max_length=300,null=True)
    name = models.CharField(max_length=255)
    overs = models.FloatField(default=0)
    maidens = models.IntegerField(default=0)
    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    no_balls = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    economy = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        
        if self.overs > 0:
            self.economy = round(self.runs / self.overs, 2)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name
    
    class Meta :
        db_table = "liveBowler"


@receiver(post_save, sender=Bowler)
def update_bowler_economy(sender, instance, **kwargs):
    
        if instance.overs > 0:
            instance.economy = round(instance.runs / instance.overs, 2)
            instance.save()


class ClosedScore(models.Model):
    matchID = models.CharField(default=0,max_length=300)
    teamid = models.CharField(max_length=300,null=True)
    batsman_name = models.CharField(max_length=255)
    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    ones = models.IntegerField(default=0)
    twos = models.IntegerField(default=0)
    threes = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    wides = models.IntegerField(default=0)
    leg_byes = models.IntegerField(default=0)
    no_balls = models.IntegerField(default=0)
    dead_ball = models.IntegerField(default=0)
    out_mode = models.CharField(max_length=400,null=True)
    out_took_player = models.CharField(max_length=400,null=True)
    strike_rate = models.FloatField(default=0.0)


    class  Meta :
        db_table = "ClosedScore"


class OutMode(models.Model):
    matchID = models.CharField(default=0,max_length=300)
    teamid = models.CharField(max_length=300,null=True)
    name = models.CharField(max_length=300, null=True)
    out_mode = models.CharField(max_length=400)
    out_took_player = models.CharField(max_length=400, null=True)
    selected_batsman = models.CharField(max_length=300, null=True)  # Add this field


    class  Meta :
        db_table = "OutMode"

class ClosedBowlerScore(models.Model):
    matchID = models.CharField(default=0,max_length=300)
    teamid = models.CharField(max_length=300,null=True)
    bowler_name = models.CharField(max_length=255)
    closed_overs = models.FloatField(default=0)
    closed_maidens = models.IntegerField(default=0)
    closed_runs = models.IntegerField(default=0)
    closed_balls = models.IntegerField(default=0)
    closed_wickets = models.IntegerField(default=0)
    closed_no_balls = models.IntegerField(default=0)
    closed_fours = models.IntegerField(default=0)
    closed_sixes = models.IntegerField(default=0)
    closed_economy = models.FloatField(default=0)

    def _str_(self):
        return f"{self.bowler_name} - Closed Bowler Score"
    

    def save(self, *args, **kwargs):
        if self.closed_overs > 0:
            self.closed_economy = round(self.closed_runs / self.closed_overs, 2)
        super().save(*args, **kwargs)

    def _str_(self):
        return self.bowler_name
    
    class  Meta :
        db_table = "ClosedBowlerScore"


@receiver(post_save, sender=ClosedBowlerScore)
def update_bowler_economy(sender, instance, **kwargs):
    if instance.closed_overs > 0:      instance.closed_economy = round(instance.closed_runs / instance.closed_overs, 2)
    instance.save()




class CompletedMatch(models.Model):
    match_id = models.ForeignKey(UpcomingTeam,on_delete=models.CASCADE,related_name='completed')
    season = models.ForeignKey(UpcomingTeam, on_delete = models.CASCADE, related_name = "completed_season")
    type = models.ForeignKey(UpcomingTeam, on_delete = models.CASCADE, related_name= "completed_type")
    toss = models.ForeignKey(UpcomingTeam, on_delete = models.CASCADE, related_name = "completed_toss")
    status = models.ForeignKey(UpcomingTeam, on_delete = models.CASCADE, related_name = "completed_status")
    ground = models.ForeignKey(UpcomingTeam, on_delete = models.CASCADE, related_name = "completed_ground")
    team1 = models.ForeignKey(UpcomingTeam, on_delete = models.CASCADE, related_name = "completed_team1",)
    team2  = models.ForeignKey(UpcomingTeam, on_delete = models.PROTECT, related_name = "completed_team2")
    won_team = models.ForeignKey(TeamDetails,on_delete=models.CASCADE,null=True,related_name="wonteam")
    lose_team = models.ForeignKey(TeamDetails,on_delete=models.CASCADE,null=True,related_name="loseteam")

    class Meta :
        db_table  = 'CompletedMatch'