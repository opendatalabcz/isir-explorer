google.charts.load('current', {
    'packages': ['timeline', 'corechart', 'bar'],
    'language': 'cs',
});

google.charts.setOnLoadCallback(function(){
    drawTimelineChart();
    drawInsTypeChart();
});

const colors = {
    "O": "#127ba3",
    "K": "#ff4d00",
    "R": "#009420",
    "?": "#292929",
};

/* Casova osa rizeni spravce  ------------------------------------------ */



Date.prototype.dmy = function() {
    var m = this.getMonth() + 1;
    var d = this.getDate();

    return d + '. ' + m + '. ' + this.getFullYear();
};

function drawTimelineChart() {
    var container = document.getElementById('spravce-timeline');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();

    dataTable.addColumn({
        type: 'string',
        id: 'INS'
    });
    dataTable.addColumn({
        type: 'string',
        id: 'INS'
    });
    dataTable.addColumn({
        type: 'string',
        id: 'style',
        role: 'style'
    });
    dataTable.addColumn({
        type: 'string',
        role: 'tooltip',
    });
    dataTable.addColumn({
        type: 'date',
        id: 'Zacatek'
    });
    dataTable.addColumn({
        type: 'date',
        id: 'Konec'
    });

    timeline = JSON.parse(timeline);
    let rows = [];

    const typNazvy = {
        "O": "Oddlužení",
        "K": "Konkurz",
        "R": "Reorganizace",
        "?": "Neurčeno",
    };

    function typRizeni(ins) {
        let col = colors[ins.t];
        return '<span style="color:' + col + ';font-weight:bol">' + typNazvy[ins.t] + '</span>';
    }

    function tooltipHtml(ins, zacatek, konec) {
        const now = new Date();
        const diffTime = Math.abs(now - konec);
        const ukonceni = (diffTime < 1000 * 60 * 60 * 24) ? "<em>Současnost</em>" : konec.dmy();
        let title = '<span class="ti-title">' + ins.i + '</span>'
        let vlasnosti = '<dl class="ti-info"><dt>Typ:</dt><dd>' + typRizeni(ins) + '</dd>';
        vlasnosti += '<dt>Zahájení:</dt><dd>' + zacatek.dmy() + '</dd>';
        vlasnosti += '<dt>Ukončení:</dt><dd>' + ukonceni + '</dd>';
        vlasnosti += '</dl>';
        return '<div class="ti-tt">' + title + vlasnosti + '</div>';
    }
    for (const ins of timeline) {
        let zacatek = new Date(ins.s * 1000);
        let konec = new Date(ins.e * 1000);
        rows.push([
            ins.i, "", colors[ins.t], tooltipHtml(ins, zacatek, konec), zacatek, konec,
        ]);
    }

    dataTable.addRows(rows);
    var options = {
        timeline: {
            showRowLabels: false,
            barLabelStyle: {
                fontSize: 3
            }
        },
        tooltip: {
            isHtml: true
        },
    };

    chart.draw(dataTable, options);
}

/* Typy rizeni  ------------------------------------------ */
function _typyRizeniBars(objTypyRizeni, elem, suffix, hAxisTitle){
    let dataTable = [
        ['Forma řízení', 'Oddlužení', 'Konkurz', 'Reorganizace'],
    ];

    if(!elem) return;
    for(const rok in objTypyRizeni){
        let row = [
            rok,
            objTypyRizeni[rok]["O"+suffix] || 0,
            objTypyRizeni[rok]["K"+suffix] || 0,
            objTypyRizeni[rok]["R"+suffix] || 0
        ];
        dataTable.push(row);
    }

    var data = google.visualization.arrayToDataTable(dataTable);

    var options = {

        isStacked: true,
        hAxis: {
            title: hAxisTitle,
            minValue: 0,
            textPosition: 'out'
        },

        series: {
            0:{color:colors["O"]},
            1:{color:colors["K"]},
            2:{color:colors["R"]},
        },

        chartArea: {width: '70%', height: '60%'},
        legend: {position: 'top', maxLines: 2},
        titlePosition: 'in',
        vAxis: {textPosition: 'out'}
    };

    var chart = new google.visualization.BarChart(elem);

    chart.draw(data, options);
}

function drawInsTypeChart(){
    let objTypyRizeni = JSON.parse(typyRizeni);
    let typy_chart = document.getElementById('typy_chart');
    let velikosti_chart = document.getElementById('velikosti_chart');
    let typy_pohl = document.getElementById('typy_pohl');
    let typy_popreno = document.getElementById('typy_popreno');

    _typyRizeniBars(objTypyRizeni, typy_chart, "", 'Počet insolvencí');
    _typyRizeniBars(objTypyRizeni, velikosti_chart, "_vyse", 'Výše (Kč)');
    _typyRizeniBars(objTypyRizeni, typy_pohl, "_pohl", 'Pohledávek');
    _typyRizeniBars(objTypyRizeni, typy_popreno, "_popreno", 'Výše (Kč)');
}
