from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice, Student
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import StudentForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages

def index(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'myapp1/index.html', context)

@login_required
def detail(request, question_id):
    #question = get_object_or_404(Question, pk=question_id)
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())

    compteur = 5
    messages.add_message(request, messages.INFO, 'Bonjour visiteur !')
    messages.debug(request, 'debug: %s requêtes SQL ont été exécutées.' % compteur)
    messages.info(request, 'info: Rebonjour !')
    messages.success(request, 'success: Votre article a bien été mis à jour.')
    messages.warning(request, 'warning: Votre compte expire dans 3 jours.')
    messages.error(request, 'error: Cette image n\'existe plus.')

    return render(request, 'myapp1/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'myapp1/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapp1:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'myapp1/results.html', {'question': question})

class qlist(generic.ListView):
    model = Question
    paginate_by = 2

class qview(generic.DetailView):
    model = Question

from .forms import NameForm




def studview(request):
    #Avec la fonction render pas besoin de loader et de Httpresponse
    studquery = Student.objects.order_by('name')
    context = {'studlist':studquery}
    return render(request, 'myapp1/student.html', context)

class StudentList(generic.ListView):
    model = Student
    paginate_by = 20

    def get_context_data(self, **kwargs):
        nbvisits=self.request.session.get('num_visits', 0)
        self.request.session['num_visits'] = nbvisits+1

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['num_visits'] = nbvisits
        return context


class StudentDetail(LoginRequiredMixin, generic.DetailView):
    model = Student


class StudentCreate(LoginRequiredMixin, CreateView):
    model = Student
    #fields = ['name', 'email', 'color', 'date']
    #success_url = reverse_lazy('myapp1:student_list')
    #fields = '__all__'
    form_class = StudentForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(StudentCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        CreatorU = User.objects.get(username=self.request.user)
        initial={'date':proposed_renewal_date, 'creator':CreatorU}
        #initial={'date':proposed_renewal_date}
        return initial


class StudentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('myapp1.can_update',)
    model = Student
    fields = ['name', 'email', 'color', 'date']
    #success_url = reverse_lazy('myapp1:student_detail', args=(pk,))

class StudentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('myapp1.can_delete',)
    model = Student
    success_url = reverse_lazy('myapp1:student_list')
