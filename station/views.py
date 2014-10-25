from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (TemplateView, DetailView, ListView,
                                    CreateView, FormView)
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.utils import timezone
from .models import Activity, Game, System, Log, Puzzle
from .forms import PuzzleForm, CommunicationForm, AdminForm

class MenuView(TemplateView):
    template_name = 'station/menu.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(MenuView, self).get_context_data(*args, **kwargs)
        ctx['game'] = self.kwargs['pk']
        return ctx

class AdminView(TemplateView):
    pass

class StatusView(DetailView):
    model = Game

    def get_context_data(self, *args, **kwargs):
        ctx = super(StatusView, self).get_context_data(*args, **kwargs)

        if self.object.systems.filter(status=System.STATUS_OFFLINE).exists():
            ctx['status'] = 'warning'
        else:
            ctx['status'] = 'good'

        if self.object.state == Game.STATE_LOSE:
            ctx['status'] = 'destroyed'
        elif self.object.state == Game.STATE_WIN:
            ctx['status'] = 'good'
        elif self.object.state == Game.STATE_INITIAL:
            pass # Don't change the state
        elif self.object.state == Game.STATE_OVERLOAD:
            ctx['status'] = 'overload'

        return ctx

class LogView(ListView):
    def get_queryset(self):
        self.game = Game.objects.get(pk=self.kwargs['pk'])
        return Log.objects.filter(game=self.game)

class CommunicationView(TemplateView):
    template_name = 'station/disabled.html'

class RepairView(TemplateView):
    template_name = 'station/disabled.html'

class ActivityView(ListView):
    def get_queryset(self):
        self.game = Game.objects.get(pk=self.kwargs['pk'])
        return Activity.objects.filter(game=self.game)

class ActivityCreateView(CreateView):
    model = Activity
    fields = ('name', 'action', 'detail')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ActivityCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.game = Game.objects.get(pk=self.kwargs['pk'])
        form.instance.game = self.game
        return super(ActivityCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home', kwargs={'pk': self.game.pk})

class PuzzleView(FormView):
    form_class = PuzzleForm
    template_name = 'station/puzzle_form.html'

    def dispatch(self, *args, **kwargs):
        self.object = get_list_or_404(Puzzle, pk=kwargs['pk'])[0]
        return super(PuzzleView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        try:
            return self.request.GET['next']
        except KeyError:
            # Fallback, just in case
            return reverse(self.object.url_name, kwargs={'pk': self.object.game.pk})

    def get_context_data(self, *args, **kwargs):
        ctx = super(PuzzleView, self).get_context_data(*args, **kwargs)
        ctx['puzzle'] = self.object
        return ctx

    def form_valid(self, form):
        if form.cleaned_data['solution'].lower() == self.object.solution.lower():
            self.object.solved = True
            self.object.save()
            return super(PuzzleView, self).form_valid(form)
        else:
            errors = form._errors.setdefault('solution', ErrorList())
            errors.append(u'Incorrect')
            return self.form_invalid(form)

class AdminView(FormView):
    form_class = AdminForm
    template_name = 'station/admin_form.html'

    def get_success_url(self):
        return reverse('admin', kwargs={'pk': self.game.pk})

    def dispatch(self, *args, **kwargs):
        self.game = get_object_or_404(Game, pk=self.kwargs['pk'])
        return super(AdminView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(AdminView, self).get_context_data(*args, **kwargs)
        ctx['game'] = self.game
        return ctx

    def form_valid(self, form):
        if self.game.state == Game.STATE_INITIAL and self.request.POST['mode'] == 'start':
            self.game.state = Game.STATE_OVERLOAD
            self.game.start_time = timezone.now()
            self.game.save()
            activity = Activity()
            activity.game = self.game
            try:
                activity.name = self.request.POST['user']
            except KeyError:
                activity.name = '<unknown>'
            activity.detail = 'Self Destruct'
            activity.action = Activity.ACTION_ENABLED_SYSTEM
            activity.save()
        elif self.game.state == Game.STATE_OVERLOAD and self.request.POST['mode'] == 'stop':
            self.game.state = Game.STATE_INITIAL
            self.game.start_time = None
            self.game.save()
            activity = Activity()
            activity.game = self.game
            try:
                activity.name = self.request.POST['user']
            except KeyError:
                activity.name = '<unknown>'
            activity.detail = 'Self Destruct'
            activity.action = Activity.ACTION_DISABLED_SYSTEM
            activity.save()
        return super(AdminView, self).form_valid(form)
