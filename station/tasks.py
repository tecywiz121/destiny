from threading import Event
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from django.utils import timezone
from datetime import datetime, timedelta
from time import sleep, time
import urlparse, urllib
from os.path import abspath
from random import choice
from .vlc import MediaPlayer, EventType
from .models import Game

LOCK_EXPIRE = 60 * 5

logger = get_task_logger(__name__)

def path2url(path):
    path = abspath(path)
    return urlparse.urljoin('file:', urllib.pathname2url(path))

class TakenError(Exception):
    pass

class TaskLock(object):
    def __init__(self, name):
        self.taken = False
        self.name = name

    @staticmethod
    def take(name):
        if not cache.add(name, 'true', LOCK_EXPIRE):
            raise TakenError()

    def __enter__(self):
        TaskLock.take(self.name)
        self.taken = True

    @staticmethod
    def release(name):
        cache.delete(name)

    def __exit__(self, type, value, traceback):
        if self.taken:
            TaskLock.release(self.name)

SOUND_FMT = 'station/sounds/jaron/{}.flac'

def _c(m, s):
    '''Shortcut for timedelta'''
    return timedelta(minutes=m, seconds=s)

def _p(*args):
    '''Computes a url for a sound file'''
    return [SOUND_FMT.format(x) for x in args]

COUNTDOWN = {
    _c( 0,  1): _p('001'),
    _c( 0,  2): _p('002'),
    _c( 0,  3): _p('003'),
    _c( 0,  4): _p('004'),
    _c( 0,  5): _p('005'),
    _c( 0, 10): _p('010', 'seconds'),
    _c( 0, 20): _p('020', 'seconds'),
    _c( 0, 20): _p('020', 'seconds'),
    _c( 0, 30): _p('030', 'seconds'),
    _c( 2, 00): _p('002', 'minutes'),
    _c(10, 00): _p('010', 'minutes'),
    _c(20, 00): _p('020', 'minutes'),
    _c(30, 00): _p('030', 'minutes'),
    _c(45, 00): _p('045', 'minutes'),
    _c(60, 00): _p('060', 'minutes'),
}

def _play(sound):
    event = Event()
    mp = MediaPlayer(sound)
    em = mp.event_manager()
    em.event_attach(EventType.MediaPlayerEndReached, lambda a: event.set())
    mp.play()
    event.wait()

def _play_countdown(oldest):
    now = timezone.now()
    end_time = oldest.start_time + timedelta(seconds=3600)
    remaining = end_time - now

    if remaining.total_seconds() <= 0:
        oldest.state = Game.STATE_LOSE
        oldest.save()
        return

    minutes = int(remaining.seconds // 60)
    seconds = int(remaining.seconds % 60)

    remaining = timedelta(minutes=minutes, seconds=seconds)

    try:
        sounds = COUNTDOWN[remaining]
    except KeyError:
        return

    logger.error('******** ' + repr(sounds))

    for sound in sounds:
        _play(sound)

def _do_countdown(self):
    while True:
        try:
            with TaskLock('audio-lock'):
                oldest = None
                for game in Game.objects.all():
                    if game.state == Game.STATE_OVERLOAD:
                        if not oldest or game.start_time <= oldest.start_time:
                            oldest = game
                if oldest:
                    _play_countdown(oldest)
        except TakenError:
            sleep(0.1)
            continue
        break

@shared_task(bind=True)
def countdown(self):
    logger.error('Checking countdown')
    try:
        with TaskLock('countdown-lock'):
            _do_countdown(self)
    except TakenError:
        pass

ANNOUNCEMENTS = _p('lookout', 'safety', 'visitors', 'welcome')

@shared_task(bind=True)
def announce(self):
    logger.error('checking announcement')
    try:
        with TaskLock('audio-lock'):
            _play(choice(ANNOUNCEMENTS))
    except TakenError:
        pass
