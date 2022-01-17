from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import AnswerForum, Forum
from django.template.defaultfilters import slugify, title

from forum.forms import FormForum

@login_required(login_url='accounts:login')
def forum(request):

    all_forum = Forum.objects.all()
    all_answer = AnswerForum.objects.all()

    if request.method == 'POST':
        form = FormForum(request.POST)
        
        title = request.POST['title']
        content = request.POST['content']
        curso = request.POST['curso']
        slug = slugify(title)
        grava_forum = Forum(user=request.user, curso=curso, slug=slug, title=title, content=content)
        grava_forum.save()
        form = FormForum()
    else:
        form = FormForum()

    template_name = 'forum.html'
    context = {
        'form': form,
        'forum': all_forum,
        'answer': all_answer
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def edit(request, id):

    forum = get_object_or_404(Forum,id=id)
    form = FormForum()

    context = {
        'forum': forum,
        'form': form
    }

    form.initial['curso'] = forum.curso
    form.initial['title'] = forum.title
    form.initial['content'] = forum.content
  
    template_name = 'forum_edit.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def delete(request, id):

    forum = get_object_or_404(Forum,id=id) 
    forum.delete()
  
    return redirect('forum:index')

@login_required(login_url='accounts:login')
def edit_final(request, id):

    if request.method == 'POST':
    
        curso = request.POST['curso']
        title = request.POST['title']
        content = request.POST['content']
        topico_forum = Forum.objects.filter(id=id)
        topico_forum.update(curso=curso, title=title, content=content)


    return redirect('forum:index')

@login_required(login_url='accounts:login')
def comment(request, id):
    
    all_forum = Forum.objects.all()
    all_answer = AnswerForum.objects.all()


    form = FormForum()

    context = {
        'form': form,
        'is_comment_id': id,
        'forum': all_forum,
        'answer': all_answer
    }

    template_name = 'forum.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def answer(request, id):

    all_forum = Forum.objects.all()
    all_answer = AnswerForum.objects.all()
    
    if request.method == 'POST':
        form = FormForum(request.POST)

        answer = request.POST['answer']

        grava_answer = AnswerForum(user=request.user, id_topico_forum=id, answer=answer)
        grava_answer.save()

        form = FormForum()
    else:
        form = FormForum()

    template_name = 'forum.html'
    context = {
        'form': form,
        'forum': all_forum,
        'answer': all_answer
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def edit_answer(request, id):

    forum_answer = get_object_or_404(AnswerForum,id=id)
    form = FormForum()

    context = {
        'forum_answer': forum_answer,
        'form': form
    }

    form.initial['answer'] = forum_answer.answer
  
    template_name = 'forum_edit_answer.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def delete_answer(request, id):

    forum_answer = get_object_or_404(AnswerForum,id=id) 
    forum_answer.delete()
  
    return redirect('forum:index')

@login_required(login_url='accounts:login')
def edit_final_answer(request, id):

    if request.method == 'POST':
    
        answer = request.POST['answer']
        topico_forum_answer = AnswerForum.objects.filter(id=id)
        topico_forum_answer.update(answer=answer)

    return redirect('forum:index')