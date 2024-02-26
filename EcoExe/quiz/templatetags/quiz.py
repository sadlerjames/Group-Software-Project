import json
import random
import os
cwd = os.getcwd()
print(cwd)
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
    def __init__(self,quizName,questions=[],answers=[[]],id=0):
        if quizName==None:
            raise exception_maker(ValueError,"quizName can't be None")
        self.quizName=quizName
        if len(questions)!=len(answers):
            raise exception_maker(AttributeError,"questions length must be answers length")
        self.questions=questions
        self.correct=[]
        for i in range(len(answers)):
            tempCor=answers[i][0]
            random.shuffle(answers[i])
            self.correct.append(find(answers[i],tempCor))
        self.answers=answers
        self.id=id
        self.save()




    def save(self):
        myDict={'quizName':self.quizName,'questions':self.questions,'answers':self.answers,'correct':self.correct}
        with open("quiz/templatetags/quizzes/"+str(self.id)+'.json',"w") as outf:
            json.dump(myDict,outf)

    def getName(self):
         return self.Name

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
print("LALAAL")
def load(id):
        with open("quiz/templatetags/quizzes/"+str(id)+'.json') as inf:
            myDict=json.load(inf)
        return (Quiz(myDict['quizName'],myDict['questions'],myDict['answers'],id))


#a=Quiz("One",["It’s acceptable to toss used automotive oil in with regular residential trash."],[["False","True"]],1)
#a=load(1)
#print(a.getAnswer())