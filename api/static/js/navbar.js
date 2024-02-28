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