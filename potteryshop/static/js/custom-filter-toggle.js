(function($) {
    if (typeof $ === 'undefined') {
        console.error('ShopFilterToggle: jQuery is not loaded');
        return;
    }

    $.extend({
        shopFilterToggle: {
            init: function() {
                this.$filterLink = $('a[href="#filter"], .ps-shop-filter-btn-wrap a');
                this.$sidebar = $('#ps-shop-sidebar');
                this.$sidebarInner = $('.ps-shop-sidebar-inner');
                this.$row = this.$sidebarInner.find('.ps-row');
                this.$widgetList = $('#ps-shop-widgets-ul');
                this.isSliding = false;
                this.slideSpeed = 200;
                this.$widgetList.find('li').each(function() {
                    console.log('ShopFilterToggle: Initial widget item display:', $(this).attr('id') || 'no-id', $(this).css('display'));
                });

                this.bindEvents();
            },

            bindEvents: function() {
                var self = this;

                $(document).on('click', 'a[href="#filter"], .ps-shop-filter-btn-wrap a', function(e) {
                    e.preventDefault();
                    console.log('ShopFilterToggle: Filter link clicked', $(this).attr('href'));

                    if (!self.isSliding) {
                        self.isSliding = true;

                        self.$sidebar.slideToggle(self.slideSpeed, function() {
                        self.isSliding = false;
                        self.$filterLink.parent().toggleClass('active');
                        self.ensureContentVisibility(self.$sidebar.is(':visible'));
                        console.log('ShopFilterToggle: Sidebar display after toggle:', self.$sidebar.css('display'));
                        console.log('ShopFilterToggle: Widget list display after toggle:', self.$widgetList.css('display'));
                    });
                    }
                });
            },

            ensureContentVisibility: function(isVisible) {
                console.log('ShopFilterToggle: Ensuring content visibility, isVisible:', isVisible);
                if (isVisible) {
                    this.$sidebar.css({
                        'display': 'block',
                        'visibility': 'visible',
                        'opacity': '1',
                        'max-height': 'none',
                        'overflow': 'visible',
                        'height': 'auto'
                    });
                    this.$sidebarInner.css({
                        'display': 'block',
                        'visibility': 'visible',
                        'opacity': '1',
                        'max-height': 'none',
                        'overflow': 'visible',
                        'height': 'auto'
                    });
                    this.$row.css({
                        'display': 'block',
                        'visibility': 'visible',
                        'opacity': '1',
                        'max-height': 'none',
                        'overflow': 'visible',
                        'height': 'auto'
                    });
                    this.$widgetList.css({
                        'display': 'block',
                        'visibility': 'visible',
                        'opacity': '1',
                        'max-height': 'none',
                        'overflow': 'visible',
                        'height': 'auto'
                    });
                    this.$widgetList.find('li').css({
                        'display': 'block',
                        'visibility': 'visible',
                        'opacity': '1',
                        'max-height': 'none',
                        'overflow': 'visible',
                        'height': 'auto'
                    });
                }
            }
        }
    });

    $(document).ready(function() {
        console.log('ShopFilterToggle: Document ready');
        $.shopFilterToggle.init();
    });
})(typeof jQuery !== 'undefined' ? jQuery : null);