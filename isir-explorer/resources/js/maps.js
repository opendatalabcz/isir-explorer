function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    if (uri.match(re)) {
      return uri.replace(re, '$1' + key + "=" + value + '$2');
    }
    else {
      return uri + separator + key + "=" + value;
    }
}

$("table").tablesorter({
    theme : "bootstrap",
    widthFixed: true,
    widgets : ["columns"],
    sortList: [[1,1]]
});

$('select.date-changer').on('change', function() {
    let optionSelected = $("option:selected", this);
    let rok = optionSelected.data("rok");
    let mesic = optionSelected.data("mesic");
    let url = location.href;
    url = updateQueryStringParameter(url, "rok", rok);
    url = updateQueryStringParameter(url, "mesic", mesic);
    location.href = url;
});


mapData = JSON.parse(mapData);
var map = L.map('map').setView([49.8, 15.5], 7);
map.touchZoom.disable();
map.doubleClickZoom.disable();
map.scrollWheelZoom.disable();
map.boxZoom.disable();
map.keyboard.disable();
map.dragging.disable();
var values = Object.values(mapData);
var minMax = [Math.min(...values), Math.max(...values)];

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token='+mapboxToken, {
    maxZoom: 18,
    attribution: 'Mapová data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
        'Mapový podklad © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/light-v9',
    tileSize: 512,
    zoomOffset: -1
}).addTo(map);

function getColor(val, minMax) {
    let gradient = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026'];
    if(typeof mapInvert !== "undefined" && mapInvert)
        gradient.reverse();
    let kus = (minMax[1] - minMax[0]) / (gradient.length+1);
    let color =  gradient[Math.floor((val-minMax[0]) / kus)];
    if(!color) color = gradient[gradient.length-1];
    return color;
}

function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7,
        fillColor: getColor(feature.properties.val, minMax),
    };
}

$(document).ready(function(){
    $.getJSON( "/api/mapy/kraje", function( data ) {

        let hodnotyKraje = mapData;
        for(let ft of data["features"]){
            let kodKraje = ft["properties"]["ref"];
            let hodnotaProKraj = hodnotyKraje[kodKraje] ? hodnotyKraje[kodKraje] : 0;
            if(!hodnotaProKraj) minMax[0] = 0;
            ft["properties"]["val"] = hodnotaProKraj;
        }

        var info = L.control();

        info.onAdd = function (map) {
            this._div = L.DomUtil.create('div', 'info');
            this.update();
            return this._div;
        };

        info.update = function (props) {
            this._div.innerHTML = (props ?
                '<b>' + props.name + '</b><br>' + infobox_metric + ': ' + props.val
                : 'Umístěte kurzor na kraj');
        };

        info.addTo(map);

        function highlightFeature(e) {
            var layer = e.target;

            layer.setStyle({
                weight: 5,
                color: '#666',
                dashArray: '',
                fillOpacity: 0.7
            });

            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                layer.bringToFront();
            }

            info.update(layer.feature.properties);
        }
        function resetHighlight(e) {
            geojson.resetStyle(e.target);
            info.update();
        }

        function zoomToFeature(e) {
            map.fitBounds(e.target.getBounds());
        }

        function onEachFeature(feature, layer) {
            layer.on({
                mouseover: highlightFeature,
                mouseout: resetHighlight,
                click: zoomToFeature
            });
        }

        let geojson = L.geoJson(data, {
            style: style,
            onEachFeature: onEachFeature
        }).addTo(map);
    });
});
