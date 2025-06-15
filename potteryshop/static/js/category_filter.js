document.addEventListener('DOMContentLoaded', function () {
    const tagCloudLinks = document.querySelectorAll('#product_tag_cloud-2 .tagcloud a.custom-category-link');
    const productList = document.querySelector('#ps-shop-products ul.ps-products');
    const loader = document.querySelector('#ps-shop-products-overlay');

    // Function to fetch and render products
    function fetchProducts(url) {
        // Show loader
        loader.style.display = 'block';

        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest' // Indicate AJAX request
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text(); // Expect HTML response
        })
        .then(html => {
            // Create a temporary container to parse the HTML
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newProductList = doc.querySelector('ul.ps-products');

            if (newProductList) {
                // Replace the existing product list with the new one
                productList.innerHTML = newProductList.innerHTML;
            } else {
                productList.innerHTML = '<li>No products found.</li>';
            }

            // Hide loader
            loader.style.display = 'none';
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            productList.innerHTML = '<li>Error loading products.</li>';
            loader.style.display = 'none';
        });
    }

    // Add click event listeners to category links
    tagCloudLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default navigation

            // Remove active class from all links
            tagCloudLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');

            const url = this.getAttribute('href');
            fetchProducts(url);
        });
    });
});