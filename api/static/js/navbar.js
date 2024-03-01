// Add Top Brand from API

window.addEventListener("load", function(){
    try{
        fetch("/api/brand_top/")
        .then(response => response.json())
        .then(data => {
            brandtoNav(data.results, document.getElementById("topbrand"));
        })
    } catch (error) {
        console.log(error);
    }
})
// Add Brand to Navbar
function brandtoNav(data, parentElement) {
    let currentUrl = new URL(window.location.href);
    currentUrl = currentUrl.origin + currentUrl.pathname;
    for (let i = 0; i < 8; i++) {
        let brandLink = document.createElement("a");
        brandLink.className = "nav-link";
        brandLink.href = currentUrl + `?brand=${data[i].BrandID}`;
        brandLink.textContent = data[i].BrandName;
        parentElement.appendChild(brandLink);
    }
}
// Add Top Category from API
window.addEventListener("load", function(){
    try{
        fetch("/api/category_top/")
        .then(response => response.json())
        .then(data => {
            catetoNav(data.results, document.getElementById("topcate"));
        })
    } catch (error) {
        console.log(error);
    }
})
// Add Category to Navbar
function catetoNav(data, parentElement) {
    let currentUrl = new URL(window.location.href);
    for (let i = 4; i >= 0; i--) {
        let cateLink = document.createElement("a");
        cateLink.className = "nav-link align-middle";
        cateLink.href = currentUrl.origin + "/" + data[i].CategoryID + "/";
        cateLink.textContent = data[i].CategoryName;
        parentElement.appendChild(cateLink);
    }
}

$(document).ready(function() {
    // check if the token cookie exists
    var token = document.cookie.split('; ').find(row => row.startsWith('token'));

    if (token) {
        // if the token exists, create the admin dropdown
        var adminDropdown = `
        <div class="dropdown admin-page">
            <a id="dropdownAdminButton" class="dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false" aria-label="Toggle Admin">Admin</a>
            <ul id="admin-dropdown" class="dropdown-menu dropdown-menu-end" aria-labelledby="dropdownAdminButton">
                <li><a class="dropdown-item" href="/dashboard">Dashboard</a></li>
                <li><a class="dropdown-item" href="/admin">Admin Page</a></li>
                <li><a id="logoutButton" class="dropdown-item" href="#">Log Out</a></li>
            </ul>
        </div>`;
        $('.navbar .container-fluid').append(adminDropdown);
    } else {
        // if the token doesn't exist, create the login button
        var loginButton = `
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#loginModal">
            Login
        </button>`;
        $('.navbar .container-fluid').append(loginButton);
    }
});
