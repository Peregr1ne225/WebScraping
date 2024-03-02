//Set Value for Price Slider
let minPrice = 0;
let maxPrice = 0;
    
function sliderSetPrice(price) {
    if(minPrice == 0 || minPrice > price || maxPrice == 0 || maxPrice < price) {
        if(minPrice == 0 || minPrice > price) minPrice = price;
        if(maxPrice == 0 || maxPrice < price) maxPrice = price;
    
        minPrice = parseFloat(minPrice);
        maxPrice = parseFloat(maxPrice);
        if (minPrice == maxPrice) {
            // If they are, adjust maxPrice slightly
            maxPrice += 0.01;
        }
        slider.noUiSlider.updateOptions({
            start: [minPrice, maxPrice],
            range: {
                'min': minPrice,
                'max': maxPrice
            }
        });
    }
}

    // Price Slider
    let slider = document.getElementById('price-slider');
    noUiSlider.create(slider, {
        start: [0, 100],
        connect: true,
        range: {
            'min': 0,
            'max': 100
        },
        step: 1
    });
    // Change Slider Value
    slider.noUiSlider.on('update', function (values, handle) {
        if (handle) {
            document.getElementById('max-value').innerHTML = values[handle];
        } else {
            document.getElementById('min-value').innerHTML = values[handle];
        }
        
    });
    slider.noUiSlider.on('change.one', function (values, handle) {
        let items_div = document.querySelectorAll('div[data-price]');
        items_div.forEach(item_price => {
            let price = Number(item_price.dataset.price);
            let parent_group = item_price.closest('.item-group'); // Find the nearest .item-group ancestor
            let corresponding_tab = document.querySelector(`#${item_price.id}-tab`); // Find the corresponding tab button
            if(price >= values[0] && price <= values[1]) {
                item_price.classList.remove('d-none');
                if (corresponding_tab) corresponding_tab.classList.remove('d-none'); // Show the tab button
            }
            else {
                item_price.classList.add('d-none');
                if (corresponding_tab) corresponding_tab.classList.add('d-none'); // Hide the tab button
            }
            // If parent_group exists, check if all child divs with data-price in this group are hidden
            if (parent_group) {
                let allHidden = Array.from(parent_group.querySelectorAll('div[data-price]')).every(div => div.classList.contains('d-none'));
                if (allHidden) {
                    // If all are hidden, hide the entire group
                    parent_group.classList.add('d-none');
                } else {
                    // If not all are hidden, show the group
                    parent_group.classList.remove('d-none');
                }
            }
        });
    });