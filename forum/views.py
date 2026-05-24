from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, TemplateView

from forum.forms import ForumForm, RispostaForm
from forum.models import Forum, Risposta
from user_manage.decorator import  client_required
from user_manage.models import Cliente, User, Owner


class ThreadList(ListView):
    model = Forum
    template_name = 'forum/lista_thread.html'
    context_object_name = 'lista_thread'


class RispostaList(DetailView):
    model = Risposta
    template_name = "forum/discussione.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Forum, pk=self.kwargs.get('pk'))


@method_decorator([login_required,client_required],name='dispatch')
class ThreadCreate(CreateView):
    model = Forum
    form_class = ForumForm
    template_name = 'forum/crea_thread.html'
    success_url = reverse_lazy('forum:thread-list')

    def form_valid(self, form):
        form.instance.user = Cliente.objects.get(user__username=self.request.user.username)
        return super(ThreadCreate,self).form_valid(form)



@method_decorator([login_required],name='dispatch')
class AddComment(CreateView):
    form_class= RispostaForm
    initial = {'key':'value'}
    template_name = 'forum/crea_risposta.html'

    def post(self, request,pk,*args, **kwargs):
        if request.user.is_client == True:
            user = Cliente.objects.get(user__username=request.user.username)
        elif request.user.is_owner == True:
            user = Owner.objects.get(user__username=request.user.username)
        object = Forum.objects.get(id=pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.titolo = object
            comment.save()
            return redirect('forum:discussione', pk=object.pk)

        return render(request, self.template_name, {'form': form})



# @login_required()
# def add_comment(request, pk):
#     if request.user.is_client ==True:
#                 user = Cliente.objects.get(user__username=request.user.username)
#     elif request.user.is_owner ==True:
#                 user= Owner.objects.get(user__username=request.user.username)
#     object =Forum.objects.get(id=pk)
#     if request.method == "POST":
#         form = RispostaForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = user
#             comment.titolo = object
#             comment.save()
#             return redirect('forum:discussione', pk=object.pk)
#     else:
#         form = RispostaForm()
#     return render(request, 'forum/crea_risposta.html', {'form': form})
#
