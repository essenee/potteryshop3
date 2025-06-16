document.addEventListener('DOMContentLoaded', function() {
    const categoryLinks = document.querySelectorAll('.tagcloud .custom-category-link');
    const productContainer = document.querySelector('.ps-products');
    const overlay = document.querySelector('#ps-shop-products-overlay');

    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const categoryId = this.getAttribute('data-category-id');

            // Show loading overlay
            if (overlay) {
                overlay.style.display = 'block';
            }

            // Send AJAX request
            fetch(`/?category_id=${encodeURIComponent(categoryId)}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                // Update product list
                if (productContainer) {
                    productContainer.innerHTML = data;
                }
                // Hide loading overlay
                if (overlay) {
                    overlay.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error fetching products:', error);
                if (overlay) {
                    overlay.style.display = 'none';
                }
                alert('Failed to load products. Please try again.');
            });
        });
    });
});

//Mobile Nav
//document.addEventListener('DOMContentLoaded', function() {
//    const widgetTitles = document.querySelectorAll('.ps-shop-sidebar .widget .ps-widget-title');
//
//    widgetTitles.forEach(title => {
//        title.addEventListener('click', function(e) {
//            e.preventDefault();
//            // Find the parent widget
//            const widget = title.closest('.widget');
//
//            if (widget) {
//                // Toggle active class
//                widget.classList.toggle('active');
//            }
//        });
//    });
//});