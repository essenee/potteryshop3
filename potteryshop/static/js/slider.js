(function($) {
        $(document).ready(function() {
            $('.slider-hero').slick({
                dots: true,
                infinite: true,
                cssEase: 'linear',
                swipe: false,
                arrows: true,
                prevArrow: '<a class="slick-prev"><i class="ps-font ps-font-angle-left"></i></a>',
                nextArrow: '<a class="slick-next"><i class="ps-font ps-font-angle-right"></i></a>',
                useTransform: false

            });
        });

    })( jQuery );