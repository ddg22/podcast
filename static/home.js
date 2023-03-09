'use strict';


function create_category(cat_name) {
    return `<li>
    <button type="button" class="ButtonLink">${cat_name}</button>
    </li>`
}


function create_hr() {
    return `<hr class="my-3">`
}


// Visualizzo le categorie
function all_categories() {
    const categories = [];
    document.querySelectorAll('.Category').forEach(category => {
        let cat = category.innerText;
        if (!categories.includes(cat)) {
            categories.push(cat);
        }
        categories.sort();
    })
    const list = document.querySelector('aside > ul');
    for (let i = 0; i < categories.length; i++) {
        let cat = create_category(categories[i]);
        list.insertAdjacentHTML('beforeend', cat);
    }

}


// Scorro i post per categoria
function category_trigger() {
    // Trigger per gestire i filtri categoria
    document.querySelectorAll('aside > ul > li > button').forEach(link => {
        link.addEventListener('click', event => {
            event.preventDefault();
            let filter = event.target.innerText;
            let cnt = 0;
            document.querySelectorAll('.Podcast').forEach(podcast => {
                let category = podcast.querySelector('.Category');
                let cat = category.innerText.trim();
                if (filter === 'Tutti' || cat === filter) {
                    podcast.classList.remove('hide');
                    cnt += 1;
                }
                else if (cat !== filter) {
                    podcast.classList.add('hide');
                }
            })
            delete_hrs();
            document.querySelectorAll('article').forEach(article => {
                if (!article.classList.contains('hide') && cnt > 1) {
                    article.insertAdjacentHTML("afterend", create_hr());
                    cnt -= 1;
                }
            })
        })
    
    })
    return;
}


function put_hrs() {
    document.querySelectorAll('article').forEach(article => {
        if (article.nextElementSibling != undefined) {
            article.insertAdjacentHTML("afterend", create_hr());
        }
    })
    return;
}


function delete_hrs() {
    document.querySelectorAll('hr').forEach(hr => {
        hr.remove();
    })
    return;
}


// Main
all_categories();
category_trigger();
put_hrs();