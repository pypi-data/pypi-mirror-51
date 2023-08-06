(function() {

    var BLOCK_MARKER = "has-iframe";

    function checkIframe(block){
        if(block.find('iframe').length) {
            block.addClass(BLOCK_MARKER);
        }
    }

    $(function() {
        $.each($(".sl-block"), function(i, block) { checkIframe($(block)); });
    });

    $(document).on("blockReplaced", function(event, block) {
        checkIframe(block.element);
    });



})();
