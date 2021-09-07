$(document).ready(function () {
    $(".navbar-burger").click(function () {
        $(".navbar-burger").toggleClass("is-active");
      	$(".navbar-menu").toggleClass("is-active");
    });

    $(".panel-tabs > a").click(function() {
    	$(".panel-tabs > a").removeClass("is-active");
    	$(this).addClass("is-active");
    })
});

