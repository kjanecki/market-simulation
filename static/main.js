function addItemsToTable(items) {
    console.log(items);
    if (items) {
        var oldTable = document.getElementById("table-body");
        var table = document.createElement('tbody');
        table.id = 'table-body';

        for (var i in items) {
            var row = table.insertRow(0);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            cell1.innerHTML = '<strong class="uid" onClick = "highlightUser(' + i + ');" >' + i + '</strong>';
            cell2.innerHTML = items[i];
        }
        oldTable.parentNode.replaceChild(table, oldTable);
    }
}

function refresh() {
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

function highlightUser(id) {
    fetch('http://localhost:8521/color?id=' + id, {
        mode: 'cors'
    });
}