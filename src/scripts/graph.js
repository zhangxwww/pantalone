// import * as echarts from "echarts";
import * as echarts from "echarts/core";
import { LineChart, PieChart, ScatterChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    ToolboxComponent,
    DataZoomComponent,
    MarkPointComponent,
    MarkLineComponent,
    MarkAreaComponent
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import { LabelLayout, UniversalTransition } from "echarts/features";

echarts.use([
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    ToolboxComponent,
    DataZoomComponent,
    MarkPointComponent,
    MarkLineComponent,
    MarkAreaComponent,
    LineChart,
    PieChart,
    ScatterChart,
    CanvasRenderer,
    LabelLayout,
    UniversalTransition
]);

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

function drawLiquidityReturnPositoinScatterGraph (domId, data) {
    const chart = echarts.init(document.getElementById(domId));
    let amount = [];
    amount.push(...data.amount);
    const maxAmount = Math.max(...amount);
    const minAmount = Math.min(...amount);
    const diffAmount = maxAmount - minAmount;
    amount = amount.map((value) => {
        return (value - minAmount) / diffAmount * 25 + 25;
    });
    const option = {
        title: {
            text: "流动性-收益-规模",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        xAxis: {
            type: "log",
            logBase: 10,
            name: "流动性",
        },
        yAxis: {
            name: "收益",
        },
        tooltip: {
            formatter: function (params) {
                return `
                <table>
                    <tbody>
                        <tr>
                            <td align="left">流动性</td>
                            <td align="right"><b>${params.data[0]}</b></td>
                        </tr>
                        <tr>
                            <td align="left">收益</td>
                            <td align="right"><b>${params.data[1].toFixed(2)}</b></td>
                        </tr>
                        <tr>
                            <td align="left">规模</td>
                            <td align="right"><b>${data.amount[params.dataIndex].toFixed(2)}</b></td>
                        </tr>
                    </tbody>
                </table>
                `
            }
        },
        series: [
            {
                type: 'scatter',
                data: data.data,
                symbolSize: (value, params) => {
                    return amount[params.dataIndex];
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 5,
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

function drawAverageReturnLineGraph (domId, data) {
    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: "平均收益",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
        },
        yAxis: {
            type: "value",
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(0) + "%";
                }
            }
        },
        series: [
            {
                name: "平均收益",
                type: "line",
                data: data.data,
                smooth: true
            }
        ],
        tooltip: {
            trigger: "axis",
            textStyle: {
                align: "left"
            },
            formatter: params => {
                let name = params[0].name;
                for (let i = 0; i < params.length; i++) {
                    name += `<br>${params[i].marker}${params[i].seriesName}: ${params[i].value.toFixed(4) * 100}%`;
                }
                return name;
            }
        },
    }
    chart.setOption(option);
    return chart;
}

export {
    drawAssetChangeLineGraph,
    drawResidualMaturityPieGraph,
    drawExpectedReturnPieGraph,
    drawLiquidityReturnPositoinScatterGraph,
    drawAverageReturnLineGraph
}