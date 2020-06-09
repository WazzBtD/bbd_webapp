$(document).ready(function() {
    $(".alert-dismissible").fadeTo(10000, 5000).slideUp(500, function(){
        $(".alert-dismissible").alert('close');
    });
});