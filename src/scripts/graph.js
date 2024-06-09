import * as echarts from "echarts";

function drawAssetChangeLineGraph (domId, data) {
    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: "资产变化",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        tooltip: {
            trigger: "axis",
            textStyle: {
                align: "left"
            },
        },
        legend: {
            data: ["现金", "货币基金", "定期存款"],
            // top: "10%",
            x: "center",
            y: "bottom"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
        },
        yAxis: {
            type: "value"
        },
        series: [
            {
                name: "现金",
                type: "line",
                data: data.cashData,
                stack: "x",
                areaStyle: {},
                smooth: true
            },
            {
                name: "货币基金",
                type: "line",
                data: data.monetaryFundData,
                stack: "x",
                areaStyle: {},
                smooth: true
            },
            {
                name: "定期存款",
                type: "line",
                data: data.fixedDepositData,
                stack: "x",
                areaStyle: {},
                smooth: true
            }
        ]
    }
    chart.setOption(option);
    return chart;
}


function drawPieGraph (domId, data, title) {
    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: title,
            x: "center",
            y: "top",
            textAlign: "center"
        },
        tooltip: {
            formatter: '{c} ({d}%)'
        },
        series: [
            {
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                data: data,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    },
                },
            }
        ]
    };
    chart.setOption(option);
    return chart;
}


function drawResidualMaturityPieGraph (domId, data) {
    return drawPieGraph(domId, data, "剩余期限");
}

function drawExpectedReturnPieGraph (domId, data) {
    return drawPieGraph(domId, data, "预期收益");
}

export {
    drawAssetChangeLineGraph,
    drawResidualMaturityPieGraph,
    drawExpectedReturnPieGraph
}