'use strict';


function see() {
    const episodes = document.querySelector('#EpisodeList');
    if (!episodes.firstElementChild) {
        episodes.classList.add('hide');
    }
    return;
}


function create_hr() {
    return `<hr class="mx-auto">`
}


function delete_hrs() {
    document.querySelectorAll('hr').forEach(hr => {
        hr.remove();
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


function search() {
    let input = document.querySelector('#Search');
    input.addEventListener('input', event => {

        // Attraverso filtri precedenti potrei aver reso invisibile il contenitore degli episodi, allora come prima cosa lo faccio comparire
        const episodes = document.querySelector('#EpisodeList');
        episodes.classList.remove('hide'); 

        let str = (event.target.value.trim()).toLowerCase();
        let cnt = 0;
        document.querySelectorAll('article').forEach(article => {
            let title = (article.querySelector('h4').innerText.trim()).toLowerCase();
            let description = (article.querySelector('.Description').innerText.trim()).toLowerCase();
            if (title.includes(str) || description.includes(str) || str.length === 0) {
                article.classList.remove('hide');
                cnt += 1;
            }
            else {
                article.classList.add('hide');
            }
        })
        delete_hrs();

        if (cnt === 0) {
            episodes.classList.add('hide');
        }

        document.querySelectorAll('article').forEach(article => {
            if (!article.classList.contains('hide') && cnt > 1) {
                article.insertAdjacentHTML("afterend", create_hr());
                cnt -= 1;
            }
        })
    })
    return;
}


// Main
put_hrs();
search();
see();