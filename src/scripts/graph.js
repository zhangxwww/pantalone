import * as echarts from "echarts";

function drawAssetChangeLineGraph (domId, data) {
    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: "资产变化"
        },
        tooltip: {
            trigger: "axis"
        },
        legend: {
            data: ["现金", "货币基金", "定期存款"]
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLabel: {
                formatter: function (value) {
                    const date = new Date(value);
                    const year = date.getFullYear();
                    const month = date.getMonth() + 1;
                    return `${year}/${month < 10 ? "0" + month : month}`;
                }
            }
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
                areaStyle: {}
            },
            {
                name: "货币基金",
                type: "line",
                data: data.monetaryFundData,
                stack: "x",
                areaStyle: {}
            },
            {
                name: "定期存款",
                type: "line",
                data: data.fixedDepositData,
                stack: "x",
                areaStyle: {}
            }
        ]
    }
    chart.setOption(option);
    return chart;
}

export { drawAssetChangeLineGraph }