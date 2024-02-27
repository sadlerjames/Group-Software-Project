from django.shortcuts import render
from quiz.templatetags.quiz import Quiz, load
# Create your views here.


def quizzes(request):
    context = {}
    quiz = load(1)
    context['id'] = quiz.id
    context['questions'] = quiz.getQuestion()
    context['total_questions'] = range(len(quiz.getQuestion()))

    options = [
        [],
        [],
        [],
        []
    ]
    for answer_set in quiz.getAnswer():
        for i in range(0, 4):
            try:
                options[i].append(answer_set[i])
            except:
                options[i].append("EMPTY ANSWER")

    context['answer0'] = options[0]
    context['answer1'] = options[1]
    context['answer2'] = options[2]
    context['answer3'] = options[3]

    correct = []
    for i in range(0, len(quiz.getQuestion())):
        correct.append(quiz.getCorrect(i))

    context['correct'] = correct
    return render(request, 'quizzes.html', context)
