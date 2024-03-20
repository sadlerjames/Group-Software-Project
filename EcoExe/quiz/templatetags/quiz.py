#Authored by Finn Ashby
import json
import random
import os
from .. import models
from django.db.utils import IntegrityError
cwd = os.getcwd()
#yprint(cwd)
##create quiz
##open existing quiz
##add questions and answers to quiz
##delete questions and answers to quiz
##delete quiz
##modify questions and answers to quiz
##save to json

#makes exceptions
def exception_maker(exception,message):
    return exception(message)

#finds index of element given list and element
def find(list,a):
    for i in range(len(list)):
        if list[i]==a:
            return i
    return -1

#print(find([0,1,2,3,4,5],0))

'''
quizName is the name of the quiz
questions is a list of strings, each string is a question
answers is a 2d list of strings, each list contains the answers and each string is an answer
NOTE answer[i][0] is the correct answer, the answers will be shuffled during construction of the object
id is the id and file name of the quiz
getQA returns both the question string and the list of answers at index n
addQA adds both a question and its answers
a question cannot be added without at least one answer
load will load a quiz given its id and return a Quiz object
'''
class Quiz:
    def __init__(self,quizName,questions=[],answers=[[]],id=None,correct=[],noPoints=10,loading=False,time_limit=60):
        #if there are more or less correct answers than questions
        if len(correct)!=len(questions):
            if correct==[]:

                for i in range(len(questions)):
                    correct.append(0)
            else:
                raise exception_maker(ValueError,"number of correct answer index is wrong")
        
        if quizName==None:
            raise exception_maker(ValueError,"quizName can't be None")
        self.quizName=quizName
        if len(questions)!=len(answers):
            raise exception_maker(AttributeError,"questions length must be answers length")
        self.questions=questions
        #self.correct=correct
        self.correct=[]
        ##Loop through answers and get the index of the correct one
        for i in range(len(answers)):
            #print(i)
            tempCor=answers[i][correct[i]]
            #print("tempCorr "+tempCor)
            random.shuffle(answers[i])
            #print("find "+str(find(answers[i],tempCor)))
            self.correct.append(find(answers[i],tempCor))
        self.answers=answers
        self.id=id
        self.points=noPoints
        self.time = time_limit
        #only saves if the not loading flag is set to false
        if (not loading):
            self.save()




    def save(self):
        if self.id!=None:
            #print("AFSJUAIFH JA",self.time)
            myDict={'quizName':self.quizName,'questions':self.questions,'answers':self.answers,'correct':self.correct}
            with open("quiz/templatetags/quizzes/"+str(self.id)+'.json',"w") as outf:
                json.dump(myDict,outf)
            try :
                entry=models.Quizzes.objects.create(id=self.id,points=self.points,time=self.time)
                entry.save()
                return
            except IntegrityError:
                return
        
        #print(models.Quizzes.objects.count()+10)
        #self.id=models.Quizzes.objects.count()+10
        #entry=models.Quizzes.objects.create(id=models.Quizzes.objects.count()+10,points=self.points)
        entry=models.Quizzes.objects.create(points=self.points,time=self.time)
        self.id=entry.pk
        
        #print("imp"+models.Quizzes.get_id(entry))
        entry.save()
        
        #print(self.id)
        myDict={'quizName':self.quizName,'questions':self.questions,'answers':self.answers,'correct':self.correct}
        with open("quiz/templatetags/quizzes/"+str(self.id)+'.json',"w") as outf:
                json.dump(myDict,outf)

    #Getters and setter
    def getId(self):
        return self.id
    
    def getName(self):
         return self.quizName

    def getQuestion(self,n=-1):
        if n==-1:
            return self.questions
        return self.questions[n]

    def getAnswer(self,n=-1):
        if n==-1:
            return self.answers
        return self.answers[n]

    def getCorrect(self,q):
        return self.answers[q][self.correct[q]]
    
    def getTime(self):
        return self.time

    def getQA(self,n=-1):
        if n==-1:
            return (self.questions,self.answers)
        return (self.questions[n],self.answers[n])

    
    def addQA(self,q,a):
        self.questions.append(q)

        tempCor=a[0]

        random.shuffle(a)

        self.correct.append(find(a,tempCor))

        self.answers.append(a)
        self.save()
#Loads and returns a quiz object given its primary key by querying the database
def load(id):
        with open("quiz/templatetags/quizzes/"+str(id)+'.json') as inf:
            myDict=json.load(inf)
        time = models.Quizzes.objects.get(id=id).time
        return (Quiz(myDict['quizName'],myDict['questions'],myDict['answers'],id,myDict['correct'],loading=True,time_limit=time))


#print("A")
#a=Quiz(quizName="One",questions=["It’s acceptable to toss used automotive oil in with regular residential trash.","Unplugging your printer when not in use reduces energy waste and potentially saves about how much annually"],noPoints=666,answers=[["False","True"],["$130","$12","$60"]],loading=False)
#a=load(31)
#print(a.getAnswer())
#print(a.id)


