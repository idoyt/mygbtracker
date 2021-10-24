// popup check if user wants to leave
$(function() {
    $('.confirm').click(function() {
        return window.confirm("Redirecting to new page. Are you sure you want to leave the page?");
    });
});
