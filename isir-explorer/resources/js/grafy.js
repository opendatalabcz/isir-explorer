
window.pocetNovychIns = function (elemId, jsonData) {
    var insData = JSON.parse(jsonData);
    var arr = [[insData["labels"]["x"], insData["labels"]["y"]]];
    var chartData = insData["data"];
    for(const m in chartData){
        arr.push([m, chartData[m]]);
    }

    var data = new google.visualization.arrayToDataTable(arr);

    var options = {
        legend: { position: "none" },
        annotations: {
            alwaysOutside: true,
            textStyle: {
                fontSize: 14,
                color: '#000',
                auraColor: 'none'
            }
        },
        vAxis: {
            title: insData["labels"]["y"]
        },
        chartArea: {
            width: "90%"
        }
    };

    var chart = new google.visualization.ColumnChart(document.getElementById(elemId));
    chart.draw(data, options);
}


window.typOsoby = function (elemId, jsonData) {

    var insData = JSON.parse(jsonData);
    let arr = [
        ['Typ osoby', 'Počet'],
    ];

    var chartData = insData["data"];
    for(const m in chartData){
        arr.push([m, chartData[m]]);
    }

    var data = google.visualization.arrayToDataTable(arr);

    var options = {

        isStacked: true,
        hAxis: {
            title: insData["labels"]["y"],
            minValue: 0,
            textPosition: 'out'
        },

        chartArea: {width: '70%', height: '60%'},
        legend: {position: 'none', maxLines: 2},
        titlePosition: 'in',
        vAxis: {textPosition: 'out'}
    };

    var chart = new google.visualization.BarChart(document.getElementById(elemId));

    chart.draw(data, options);
}


function rescaleData(elemId, res){
    let histObject = window.histograms[elemId];
    //rescale data from global histObject with given resolution and keep original unmodified
    let result = {
        data: [],
        res: res,
        min: histObject.min,
    };

    let i=0, k=1, val=histObject.min, sum=0;
    while(val < histObject.max){
        let cnt = histObject.data[i];
        if(val <= histObject.min + k*res){
            sum+=cnt;
        }else{
            let diff = val - (histObject.min + k*res);
            let overflow = cnt*(diff/histObject.res);
            sum+=Math.max(0,cnt-overflow);

            result.data.push(sum);
            sum=overflow;
            ++k;
        }
        val += histObject.res;
        ++i;
    }
    if(sum > 0) result.data.push(sum);
    result.max = result.min + result.data.length*res;
    return result;
}

function drawPlot(elemId, res){
    let histObject = window.histograms[elemId];
    let histObj = (res == histObject.res) ? histObject : rescaleData(elemId, res);

    let i=histObj.min, j=0,
        xPoints=[],
        descrData=[],
        selected=[],
        shapes=[],
        anno=[],
        maxVal=0,
        decimal=(Math.log10(histObj.res)<=1) ? 1 : 0;

    while(i < histObj.max){
        let str = i.toFixed(decimal)+"-"+(i+histObj.res).toFixed(decimal);
        descrData.push(str);
        let rangeCenter = i+histObj.res/2;
        xPoints.push(rangeCenter.toFixed(decimal));
        if(histObj.data[j] > maxVal) maxVal=histObj.data[j];
        i += histObj.res;
        ++j;
    }

    if(histObject.marker){
        let index = Math.floor((data.marker - histObj.min) / res);
        selected.push(index);

        shapes.push({
            type: 'line',
            x0: data.marker,
            y0: 0,
            x1: data.marker,
            y1: 1,
            yref: "paper",
            layer: "bellow",
            line: {
                color: 'yellow',
                width: 2,
                dash: "dot"
            }
        });
        anno.push({
            x: data.marker + (histObj.max - histObj.min)/250,
            y: 1,
            showarrow: false,
            text: data.name,
            yref: "paper",
            align: "left",
            xanchor: "left",
            font: {
                color: "yellow"
            }
        });
    }

    let plotData = [{
        x: xPoints,
        y: histObj.data,
        text: descrData,
        type: 'bar',
        selectedpoints: selected,
        selected: {
            marker: {color: "yellow", opacity: 1}
        },
        unselected: {
            marker: {color: "#3366cc", opacity: 1}
        },

    }];

    let layout = {
        xaxis: {type: histObject.xtype || "linear", title: {text: histObject.insData.labels.x, font: {size: 11}}, color:"black", spikemode:"across", spikesnap: "data"},
        yaxis: {type: histObject.ytype || "linear", title: {text: histObject.insData.labels.y, font: {size: 11}}, color:"black", gridcolor:"#ccc", spikemode:"marker", showspikes: false},
        barmode: 'relative',
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 0,
            pad: 4
        },
        paper_bgcolor: "rgba(0, 0, 0, 0)",
        shapes: shapes,
        bargap:0,
        bargroupgap: 0,
        annotations: anno,
    };

    Plotly.newPlot(elemId, plotData, layout, {modeBarButtonsToRemove: ['toggleSpikelines','hoverCompareCartesian','hoverClosestCartesian']});
}

window.histograms = {};

window.histogram = function (elemId, jsonData) {
    var insData = JSON.parse(jsonData);
    let histObject = insData.data;
    histObject.insData = insData;
    window.histograms[elemId] = histObject;
    drawPlot(elemId, histObject.defRes);

    if($("#resRange")){
        $("#resVal").text(histObject.defRes);
        $("#resRange").attr("min", histObject.res)
            .attr("max", Math.min(Math.round((histObject.max-histObject.min)/4),histObject.res*100))
            .attr("step", histObject.res)
            .attr("value", histObject.defRes)
            .on("input", function(){
                $("#resVal").text($(this).val());
                drawPlot(elemId, parseFloat($(this).val()));
            });
    }
}
