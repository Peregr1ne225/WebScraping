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
    // Change Item Range
    slider.noUiSlider.on('change.one', function (values, handle) {
        let items_div = document.querySelectorAll('div[data-price]');
        items_div.forEach(item_price => {
            let price = Number(item_price.dataset.price);
            if(price >= values[0] && price <= values[1]) {
                item_price.classList.remove('d-none');
                item_price.classList.add('d-flex');
            }
            else {
                item_price.classList.remove('d-flex');
                item_price.classList.add('d-none');
            }
            addDNoneToItemGroup();
        });
    });
    // Group hidden
    function addDNoneToItemGroup() {
        let itemGroups = document.querySelectorAll(".item-group");
        itemGroups.forEach(itemGroup => {
            let children = itemGroup.children;
            let allHaveDNone = true;
            for (let i = 0; i < children.length; i++) {
                if (!children[i].classList.contains("d-none")) {
                    allHaveDNone = false;
                    break;
                }
            }
            if (allHaveDNone) {
                itemGroup.classList.add("d-none");
            } else {
                itemGroup.classList.remove("d-none");
            }
        });
    }