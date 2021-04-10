google.charts.load('current', {
    'packages': ['corechart', 'bar'],
    'language': 'cs',
});

google.charts.setOnLoadCallback(function(){
    drawInsTypeChart();
});

const colors = {
    "O": "#127ba3",
    "K": "#ff4d00",
    "R": "#009420",
    "?": "#292929",
};


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

    _typyRizeniBars(objTypyRizeni, typy_chart, "", 'Počet insolvencí');
    _typyRizeniBars(objTypyRizeni, velikosti_chart, "_vyse", 'Výše (Kč)');
}
