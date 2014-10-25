from django.db import models
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField

class Game(models.Model):
    STATE_INITIAL = 0
    STATE_OVERLOAD = 1
    STATE_WIN = 2
    STATE_LOSE = 3

    STATE_CHOICES = (
        (STATE_INITIAL, 'Initial'),
        (STATE_OVERLOAD, 'Overload in progress'),
        (STATE_WIN, 'Overload aborted'),
        (STATE_LOSE, 'Dead'),
    )

    state = models.IntegerField(choices=STATE_CHOICES)
    start_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u'Game {}'.format(self.pk)

class Activity(models.Model):
    class Meta:
        ordering = ('created',)

    ACTION_AUTH = 0
    ACTION_DEAUTH = 1
    ACTION_PERSONAL_LOG = 2
    ACTION_ANNOUNCE = 5
    ACTION_REPAIRED = 6
    ACTION_DISABLED_SYSTEM = 7
    ACTION_ENABLED_SYSTEM = 8
    ACTION_GARBAGE = 9

    ACTION_CHOICES = (
        (ACTION_AUTH, 'Authenticated'),
        (ACTION_DEAUTH, 'Deauthenticated'),
        (ACTION_PERSONAL_LOG, 'Personal Log'),
        (ACTION_ANNOUNCE, 'Announced'),
        (ACTION_REPAIRED, 'Initiated Repair'),
        (ACTION_DISABLED_SYSTEM, 'Disabled System'),
        (ACTION_ENABLED_SYSTEM, 'Enabled System'),
        (ACTION_GARBAGE, u'\u2593' * 12),
    )

    game = models.ForeignKey(Game, related_name='activities')
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    action = models.IntegerField(choices=ACTION_CHOICES)
    detail = models.TextField(blank=True)

    def __unicode__(self):
        return u'{}: {} did {}'.format(self.created, self.name, self.get_action_display())

class System(models.Model):
    class Meta:
        unique_together = (('game', 'name'),)
    STATUS_ONLINE = True
    STATUS_OFFLINE = False
    STATUS_CHOICES = (
        (STATUS_ONLINE, 'online'),
        (STATUS_OFFLINE, 'offline'),
    )
    game = models.ForeignKey(Game, related_name='systems')
    name = models.CharField(max_length=20)
    slug = AutoSlugField(populate_from='name', unique_with=['game'])
    status = models.BooleanField(choices=STATUS_CHOICES, default=STATUS_ONLINE)

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.game)

class Log(models.Model):
    game = models.ForeignKey(Game)
    author = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    contents = models.TextField()

class Puzzle(models.Model):
    game = models.ForeignKey(Game)
    url_name = models.CharField(max_length=255)
    solved = models.BooleanField(default=False)
    hint = models.TextField()
    solution = models.TextField()

    def get_absolute_url(self):
        return reverse('puzzle', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u'{} ({}@{})'.format(
            (self.hint[:22] + '...') if len(self.hint) > 25 else self.hint,
            self.game,
            self.url_name)
