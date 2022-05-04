from cmath import log
from django.shortcuts import render,redirect

from .forms import EntryForm, TopicForm
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.

def index(request):
    return render(request, 'MainApp/index.html')
@login_required
def topics(request):
    topics = Topic.objects.all()


    context = {'topics':topics} #key is what you use in the html file, value is what you use in the view file

    return render(request,'MainApp/topics.html', context)
@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')

    if topic.owner != request.user:
        raise Http404

    context = {'topic':topic,'entries':entries}

    return render(request,'MainApp/topic.html',context)
@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            new_topic = form.save()

            return redirect('MainApp:topics')
    context = {'form': form}
    return render(request, 'MainApp/new_topic.html',context)
@login_required
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('MainApp:topic',topic_id=topic_id)

    context = {'form': form,'topic':topic}
    return render(request, 'MainApp/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('MainApp:topic',topic_id=topic.id)

    context = {'form': form,'topic':topic, 'entry':entry}
    return render(request, 'MainApp/edit_entry.html',context)