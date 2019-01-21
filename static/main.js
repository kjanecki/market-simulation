'use strict';

var currentlyChosenUserID;

const toggleList = (id) => {
    const element = document.getElementById('shopping-list-' + id);
    if (element.classList.contains('visible-list')) {
        element.classList.remove('visible-list');
    } else {
        element.classList.add('visible-list');
    }
}

const createShoppingList = (list, id) => {
    const button = '<button class="btn btn-outline-dark btn-sm my-2" onclick="toggleList(' + id + ')">Show list</button>'
    var shoppingList = '<ul class="list-group list-group-flush mt-2 hidden-list" id="shopping-list-' + id + '">';
    for (var i = 0; i < list.length; ++i) {
        shoppingList += '<li class="list-group-item">' + list[i] + '</li>';
    }
    return button + shoppingList + '</ul>';
}

const addItemsToTable = (items) => {
    if (items) {
        const oldTable = document.getElementById("table-body");
        const table = document.createElement('tbody');
        table.id = 'table-body';

        for (var id in items) {
            const shoppingList = items[id];
            if (shoppingList) {
                const row = table.insertRow(0);
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);
                row.id = id;
                cell1.width = '10%';
                cell2.width = '90%';
                cell1.innerHTML = '<button class="btn btn-outline-dark btn-lg uid my-1" onClick = "highlightUser(' + id + ');" >' + id + '</button>';
                cell2.innerHTML = createShoppingList(shoppingList, id);
                cell2.classList.add('text-center');
            }
        }
        oldTable.parentNode.replaceChild(table, oldTable);
    }
}

const refresh = () => {
    fetch('http://localhost:8521/users', {
        mode: 'cors'
    }).then((res) => {
        return res.json();
    }).then(items => {
        addItemsToTable(items);
    }).catch(err => {
        console.error(err);
    });
}

const highlightUser = (id) => {
    if (id && id !== currentlyChosenUserID) {
        fetch('http://localhost:8521/color?id=' + id, {
            mode: 'cors'
        });
        currentlyChosenUserID = currentlyChosenUserID || id;
        document.getElementById(currentlyChosenUserID).classList.remove('highlight-user');
        currentlyChosenUserID = id;
        document.getElementById(currentlyChosenUserID).classList.add('highlight-user');
    }
}