'use strict';

var data = {};
var currentlyChosenUserID;
var isAutoRefreshOn = false;

const toggleAutoRefresh = () => {
    isAutoRefreshOn = !isAutoRefreshOn;
}

const toggleList = (id) => {
    const element = document.getElementById('shopping-list-' + id);
    if (element.classList.contains('visible-list')) {
        element.classList.remove('visible-list');
    } else {
        element.classList.add('visible-list');
    }
}

const createShoppingListItems = (list) => {
    var shoppingListItems = '';
    if (list) {
        for (var i = 0; i < list.length; ++i) {
            shoppingListItems += '<li class="list-group-item">' + list[i] + '</li>';
        }
    }
    return shoppingListItems;
}

const addItemsToTable = (items) => {
    if (items) {
        const oldTable = document.getElementById("table-body");
        const table = document.createElement('tbody');
        table.id = 'table-body';

        for (var id in items) {
            const shoppingList = items[id];
            if (shoppingList) {
                const button = '<button class="btn btn-outline-dark btn-sm my-2" onclick="toggleList(' + id + ')">Show list</button>';
                const shoppingListHTML = '<ul class="list-group list-group-flush mt-2 hidden-list" id="shopping-list-' + id + '">' + createShoppingListItems(shoppingList) + '</ul>';
                const row = table.insertRow(0);
                const cell1 = row.insertCell(0);
                const cell2 = row.insertCell(1);
                row.id = id;
                cell1.width = '10%';
                cell1.innerHTML = '<button class="btn btn-outline-dark btn-lg uid my-1" onClick = "highlightUser(' + id + ');" >' + id + '</button>';
                cell2.innerHTML = button + shoppingListHTML;
                cell2.classList.add('text-center');
            }
        }
        oldTable.parentNode.replaceChild(table, oldTable);
    }
}

const refresh = (callback) => {
    fetch('http://localhost:8521/users', {
        mode: 'cors'
    }).then(res => res.json()).then(items => {
        addItemsToTable(items);
        if (callback) {
            callback(items);
        };
    }).catch(err => {
        console.error(err);
    });
}

const setChosenUsersShoppingList = (items, id) => {
    document.getElementById('chosen-user-shopping-list').innerHTML = createShoppingListItems(items[id]);
};

const highlightUser = (id, forcedHighlight = false) => {
    if ((id && id !== currentlyChosenUserID) || (forcedHighlight && id)) {
        if (!forcedHighlight) {
            fetch('http://localhost:8521/color?id=' + id, {
                mode: 'cors'
            });
        }
        document.getElementById(currentlyChosenUserID).classList.remove('highlight-user');
        currentlyChosenUserID = id;
        document.getElementById(currentlyChosenUserID).classList.add('highlight-user');
        document.getElementById('chosen-user-id').innerText = currentlyChosenUserID;
    }
}

const setAgentsMapData = (callback) => {
    fetch('http://localhost:8521/agent_counts', {
        mode: 'cors'
    }).then(res => res.json()).then(items => {
        console.log(items);
        Plotly.plot(document.getElementById('agents-map-plot'), [{
            x: [1, 2, 3, 4, 5],
            y: [1, 2, 4, 8, 16]
        }]);
    });
}

const autoRefresh = (forcedRefresh = false) => {
    if (isAutoRefreshOn || forcedRefresh) {
        setAgentsMapData();
        refresh((items) => {
            setChosenUsersShoppingList(items, currentlyChosenUserID);
            highlightUser(currentlyChosenUserID, true);
        })
    }
}

setInterval(autoRefresh, 3000);