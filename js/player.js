
player = {};

(function (player) {

    player = player || {};
    player.songid = '47506486';
    player.song = {liked: false};
    player.playing = false;
    player.debugMode = true;
    const DEFAULT_ARTWORK = '';

    player.log = function (str) {
        if (player.debugMode) {
            console.log(str);
        }
    };

    player.play = function () {
        $('#audio-player')[0].play();
        player.playing = true;
    };

    player.pause = function () {
        $('#audio-player')[0].pause();
        player.playing = false;
    };

    player.init = function () {

        SC.initialize({
            client_id: '27bcac07db1cde6ee2ff5f3ad8d79969'
        });

        $('.next-btn').on('click', player.newSong);
        $('.play-btn').on('click', player.play);
        $('.heart').on('click', client.likeSong);
        $('.pause-btn').on('click',player.pause);

        player.newSong();

    };

    player.newSong = function () {

        client.getSong(function (sobj) {

            player.log('getsong');
            player.songid = sobj.song_id;
            player.song = sobj;
            if (sobj.song_image.length) {
                player.artwork = sobj.song_image;
            } else if (sobj.user_image.length) {
                player.artwork = sobj.user_image;
            } else {
                player.artwork = DEFAULT_ARTWORK;
            }

            SC.get("/tracks/" + player.songid).then(function (sound) {
                player.log('playing: ' + sobj.user_name + ' - ' + sobj.song_title);
                $('.title').text(sobj.song_title);
                $('.artist').text(sobj.user_name);
                $('.artwork').attr('src', player.artwork);
                $('.artlink').attr('href', sobj.song_url);

                var url = sound.stream_url + "?client_id=27bcac07db1cde6ee2ff5f3ad8d79969";
                $("#audio-player").attr("src", url);
                player.song.url = url;
                player.song.liked = false;
                player.play();
            });

        });
    };

})(player);

$(player.init);
