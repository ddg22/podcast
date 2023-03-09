'use strict';


function create_hr() {
    return `<hr class="my-3">`
}


function put_hrs() {
    document.querySelectorAll('article').forEach(article => {
        if (article.nextElementSibling != undefined) {
            article.insertAdjacentHTML("afterend", create_hr());
        }
    })
    return;
}


// Main
put_hrs();
