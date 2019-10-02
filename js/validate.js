/**
 * validate.js
 * 
 * Purpose: This file is used with lookup.html to insure that the user inputs
 *   a valid player name. Please note that the XRegExp plugin is used for this
 *   process. Within this project directory, it is stored as the xregexp.js file.
 * 
 * Process: When the search button is clicked, the error message on the page is hidden
 *   from view, and CSS animations are reset. After validating the data, if an error is
 *   found, form submission is halted and error feedback is shown to the user
 */
$("#search_button").click( function(e) {

    // Error message is hidden here and CSS animations are reset
    $("#error_msg").css("visibility", "hidden");
    $("#error_msg").text("Error message goes here");

    $("#summoner_search_box").removeClass("blink_crimson");
    $("#summoner_search_box").removeClass("blink");

    // This is our check for an empty text field and the error returned if true
    if ( $("#summoner_search_box").val() == "" ) {
        event.preventDefault();
        void this.offsetWidth;

        $("#error_msg").text("Missing a summoner name");
        $("#error_msg").css("color", "red");
        $("#error_msg").css("visibility", "visible");

        $("#summoner_search_box").addClass("blink");
    }
    // This is our check for invalid characters in the text field and appropriate
    //   feedback returned if true
    else if ( ! XRegExp("^[_ 0-9\\pL\\.]+$").test( $("#summoner_search_box").val() ) ) {
        event.preventDefault();
        void this.offsetWidth;

        $("#error_msg").text("Invalid character detected");
        $("#error_msg").css("color", "crimson");
        $("#error_msg").css("visibility", "visible");
        
        $("#summoner_search_box").addClass("blink_crimson");
    }
});