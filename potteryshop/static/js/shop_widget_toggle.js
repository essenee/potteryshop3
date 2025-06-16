document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('shop_widget_toggle.js loaded');
        const widgetTitles = document.querySelectorAll('#ps-shop-sidebar .widget .ps-widget-title');
        console.log('Found widget titles:', widgetTitles.length);

        if (widgetTitles.length === 0) {
            console.warn('No .ps-widget-title elements found');
        }

        widgetTitles.forEach(title => {
            title.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Widget title clicked:', title);

                // Find parent widget and tagcloud
                const widget = title.closest('.widget');
                const tagcloudContainer = widget ? widget.querySelector('.ps-shop-widget-col:nth-child(2)') : null;
                const tagcloud = tagcloudContainer ? tagcloudContainer.querySelector('.tagcloud') : null;

                if (widget && tagcloudContainer && tagcloud) {
                    // Toggle active class
                    widget.classList.toggle('active');
                    tagcloud.classList.toggle('active');
                    const isActive = widget.classList.contains('active');
                    console.log('Widget:', widget);
                    console.log('Tagcloud container:', tagcloudContainer);
                    console.log('Tagcloud:', tagcloud);
                    console.log('Widget active:', isActive);
                    console.log('Tagcloud container display:', getComputedStyle(tagcloudContainer).display);
                    console.log('Tagcloud display:', getComputedStyle(tagcloud).display);
                    console.log('Icon content:', getComputedStyle(title, '::after').content);
                    console.log('Sidebar display:', getComputedStyle(document.querySelector('#ps-shop-sidebar')).display);

                    // Update data-expanded
                    title.dataset.expanded = isActive ? 'true' : 'false';
                    console.log('Data-expanded:', title.dataset.expanded);
                } else {
                    console.log('Elements not found:', { widget, tagcloudContainer, tagcloud });
                }
            });
        });
    } catch (error) {
        console.error('Error in shop_widget_toggle.js:', error);
    }
});