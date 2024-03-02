function sortName(order) {
    return function() {
        let items = Array.from(document.querySelectorAll('.item-product'));
        items.sort(function(a, b) {
            let nameA = a.querySelector('.p-name').textContent;
            let nameB = b.querySelector('.p-name').textContent;
            return order === 'a' ? nameA.localeCompare(nameB) : nameB.localeCompare(nameA);
        });
        sortProduct(items);
    };
}

function sortPrice(order) {
    return function() {
        let items = Array.from(document.querySelectorAll('.item-product'));
        items.sort(function(a, b) {
            let priceA = parseFloat(a.getAttribute('data-price'));
            let priceB = parseFloat(b.getAttribute('data-price'));
            return order === 'min' ? priceA - priceB : priceB - priceA;
        });
        sortProduct(items);
    };
}

function sortDate(order) {
    return function() {
        let items = Array.from(document.querySelectorAll('.item-product'));
        items.sort(function(a, b) {
            let dateA = new Date(a.getAttribute('data-created'));
            let dateB = new Date(b.getAttribute('data-created'));
            return order === 'old' ? dateA - dateB : dateB - dateA;
        });
        sortProduct(items);
    };
}

function sortProduct(items) {
    let productDisplay = document.getElementById('product-display');
    items.forEach(item => {
        // Remove the 'fade' class from the item
        item.classList.remove('fade');
        productDisplay.appendChild(item);
    });
    let itemGroups = document.querySelectorAll('.item-group');
    if (itemGroups.length > 0) {
        itemGroups.forEach(item => {
            item.parentNode.removeChild(item);
        })
    }
}
