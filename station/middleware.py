from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Puzzle

class PuzzleMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            game_pk = view_kwargs['pk']
        except KeyError:
            return None

        if request.GET.get('bypass', 'false') == 'true':
            return None

        try:
            puzzle = Puzzle.objects.filter(game__pk=game_pk,
                                        url_name=request.resolver_match.url_name,
                                        solved=False)[0]
        except IndexError:
            return None

        path = '{}?next={}'.format(puzzle.get_absolute_url(), request.path)
        return HttpResponseRedirect(path)
