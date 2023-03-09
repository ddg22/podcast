'use strict';

function dates() {
    document.querySelectorAll('.Date').forEach(date => {
        let single_date = dayjs(date.innerText);
        date.innerText = single_date.format('DD-MM-YYYY');
    })
    return;
}


// Main
dates();