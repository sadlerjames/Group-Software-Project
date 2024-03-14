#Authored by Finn Ashby
from treasurehunt import models
'''
(STATIC METHOD) Treasure.getTreasure(id,name)    returns a Treasure object given eiter id or name

a.addStage(stage_no,    (str)type,   (str)info,   (int)no_points) stage_no must be not None

'''
class Treasure:
    def __init__(self,name,noPoints=10,img='/img/Default.png',creating=True,id=None):
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
        return self.id
    def getPoints(self):
        return self.id
    

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
            
    def addStage(self,stage_no,type='quiz',info='1',no_points=10):
        models.Stage.objects.create(hunt=models.TreasureHunt.objects.get(hunt_id=self.id),order=stage_no,activity_type=type,information=info,no_points=no_points)
    def getStagePoints(self,stage_no):
        return models.Stage.objects.get(hunt=self.id,order=stage_no).no_points
    
    def getStageInfo(self,stage_no):
        return models.Stage.objects.get(hunt=self.id,order=stage_no).information
    
    def getStageActivity(self,stage_no):
        return models.Stage.objects.get(hunt=self.id,order=stage_no).activity_type


    def getImage(self):
        return models.TreasureHunt.objects.get(hunt_id=self.id).image
        
    

#a=Treasure('Polo1',256)
#a.addStage(1)
#print("1231231231232POLOPOPOPOOPLPOKPOASKDPOASKASPDKASDOKAASKDPAKDSP")