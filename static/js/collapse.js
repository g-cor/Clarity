/**
 * collapse.js
 * 
 * Purpose: This file handles the behavior of the buttons that appear
 *    when rendering summoner.html.
 * 
 * Process: The "btn-primary" class buttons will cause all collapsable
 *    sections of the page to be hidden. But this behavior does not
 *    stop the button from executing it's assigned task of displaying
 *    some section of the page, so it creates a neat ability to
 *    bounce back and forth between page sections without creating
 *    excess clutter.
 */

$('.btn-primary').click( function(e) {
    $('.collapse').collapse('hide');
});