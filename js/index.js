
UI = {};

(function (UI) {

    UI = UI || {};

    UI.bindings = function () {

        $('.next-btn').on('click', function () {
            $('.heart').removeClass('red');
            $('.heart').addClass('clickable');
            $('.play-btn').addClass('hidden');
            $('.pause-btn').removeClass('hidden');
        });

        $('.play-btn').on('click', function () {
            $('.play-btn').addClass('hidden');
            $('.pause-btn').removeClass('hidden');
        });

        $('.pause-btn').on('click', function () {
            $('.play-btn').removeClass('hidden');
            $('.pause-btn').addClass('hidden');
        });

        $('.heart').on('click', function () {
            if (!player.song.liked) {
                $('.heart').addClass('red');
                $('.heart').removeClass('clickable');
            }
        });

    };

    UI.init = function () {
        UI.bindings();
    };

})(UI);

$(UI.init);