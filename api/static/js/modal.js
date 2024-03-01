// Edit Modal
function onShow (event) {
// Get the clicked element and its parent
    let clickedElement = event.relatedTarget;
    let parentElement = clickedElement.closest('.item-product');
    // Get the data from the parent element
    let productName = parentElement.querySelector('.p-name').textContent;
    let productPrice = parentElement.querySelector('.p-price').textContent;
    let productDescription = parentElement.querySelector('.p-desc').textContent;
    // Get the product id
    let productId = parentElement.id;
    // Get the modal elements
    let modalTitle = document.querySelector('#editModal .modal-title')
    let modalBodyId = document.querySelector('#editModal .modal-body #productId')
    let modalBodyName = document.querySelector('#editModal .modal-body #productName')
    let modalBodyPrice = document.querySelector('#editModal .modal-body #productPrice')
    let modalBodyDescription = document.querySelector('#editModal .modal-body #productDescription')
    // Set the data in the modal
    modalTitle.textContent = "Edit Product: " + productId;
    modalBodyId.value = productId;
    modalBodyName.value = productName;
    modalBodyPrice.value = productPrice;
    modalBodyDescription.value = productDescription;
}

// Switching Modals
let isSwitchingModals = false;
let editBtn = document.querySelector('#editModal');
editBtn.addEventListener('show.bs.modal', onShow);
// Hide edit modal for confirm modal then reassigned edit modal
editBtn.addEventListener('hidden.bs.modal', function(event) {
    //check if go edit
    if (isSwitchingModals) {
        isSwitchingModals = false;
        return;
    }
    editBtn.removeEventListener('show.bs.modal', onShow)
    let form = editBtn.querySelector('form')
    form.reset();
    editBtn.addEventListener('show.bs.modal', onShow);
});
// Confirm Modal
let conBtn = document.querySelector('#confirmModal');
conBtn.addEventListener('show.bs.modal', function(event) {
    isSwitchingModals = true; // Set the flag to true
    editBtn.removeEventListener('show.bs.modal', onShow);
    let productId = document.querySelector('#productId').value;
    let productName = document.querySelector('#productName').value;
    let productPrice = document.querySelector('#productPrice').value;
    let productStock = document.querySelector('#productStock').value;
    if (productStock === "") {
        productStock = "&lt;Not Change&gt;";
    }
    
    let productDescription = document.querySelector('#productDescription').value;
    let modalBody = document.querySelector('#confirmModal .modal-body');
    modalBody.innerHTML = `
        <p class="text-break"><strong>Product ID:</strong> ${productId}</p>
        <p class="text-break"><strong>Product Name:</strong> ${productName}</p>
        <p class="text-break"><strong>Price:</strong> ${productPrice}</p>
        <p class="text-break"><strong>Stock:</strong> ${productStock}</p>
        <p class="text-break"><strong>Description:</strong> ${productDescription}</p>
    `;
});
// Hide confirm modal reassigned edit modal
conBtn.addEventListener('hidden.bs.modal', function(event) {
    isSwitchingModals = false;
    editBtn.addEventListener('show.bs.modal', onShow);
});
// Enable Modal input
let modalInput = document.querySelectorAll('.modal-body input[type="text"], .modal-body select, .modal-body textarea');
modalInput.forEach(input => {
    input.style.color = 'gray';
    input.addEventListener('click', function() {
        this.style.color = 'black';  // Use 'this' to refer to the clicked element
    });
});
// Submit Edit Form
document.getElementById('submitEditForm').addEventListener('click', function() {
    document.getElementById("loadingScreen").style.display = "block";
    let modalForm = document.querySelector('#editModal form');
    let csrftoken = document.querySelector('[name=csrf-token]').content;
    let formSend = new FormData(modalForm);
    let productId = formSend.get('ProductID');
    let object = {};
    formSend.forEach((value, key) => {object[key] = value});
    let json = JSON.stringify(object);
    let url = `/api/product/${productId}/`;
    //modalForm.submit();
    fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: json
    })
    .then(response => {
        responseHeader(response.status, response.statusText);
        console.log(response);
        return response.json()
    })
    .then(data => {
        console.log(data);
        setNewData(data);
        responseModal(data);
    })
    .catch((error) => {
        console.error(error);
    });
});
// Modal Response Header
function responseHeader(status, text) {
    let modalTitle = document.querySelector('#responseModal .modal-title');
    modalTitle.textContent = `Status ${status}: ${text}`;
}
// Modal Response Body
function responseModal(data) {
    let myModal = new bootstrap.Modal(document.getElementById('responseModal'));
    let modalBody = document.querySelector('#responseModal .modal-body');
    let jsonString = JSON.stringify(data, null, 2);
    modalBody.textContent = jsonString;
    myModal.show();
    document.getElementById("loadingScreen").style.display = "none";
}

let compareNow = document.getElementById(`compare-now`);
compareNow.addEventListener('click', function() {
    let compareItems = document.querySelectorAll('.compare-bar .compare-items .compare-item');
    if(compareItems.length < 2) {
        alert('You need at least 2 items to compare');
        return;
    }
    let modal = new bootstrap.Modal(document.getElementById('compareModal'));
    // Open the modal
    modal.show();
});

let compareModal = document.getElementById('compareModal');
compareModal.addEventListener('show.bs.modal', function() {
    let compareItems = document.querySelectorAll('.compare-bar .compare-items .compare-item');
    let compareModalBody = compareModal.querySelector('.modal-body .card-group');
    compareModalBody.innerHTML = '';
    compareItems.forEach(item => {
        let full = item.id;
        let productId = full.split('-')[1];
        let url = `/api/product/${productId}/`;
        fetch(url)
        .then(response => response.json())
        .then(data => {
            let product = compareProduct(data);
            compareModalBody.appendChild(product);
        });
    });
});
function compareProduct(data){
    let compareCard = document.createElement('div');
    compareCard.className = 'card compare-part';
    compareCard.innerHTML = `
        <img src="https://img.advice.co.th/images_nas/pic_product4/A0147250/A0147250_1.jpg" class="card-img-top" alt="...">
        <div class="card-body">
            <h5 class="card-title"> <strong>Product Name :</strong>${data.ProductName}</h5>
            <div class="d-flex border-bottom my-2">
                <p class="card-text fw-bold me-1 mb-1">Brand: </p>
                <p class="card-text mb-1">${data.BrandName}</p>
            </div>
            <div class="border-bottom my-2">
                <p class="card-text fw-bold mb-1 align-self-center">Description:</p>
                <p class="card-text">${data.Description}</p>    
            </div>
            <div class="d-flex border-bottom my-2">
                <p class="card-text fw-bold me-1 mb-1">Stock: </p>
                <p class="card-text mb-1">${data.Stock}</p>
            </div>
            <div class="d-flex border-bottom my-2">
                <p class="card-text fw-bold me-1 mb-1">Price: </p>
                <p class="card-text mb-1">${data.Price}</p>
            </div>
            <div class="my-2">
                <div class="d-flex">
                    <p class="fw-bold me-1 mb-1">Retail:</p>
                    <p class="card-text me-1 mb-1">${data.RetailName}</p>
                </div>
                <a role="button" href="${data.URL}" class="btn btn-primary">More Details</a>
            </div>
        </div>
        <div class="card-footer">
            <small class="m-0">Last Edited: ${data.DateEdit}</small>
        </div>`
    return compareCard;
}