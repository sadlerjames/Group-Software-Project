#Authored by Finn Ashby
from treasurehunt import models
from django.forms.models import model_to_dict
'''
(STATIC METHOD) Treasure.getTreasure(id,name)    returns a Treasure object given eiter id or name

a.addStage(stage_no,    (str)type,   (str)info,   (int)no_points) stage_no must be not None

'''
class Treasure:
    def __init__(self,name,noPoints=10,img='treasure_hunt/default.png',creating=True,id=None):
        self.name=name
        self.points=noPoints
        self.img=img
        if(creating):
            a=models.TreasureHunt.objects.create(name=self.name,points=self.points,image=img)
            self.id=a.hunt_id
        else:
            self.id=id
            
    def getId(self):
        return self.id
    def getName(self):
        return self.name
    def getPoints(self):
        return self.points
    

    def getTreasure(id=None,name=None):
        if id==None and name==None:
            raise NotImplementedError("Please pass either an id or name pretty please thanks!")
        elif id!=None:
            a=models.TreasureHunt.objects.get(hunt_id=id)
            return Treasure(a.name,a.points,creating=False,id=a.hunt_id)
        elif name!=None:
            a=models.TreasureHunt.objects.get(name=name)
            return Treasure(a.name,a.points,creating=False,id=a.hunt_id)
        raise NotImplementedError("Please talk to finn if this prints")
            
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
    
    def getActivities():
        #{i.title: i.specs for i in models.Activities.objects.all()}
        a=(models.Activities.objects.values())
        new_dict = {}
        for item in a:
            name = item['act_id']
            new_dict[name] = item
        return new_dict

    def getStageNo(player_name,hunt_id):
        try:
            a=models.UserTreasure.objects.get(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id))
            return a.stage_completed
        except models.UserTreasure.DoesNotExist:
            return 0
    
    def incrementStage(player_name,hunt_id,points=0):
        try:
            a=models.UserTreasure.objects.get(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id))
            a.stage_completed+=1
            a.no_points+=points
            a.save()
        except models.UserTreasure.DoesNotExist:
            models.UserTreasure.objects.create(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id),no_points=0,stage_completed=1)
            a=models.UserTreasure.objects.get(player=player_name,hunt=models.TreasureHunt.objects.get(hunt_id=hunt_id))
            a.no_points+=points
            a.save()
    
    def getUserStages(player_name):
        entries = models.UserTreasure.objects.filter(player=player_name)
        stages=[]
        stage=[]
        for entry in entries:
            try:
                stage = Treasure.getStageNo(player_name,entry.hunt.hunt_id) + 1 #get the next stage
                hunt = Treasure.getTreasure(id=entry.hunt.hunt_id)
                activityID = hunt.getStageActivity(stage)
                stage=[entry.hunt.hunt_id,stage]
                stages.append(stage)
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
                models.UserTreasure.objects.get(player=user_name,hunt_id=hunt.hunt_id)
            except models.UserTreasure.DoesNotExist:
                newHunts.append(Treasure.getTreasure(id=hunt.hunt_id))
        return newHunts
