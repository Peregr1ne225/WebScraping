// Edit Modal
function onShow (event) {
    // Get the clicked element and its parent
    let clickedElement = event.relatedTarget;
    let parentElement = clickedElement.parentElement;
    
    // Get the data from the parent element
    let nameText = parentElement.children[4].textContent;
    let priceText = parentElement.children[8].textContent;
    let descriptionText = parentElement.children[6].textContent;            

    // Set data for the modal
    let productId = parentElement.id;
    let productName = nameText.substring(nameText.indexOf(':') + 1).trim();
    let productPrice = priceText.substring(priceText.indexOf(':') + 1).trim();
    let productDescription = descriptionText.substring(descriptionText.indexOf(':') + 1).trim();

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
//Data from response to update the product
function setNewData(data) {
    let productDiv = document.getElementById(data.ProductID);

    productDiv.children[4].textContent = `Product Name : ${data.ProductName}`;
    productDiv.children[7].textContent = `Stock: ${data.Stock}`;
    productDiv.children[8].textContent = `Price: ${data.Price}`;

    productDiv.dataset.price = data.Price;
    productDiv.dataset.score = data.SimilarScore;
    productDiv.dataset.group = data.SimilarGroup;

    let productEdit = productDiv.querySelector('.edit-update p');
    productEdit.textContent = `Last Edited: ${data.DateEdit}`;
    
    if(document.getElementsByClassName('item-group').length > 0)
        changeGroup(data.ProductID, data.SimilarGroup);
}