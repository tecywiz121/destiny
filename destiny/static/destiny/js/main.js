$(function() {
    'use strict';

    var gCurrentUser = '';
    var gCurrentLevel = 0;
    var gBypass = false;

    var setCurrentLevel = function(user, level) {
        if (level < gCurrentLevel) {
            $('.status a').click();

        }

        if ((gCurrentUser && user !== gCurrentUser) ||
            (level === 0 && gCurrentLevel > 0)) {
            logActivity('deauth');
        }

        if (level > 0 && (gCurrentUser !== user || gCurrentLevel !== level)) {
            gCurrentUser = user;
            $('.current-user').text(user);

            logActivity('auth');
        }

        if (level >= 4) {
            gBypass = true;
            level = 3;
        } else {
            gBypass = false;
        }

        gCurrentLevel = level;
        $('.current-level').text(level);
        $('.side-nav li').addClass('disabled');
        $('.side-nav .unlock > a').text('Unlock Terminal');

        switch (level) {
            case 3:
                $('.side-nav .admin').removeClass('disabled');
            case 2:
                $('.side-nav .comms').removeClass('disabled');
                $('.side-nav .repairs').removeClass('disabled');
            case 1:
                $('.side-nav .logs').removeClass('disabled');
                $('.side-nav .unlock > a').text('Lock Terminal');
            case 0:
            default:
                $('.side-nav .status, .side-nav .unlock')
                    .removeClass('disabled');
        }
    };

    var logActivity = function(action, detail) {
        if (!detail) {
            detail = '';
        }
        switch (action) {
            case 'auth':
                action = 0;
                break;
            case 'deauth':
                action = 1;
                break;
            case 'log':
                action = 2;
                break;
            case 'announce':
                action = 3;
                break;
            case 'repair':
                action = 4;
                break;
            case 'disabled':
                action = 5;
                break;
            case 'enabled':
                action = 6;
                break;
            case 'garbage':
                action = 7;
                break;
        }

        $.post('activity/new/',
            {action: action, name: gCurrentUser, detail: detail});
    };

    var updateEvents = function() {
        // Activate Countdown Clocks
        $('#contents-wrap *[data-start]').each(function() {
            var d = new Date(Date.parse($(this).attr('data-start')));
            d.setSeconds(d.getSeconds() + 3600);
            $(this).countdown({
                until: d
            });
        });

        // Make forms work properly
        $('#contents-wrap form').submit(function(evt) {
            evt.preventDefault();
            var $this = $(this);

            var a = $.post($this.attr('action'),
                $this.serialize() + '&user=' + gCurrentUser);
            a.done(function(data) {
                var content = $(data, '#contents');
                $('#contents-wrap').empty().append(content);
                updateEvents();
            });
        });
    };

    // Prevent accidental navigation
    window.onbeforeunload = function() {
        return true;
    };

    // Prevent disabled links from working
    $('body').on('click', '.disabled a', function() {
        return false;
    });

    // Fullscreen Button
    $('.fullscreen').click(function() {
        if (screenfull.enabled) {
            screenfull.request();
        }
        return false;
    });

    // Hide/show fullscreen button based on state
    $(document).on(screenfull.raw.fullscreenchange, function() {
        if (screenfull.isFullscreen) {
            $('.fullscreen').hide();
        } else {
            $('.fullscreen').show();
        }
    });

    // Authentication Dialog
    $('#auth-modal').modal({ show: false});
    $('#welcome-modal').modal({ show: false});
    $('.auth-toggle').click(function() {
        if (gCurrentLevel > 0) {
            setCurrentLevel('', 0);
        } else {
            $('#auth-modal').modal('show');
        }
        return false;
    });

    // Navigation Hack
    $('body').bind('click', '*[data-href]', function(evt) {
        var $this = $(evt.target),
            href = $this.data('href');

        if (!href) {
            return; // Odd, don't know why this would happen
        }

        if (gBypass) {
            href += '?bypass=true';
        }

        $('#contents-wrap').load(href + ' #contents',
            function(data, textStatus, jqXHR) {
                if (jqXHR.status < 200 || jqXHR.status >= 300) {
                    console.log('load failed: ', textStatus);
                    return;
                }
            updateEvents();
        });
    });

    // Tabs
    $('.nav > li:not(.unlock) > a').click(function() {
        var $this = $(this);
        if ($this.parent().is('.disabled, .active')) {
            return false;
        }
        $this.tab('show');
    });

    // Start the QR code reader
    $('#reader').html5_qrcode(
        function(data) {
            var object;
            try {
                object = JSON.parse(data);
            } catch (e) {
                console.log('Invalid JSON:', e);
                return;
            }

            var name = object.n,
                level = object.l;

            if ('undefined' === name || 'undefined' === level) {
                console.log('Missing data:', data);
                return;
            }

            setCurrentLevel(name, level);

            $('#auth-modal').modal('hide');
            $('#welcome-modal').modal('show');
        },

        function(error) {
            // Ignore read errors
        },

        function(videoError) {
            alert('Could not open stream: ' + videoError);
            if (videoError === 'NO_DEVICES_FOUND') {
                setCurrentLevel(videoError, 3);
            }
        }
    );

    // Click the status tab
    $('.status a').click();
});
