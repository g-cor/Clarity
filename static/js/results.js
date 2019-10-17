/**
 * results.js
 * 
 * Purpose: This file handles the general behavior of buttons and <a> content
 *    in results.html
 */

// This function returns true if any DOM elements from the classes listed are collapsing
function isCollapsing() {
    var $elements = $('.chest, .mastery, .search-block, .player-content');
    return $elements.hasClass('collapsing');
}

var ready = false;
$('document').ready( function() {
    ready = true;

    /* When the hextech chest or mastery progress button is clicked, hide all content relating
    to hextech chest or mastery progress (Default behavior to open the div targetted by
    the button will still execute - see results.html if necessary) */
    $('.btn-primary').click( function(e) {
        if (ready && !isCollapsing())
            $('.chest , .mastery').collapse('hide');
        else {
            event.preventDefault();
            event.stopPropagation();
        }
    });
    
    /* Change color of text inside the div with mouse is over it or not over it (to help
    indicate that they can be clicked) */
    $('.search-block').not('.title-row').mouseover( function() {
        $(this).css('color', 'dodgerblue');
    });
    $('.search-block').not('.title-row').mouseout( function() {
        $(this).css('color', '#212529');
    });

    /* When a search result is clicked, I want all content except for the result clicked
    to collapse on the page. As that is happening, the default behavior, which is to
    display a specific 'player-content' div, will be executing (see results.html).
    Alternatively, if the result is clicked a second time, we need to show the other
     results and content again. */
    $('.search-block').not('.title-row').click( function(e) {
        if (ready && !isCollapsing()) {
            $('.player-content').collapse('hide');
            $('.chest , .mastery').collapse('hide');
            $('.search-block.collapse.show').not(this).collapse('hide');
            $('.search-block.collapse').collapse('show');
        }
        else {
            event.preventDefault();
            event.stopPropagation();
        }
    });
});