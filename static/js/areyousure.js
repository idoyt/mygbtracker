// popup check if user wants to leave
$(function() {
    $('.confirm').click(function() {
        return window.confirm("Redirecting to New Page Are you sure you want to leave the page?");
    });
});
