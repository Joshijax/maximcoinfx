(function ($) {
    "use strict";
         $('.copy').on('click',function(){
            myFunction();
        });
        function myFunction() {
            var copyText = document.getElementById("copyed");
            copyText.select();
            document.execCommand("Copy");
        }
        $('.owl-carousel').owlCarousel({
        loop: true,
        dots: true,
        nav: true,
        navText: [
            "<i class='pe-7s-angle-left'></i>",
            "<i class='pe-7s-angle-right'></i>"
        ],
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: true
            },
            480: {
                items: 2,
                nav: true
            },
            768: {
                items: 2,
                nav: true
            },
            1000: {
                items: 3,
                nav: true,
                loop: false,
                margin: 20
            },
            1200: {
                items: 4,
                nav: true,
                loop: false,
                margin: 20
            }
        }
    })
    
    }(jQuery));