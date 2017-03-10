(function ($) {
    "use strict"; // Start of use strict

    // Display selected date and bind date field
    $(document).bind('click', '.list-group button', function (event) {
        var $element = $(this);
        var hour = $element.attr("data-src");
        var day = $element.parent().attr("data-src");
        var full_date = day + ' ' + hour;

        $('.list-group button').removeClass('active');
        $element.addClass('active');
        $('#date').text(full_date);
        $('#id_date_refill').val(full_date);
    });

    // Display hours on day selection
    $(document).on('click', '.day', function (event) {
        var $element = $(this);
        var day = ($element.children().text().length == 1) ? '0' + $element.children().text() : $element.children().text();
        var $old_element = $('.show');
        var $new_element = $('.' + day);

        $('.day').removeClass('active');
        $element.addClass('active');
        $old_element.removeClass("show");
        $old_element.addClass("hide");
        $new_element.removeClass("hide");
        $new_element.addClass("show");
    });

    var date = new Date();
    $("#calendar").load('/calendar/' + date.getFullYear() + '/' + date.getMonth());

    $(document).on('click', '.load', function (event) {
        $('#calendar').load($(this).attr('href'));
        event.preventDefault();
    });

})(jQuery); // End of use strict
