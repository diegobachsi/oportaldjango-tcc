from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import AnswerForum, Forum
from django.template.defaultfilters import slugify, title
from django.core.paginator import Paginator

from forum.forms import FormForum

@login_required(login_url='accounts:login')
def forum_index(request):

    all_forum = Forum.objects.all()

    if request.method == 'POST':
        form = FormForum(request.POST)
        
        title = request.POST['title']
        content = request.POST['content']
        curso = request.POST['curso']
        slug = slugify(title)
        grava_forum = Forum(user=request.user, curso=curso, slug=slug, title=title, content=content, qtd_answer=0)
        grava_forum.save()
        form = FormForum()
    else:
        form = FormForum()

    template_name = 'forum_index.html'

    count = all_forum.count()
    paginator = Paginator(all_forum, 5)
    page = request.GET.get('page')
    all_forum = paginator.get_page(page)

    context = {
        'form': form,
        'forum': all_forum,
        'count': count
    }
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def forum(request, slug):

    forum = Forum.objects.filter(slug=slug)
    id_forum = Forum.objects.filter(slug=slug).values('id')
    all_answer = AnswerForum.objects.filter(id_topico_forum=id_forum[0]['id'])

    print(all_answer)

    if request.method == 'POST':
        form = FormForum(request.POST)
        
        title = request.POST['title']
        content = request.POST['content']
        curso = request.POST['curso']
        grava_forum = Forum(user=request.user, curso=curso, slug=slug, title=title, content=content, qtd_answer=0)
        grava_forum.save()
        form = FormForum()
    else:
        form = FormForum()

    template_name = 'forum.html'
    context = {
        'form': form,
        'forum': forum,
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
        slug = slugify(title)
        topico_forum = Forum.objects.filter(id=id)
        topico_forum.update(curso=curso, title=title, content=content, slug=slug)


    return redirect('forum:index')

@login_required(login_url='accounts:login')
def comment(request, id):
    
    forum = Forum.objects.filter(id=id)
    all_answer = AnswerForum.objects.filter(id_topico_forum=id)

    form = FormForum()

    context = {
        'form': form,
        'is_comment_id': id,
        'forum': forum,
        'answer': all_answer
    }

    template_name = 'forum.html'
    return render(request, template_name, context)

@login_required(login_url='accounts:login')
def answer(request, id):

    forum = Forum.objects.filter(id=id)
    all_answer = AnswerForum.objects.filter(id_topico_forum=id)
    
    if request.method == 'POST':
        form = FormForum(request.POST)

        answer = request.POST['answer']

        grava_answer = AnswerForum(user=request.user, id_topico_forum=id, answer=answer)
        grava_answer.save()

        qtd_answer = forum.values('qtd_answer')[0]['qtd_answer']
        new_qtd_answer = qtd_answer + 1

        forum.update(qtd_answer=new_qtd_answer)

        form = FormForum()
    else:
        form = FormForum()

    template_name = 'forum.html'
    context = {
        'form': form,
        'forum': forum,
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

    id_topico_forum = AnswerForum.objects.filter(id=id).values('id_topico_forum')[0]['id_topico_forum']

    forum = Forum.objects.filter(id=id_topico_forum)
    qtd_answer = forum.values('qtd_answer')[0]['qtd_answer']
    new_qtd_answer = qtd_answer - 1

    forum.update(qtd_answer=new_qtd_answer)

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