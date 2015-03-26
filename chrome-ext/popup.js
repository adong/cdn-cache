var CDNCacheFront = {

    init: function() {
        $('#clear-cache').click(CDNCacheFront.clearCache);
    },

    clearCache: function(){
        localStorage.clear();
        $('#message-area').text('Cache Cleared!').css('color', 'green');
    }

};

jQuery(CDNCacheFront.init);