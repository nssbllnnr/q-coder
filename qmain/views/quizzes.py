from django.shortcuts import render, redirect
from django.http import HttpResponse

from ..forms import CreatePollForm
from ..models import Poll


def home(request, course_id):
    polls = Poll.objects.all()

    context = {
        'polls' : polls,
        'course_id' : course_id
    }
    return render(request, 'poll/home.html', context)

def create(request, course_id):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('quizzes')
    else:
        form = CreatePollForm()
    context = {
        'form' : form,
        'course_id' : course_id
    }
    return render(request, 'poll/create.html', context)


def vote(request, course_id, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('quizzes-results', course_id, poll.id)

    context = {
        'poll' : poll,
        'course_id' : course_id
    }
    return render(request, 'poll/vote.html', context)

def results(request,course_id, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll,
        'course_id' : course_id
    }
    return render(request, 'poll/results.html', context)