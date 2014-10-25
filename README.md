Destiny
=======

Destiny is a javascript and django based interface for a fictional space
station.

I whipped this together pretty quickly, so forgive the horrible state of the
code.

![](https://i.imgur.com/ndlLYq5.png)

## Setup

Do the normal django database setup, then go to the admin interface and create
a game, some systems, logs, and whatever you think you need for the game. You'll
probably want a couple puzzles as well. The url name parameter has to match the
name of a urlconf line.

## Running the Game

Running the game is pretty simple. Run these two commands to run Destiny
attached to a terminal:

    $ gunicorn --debug --reload  destiny.wsgi --bind 0.0.0.0
    $ celery -A destiny worker -l info -B

Celery is used for time based events, such as announcements and the self
destruct, and gunicorn serves the application.

## QR Codes

The QR codes you need for the game must hold a JSON encoded object, with the
player's name as 'n' and their access level (0-4) as 'l'. For example:

    {"n":"Player Name","l":1}

Levels 0-3 give increasing access to various menu options, while anything
greater than 3 gets to bypass the puzzles. The idea is that the crew of the
station would get levels 0-3, depending on their rank, while the saboteur would
get level 4.

The website I used to generate the codes was: http://www.qrexplore.com/generate/
With the 'Treat as CSV' option enabled. You have to backslash escape commas.

## Compatibility

I've only been able to get this to run in Firefox, and Firefox Browser for
Android. I'm sure it would be pretty easy to get it working in Chrome, but I
haven't had the time yet. It would also be nice to get this working on iOS.

## Future Work

Besides making Destiny more cross-platform, I'd like to finish the repair and
communication screens, use django's users for authentication, make all the
screens show live data, and the list goes on.

## Credits

The voiceovers were provided by some of the members of the recordthis community
on reddit:

	* AvidLebon
	* megajs
	* tattedspyder

Thanks so much guys!

