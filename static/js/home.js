$(document).ready(function () {
    $(".navbar-burger").click(function () {
        $(".navbar-burger").toggleClass("is-active");
      	$(".navbar-menu").toggleClass("is-active");
    });

    $(".panel-tabs").click(function() {
    	$(".panel-tabs > a").toggleClass("is-active");
    })
});

