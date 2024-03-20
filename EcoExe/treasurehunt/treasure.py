#Authored by Finn Ashby
from treasurehunt import models
from django.forms.models import model_to_dict
'''
(STATIC METHOD) Treasure.getTreasure(id,name)    returns a Treasure object given eiter id or name

a.addStage(stage_no,    (str)type,   (str)info,   (int)no_points) stage_no must be not None

'''
#Class to communicate with the treasure hunt part of the database
class Treasure:
    #id will be None if a treasure hunt is being loaded
    def __init__(self,name,noPoints=10,img='treasure_hunt/default.png',creating=True,id=None):
        self.name=name
        self.points=noPoints
        self.img=img
        if(creating):
            #If the treasure object is being created
            a=models.TreasureHunt.objects.create(name=self.name,points=self.points,image=img)
            self.id=a.hunt_id
        else:
            self.id=id
    #Getters
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getPoints(self):
        return self.points
    
    #Returns a treasure object given either the id or name without having to construct a new one
    def getTreasure(id=None,name=None):
        if id==None and name==None:
            raise NotImplementedError("Please pass either an id or name pretty please thanks!")
        elif id!=None:
            a=models.TreasureHunt.objects.get(hunt_id=id)
            return Treasure(a.name,a.points,creating=False,id=a.hunt_id)
        elif name!=None:
            a=models.TreasureHunt.objects.get(name=name)
            return Treasure(a.name,a.points,creating=False,id=a.hunt_id)
        raise NotImplementedError("Pass")

    #Adds a stage to a specific treasure hunt
    def addStage(self,stage_no,activity_id='1',info='1',no_points=10):
        models.Stage.objects.create(hunt=models.TreasureHunt.objects.get(hunt_id=self.id),order=stage_no,activity_id=models.Activities.objects.get(act_id=activity_id),information=info,no_points=no_points)
    def getStagePoints(self,stage_no):
        return models.Stage.objects.get(hunt=self.id,order=stage_no).no_points
    
    def getStageInfo(self,stage_no):
        return models.Stage.objects.get(hunt=self.id,order=stage_no).information
    
    def getStageActivity(self,stage_no):
        a = models.Stage.objects.get(hunt=self.id,order=stage_no)
        return a.activity_id.act_id


    def getImage(self):
        return models.TreasureHunt.objects.get(hunt_id=self.id).image
        
    def addActivity(name,location,activity_type,activity_info,points,location_name):
        a=models.Activities.objects.create(type=activity_type,name=name,info=activity_info,location=location,points=points,location_name=location_name)
        return a.act_id

    #Returns a dictionary  of all activities in the database as a dictionary of dictionaries
    def getActivities():
        #{i.title: i.specs for i in models.Activities.objects.all()}
        a=(models.Activities.objects.values())
        new_dict = {}
        for item in a:
            name = item['act_id']
            new_dict[name] = item
        return new_dict
    #Returns the current stage a player is on for a specific hunt
    def getStageNo(player_name,hunt_id):
        try:
            a=models.UserTreasure.objects.get(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id))
            return a.stage_completed
        except models.UserTreasure.DoesNotExist:
            return 0
            
    #Increments a stage for a player
    #Haven't started the treasure hunt, they will be placed in the database
    def incrementStage(player_name,hunt_id,points=0):
        try:
            #Increment the stage and the number of points then save the entry to the database
            a=models.UserTreasure.objects.get(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id))
            a.stage_completed+=1
            a.no_points+=points
            a.save()
        #Exception occurs if the player isn't in the database yet
        except models.UserTreasure.DoesNotExist:
            models.UserTreasure.objects.create(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id),no_points=0,stage_completed=1)
            a=models.UserTreasure.objects.get(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id))
            a.no_points+=points
            a.save()

    #Returns a list of all the treasure hunts a player is doing and the id of the next stage they are doing
    def getUserStages(player_name):
        entries = models.UserTreasure.objects.filter(player=player_name)
        stages=[]
        stage=[]
        for entry in entries:
            try:
                #If they are doing the treasure hunt
                stage = Treasure.getStageNo(player_name,entry.hunt.hunt_id) + 1 #get the next stage
                hunt = Treasure.getTreasure(id=entry.hunt.hunt_id)
                activityID = hunt.getStageActivity(stage)
                stage=[entry.hunt.hunt_id,stage]
                stages.append(stage)
            #If they aren't doing the treasure hunt, say they are on stage -1 
            except models.Stage.DoesNotExist:
                stages.append([entry.hunt.hunt_id,-1])
                continue
        return stages
        
    #returns a list of  treasure hunt objects a player hasnt done given the user id
    def getNewHunts(user_name):
        hunts=models.TreasureHunt.objects.all()
        newHunts=[]
        for hunt in hunts:
            try:
                #If the user is in a hunt, dont do anything
                models.UserTreasure.objects.get(player=user_name,hunt_id=hunt.hunt_id)
            except models.UserTreasure.DoesNotExist:
                #If the user isn't in a hunt, add it to the list
                newHunts.append(Treasure.getTreasure(id=hunt.hunt_id))
        return newHunts
