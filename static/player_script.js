const if_tapped = {
    0: 'Coral',
    1: 'red',
    2: 'blue',
    3: 'black'
}

function getColorPlayer(tapped, color) {
    if (tapped) {
        return if_tapped[color];
    } else {
        return 'white';
    }
}

function getColorLeader(tapped, color) {
    var if_not_tapped = {
        0: 'Beige',
        1: 'PaleVioletRed',
        2: 'SkyBlue',
        3: 'Gray'
    };

    if (tapped) {
        return if_tapped[color];
    } else {
        return if_not_tapped[color];
    }
}

$.get({
    url: 'state',
    cache: false
}).then(state => {
    var body = document.getElementsByTagName('body')[0];
    var tbl = document.createElement('table');
    tbl.style.width = '500px';
    tbl.style.height = '500px';
    tbl.setAttribute('border', '1');
    var tbdy = document.createElement('tbody');

    for (var i = 0; i < 5; i++) {
        var tr = document.createElement('tr');
        for (var j = 0; j < 5; j++) {
            var td = document.createElement('td');

            data = state[i][j];

            td.appendChild(document.createTextNode(data['word']));

            var color = getColorPlayer(data['tapped'], data['color']);
            td.style.backgroundColor = color;
            td.onclick = (function makeOnClick(word, i, j) {
                return () => {
                    if (confirm('Click `' + word + '`?')) {
                        $.get('click/' + i + '/' + j);
                    }
                }
            })(data['word'], i, j);

            tr.appendChild(td)
        }
        tbdy.appendChild(tr);
    }
    tbl.appendChild(tbdy);
    body.appendChild(tbl)

});
