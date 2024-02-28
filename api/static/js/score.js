// Increase Category Score
function cateIncrease(path){
    let csrftoken = document.querySelector('[name=csrf-token]').content;
    path_part = path.split('/');
    cate_id = path_part[1];
    let url = "/api/category_root/?id=" + cate_id;
    fetch(url).then(response => response.json()).then(data => {
        cate_id = data.root_category_id;
        url = "/api/category/"+ cate_id + "/";
        let patchDataCate = {
            "CategoryScore": 1
        };
        fetch(url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(patchDataCate)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    })
}
// Increase Brand Score
function brandIncrease(brand){
    let csrftoken = document.querySelector('[name=csrf-token]').content;
    url = "/api/brand/" + brand + "/";
    let patchDataBrand = {
        "BrandScore": 1
    };
    fetch(url, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(patchDataBrand)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Success:", data);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}