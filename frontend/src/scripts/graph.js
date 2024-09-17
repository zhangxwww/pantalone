import * as echarts from "echarts/core";
import { LineChart, PieChart, ScatterChart, BarChart } from "echarts/charts";
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

import { timeFormat } from "@/scripts/formatter";

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
    BarChart,
    CanvasRenderer,
    LabelLayout,
    UniversalTransition
]);

function drawAssetChangeLineGraph (domId, data) {
    console.log(data);
    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: "资产总额",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        tooltip: {
            trigger: "axis",
            textStyle: {
                align: "left"
            },
            formatter: params => {
                let name = `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${params[0].name}</b></td>
                        </tr>
                `;
                let sum = 0;
                for (let i = 0; i < params.length; i++) {
                    name += `<tr>
                        <td align="left">${params[i].marker}${params[i].seriesName}：</td>
                        <td align="right"><b>${params[i].value.toFixed(2)}</b></td>
                    </tr>`;
                    sum += params[i].value;
                }
                name += `<tr>
                    <td align="left"><b>总计：</b></td>
                    <td align="right"><b>${sum.toFixed(2)}</b></td>
                `
                name += "</tbody></table>";
                return name;
            }
        },
        legend: {
            data: ["现金", "货币基金", "定期存款", "基金"],
            x: "center",
            y: "bottom"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLabel: {
                interval: index => { return index % 2 == 1 }
            },
        },
        yAxis: {
            type: "value",
            name: "资产规模",
            position: "left",
            boundaryGap: false
        },
        series: [
            {
                name: "现金",
                type: "line",
                data: data.cashData,
                stack: "x",
                areaStyle: {},
                smooth: true,
            },
            {
                name: "货币基金",
                type: "line",
                data: data.monetaryFundData,
                stack: "x",
                areaStyle: {},
                smooth: true,
            },
            {
                name: "定期存款",
                type: "line",
                data: data.fixedDepositData,
                stack: "x",
                areaStyle: {},
                smooth: true,
            },
            {
                name: "基金",
                type: "line",
                data: data.fundData,
                stack: "x",
                areaStyle: {},
                smooth: true,
            },
        ]
    }
    chart.setOption(option);
    return chart;
}

function drawAssetDeltaChangeBarGraph (domId, data) {
    console.log(data);
    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: "资产变动",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        tooltip: {
            trigger: "axis",
            textStyle: {
                align: "left"
            },
            formatter: params => {
                let name = `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${params[0].name}</b></td>
                        </tr>
                `;
                for (let i = 0; i < params.length; i++) {
                    name += `<tr>
                        <td align="left">${params[i].marker}${params[i].seriesName}：</td>
                        <td align="right"><b>${params[i].value.toFixed(2)}</b></td>
                    </tr>`;
                }
                name += "</tbody></table>";
                return name;
            }
        },
        legend: {
            data: ["现金", "货币基金", "定期存款", "基金", "总资产"],
            x: "center",
            y: "bottom"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLine: {
                onZero: true
            },
            axisLabel: {
                interval: index => { return index % 2 == 1 }
            },
        },
        yAxis: {
            type: "value",
            name: "资产变动",
            position: "left",
            boundaryGap: false
        },
        series: [
            {
                name: "现金",
                type: "bar",
                data: data.cashDeltaData,
                barGap: '10%',
                barCategoryGap: '60%'
            },
            {
                name: "货币基金",
                type: "bar",
                data: data.monetaryFundDeltaData,
            },
            {
                name: "定期存款",
                type: "bar",
                data: data.fixedDepositDeltaData,
            },
            {
                name: "基金",
                type: "bar",
                data: data.fundDeltaData,
            },
            {
                name: "总资产",
                type: "bar",
                data: data.totalDeltaData
            }
        ]
    }
    chart.setOption(option);
    return chart;
}

function drawPieGraph (domId, data, title) {
    console.log(data);
    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: title,
            x: "center",
            y: "top",
            textAlign: "center"
        },
        tooltip: {
            formatter: function (params) {
                return `
                <table>
                    <tbody>
                        <tr>
                            <td align="left">规模：</td>
                            <td align="right"><b>${params.value.toFixed(2)}</b></td>
                        </tr>
                        <tr>
                            <td align="left">占比：</td>
                            <td align="right"><b>${params.percent.toFixed(2)}%</b></td>
                        </tr>
                    </tbody>
                </table>
                `
            }
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

function drawLiquidityReturnPositionScatterGraph (domId, data) {
    console.log(data);
    const chart = echarts.init(document.getElementById(domId));
    let amount = [];
    if (data.amount.length === 1) {
        amount.push(25);
    } else {
        amount.push(...data.amount);
        const maxAmount = Math.max(...amount);
        const minAmount = Math.min(...amount);
        const diffAmount = maxAmount - minAmount;
        amount = amount.map((value) => {
            return (value - minAmount) / diffAmount * 25 + 25;
        });
    }
    console.log(amount);
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
            type: "value",
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(1) + "%";
                }
            }
        },
        tooltip: {
            formatter: function (params) {
                return `
                <table>
                    <tbody>
                        <tr>
                            <td align="left">流动性：</td>
                            <td align="right"><b>${params.data[0]}</b></td>
                        </tr>
                        <tr>
                            <td align="left">收益：</td>
                            <td align="right"><b>${(params.data[1] * 100).toFixed(2)}%</b></td>
                        </tr>
                        <tr>
                            <td align="left">规模：</td>
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
    console.log(data);
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
            axisLabel: {
                interval: index => { return index % 2 == 1 }
            },
        },
        yAxis: {
            type: "value",
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(1) + "%";
                }
            }
        },
        legend: {
            data: ["持有收益", "最新收益", "1年期国债收益率"],
            x: "center",
            y: "bottom"
        },
        series: [
            {
                name: "持有收益",
                type: "line",
                data: data.data.holding,
                smooth: true
            },
            {
                name: "最新收益",
                type: "line",
                data: data.data.latest,
                smooth: true
            },
            {
                name: "1年期国债利率",
                type: "line",
                data: data.yields,
                smooth: true
            }
        ],
        tooltip: {
            trigger: "axis",
            textStyle: {
                align: "left"
            },
            formatter: params => {
                let name = `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${params[0].name}</b></td>
                        </tr>
                `;
                for (let i = 0; i < params.length; i++) {
                    name += `<tr>
                        <td align="left">${params[i].marker}${params[i].seriesName}：</td>
                        <td align="right"><b>${(params[i].value * 100).toFixed(2)}%</b></td>
                    </tr>`;
                }
                name += "</tbody></table>";
                return name;
            }
        },
    }
    chart.setOption(option);
    return chart;
}

function drawRiskIndicatorLineGraph (domId, data) {
    console.log(data);

    const help = {
        sharpeRatio: [],
    }
    const interval = {
        sharpeRatio: [],
    }
    for (let i = 0; i < data.sharpeRatio.length; i++) {
        if (isNaN(data.sharpeRatio[i])) {
            help.sharpeRatio.push(Number.NaN);
            interval.sharpeRatio.push(Number.NaN);
        } else {
            const int = data.sharpeConfidence[i];
            help.sharpeRatio.push(data.sharpeRatio[i] + int.lower);
            interval.sharpeRatio.push(int.upper - int.lower);
        }
    }

    const chart = echarts.init(document.getElementById(domId));
    const option = {
        title: {
            text: "风险指标",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLabel: {
                interval: index => { return index % 2 == 1 }
            },
        },
        yAxis: {
            type: "value",
        },
        legend: {
            data: ["夏普率"],
            x: "center",
            y: "bottom"
        },
        series: [
            {
                name: "夏普率",
                type: "line",
                data: data.sharpeRatio,
                smooth: true,
            },
            {
                type: "bar",
                data: help.sharpeRatio,
                barWidth: 3,
                itemStyle: {
                    normal: {
                        barBorderColor: 'rgba(0,0,0,0)',
                        color: 'rgba(0,0,0,0)'
                    },
                    emphasis: {
                        barBorderColor: 'rgba(0,0,0,0)',
                        color: 'rgba(0,0,0,0)'
                    }
                },
                stack: "confidence-sharpe",
            },
            {
                type: "bar",
                data: interval.sharpeRatio,
                barWidth: 3,
                itemStyle: {
                    color: 'rgba(220,220,220,0.8)'
                },
                stack: "confidence-sharpe",
            }
        ],
        tooltip: {
            trigger: "axis",
            textStyle: {
                align: "left"
            },
            formatter: params => {
                let name = `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${params[0].name}</b></td>
                        </tr>
                `;
                for (let i = 0; i < params.length; i++) {
                    if (params[i].seriesName.indexOf('series') >= 0) {
                        continue;
                    }
                    name += `<tr>
                        <td align="left">${params[i].marker}${params[i].seriesName}：</td>
                        <td align="right"><b>${params[i].value}</b></td>
                    </tr>`;
                }
                name += "</tbody></table>";
                return name;
            }
        },
    }
    chart.setOption(option);
    return chart;
}

function drawEmptyAssetChangeLineGraph (domId, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        cashData: Array(dates.length).fill(Number.NaN),
        monetaryFundData: Array(dates.length).fill(Number.NaN),
        fixedDepositData: Array(dates.length).fill(Number.NaN),
        fundData: Array(dates.length).fill(Number.NaN),
    }
    drawAssetChangeLineGraph(domId, data);
}

function drawEmptyAssetDeltaChangeBarGraph (domId, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        cashDeltaData: Array(dates.length).fill(Number.NaN),
        monetaryFundDeltaData: Array(dates.length).fill(Number.NaN),
        fixedDepositDeltaData: Array(dates.length).fill(Number.NaN),
        fundDeltaData: Array(dates.length).fill(Number.NaN),
        totalDeltaData: Array(dates.length).fill(Number.NaN),
    }
    drawAssetDeltaChangeBarGraph(domId, data);
}

function drawEmptyResidualMaturityPieGraph (domId) {
    const data = [
        { value: 0, name: "T+0" },
        { value: 0, name: "T+1" },
        { value: 0, name: "T+2" },
        { value: 0, name: "30日内" },
        { value: 0, name: "90日内" },
        { value: 0, name: "180日内" },
        { value: 0, name: "365日内" },
        { value: 0, name: "365日以上" },
    ]
    drawResidualMaturityPieGraph(domId, data);
}

function drawEmptyExpectedReturnPieGraph (domId) {
    const data = [
        { value: 0, name: "<1%" },
        { value: 0, name: "1%-2%" },
        { value: 0, name: "2%-5%" },
        { value: 0, name: "5%-10%" },
        { value: 0, name: ">10%" },
    ]
    drawExpectedReturnPieGraph(domId, data);
}

function drawEmptyLiquidityReturnPositionScatterGraph (domId) {
    const data = {
        data: [],
        amount: []
    }
    drawLiquidityReturnPositionScatterGraph(domId, data);
}

function drawEmptyAverageReturnLineGraph (domId, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        data: Array(dates.length).fill(Number.NaN),
        yields: Array(dates.length).fill(Number.NaN),
    }
    drawAverageReturnLineGraph(domId, data);
}

function drawEmptyRiskIndicatorLineGraph (domId, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        sharpeRatio: Array(dates.length).fill(Number.NaN),
    }
    drawRiskIndicatorLineGraph(domId, data);
}


export {
    drawAssetChangeLineGraph,
    drawAssetDeltaChangeBarGraph,
    drawResidualMaturityPieGraph,
    drawExpectedReturnPieGraph,
    drawLiquidityReturnPositionScatterGraph,
    drawAverageReturnLineGraph,
    drawRiskIndicatorLineGraph,

    drawEmptyAssetChangeLineGraph,
    drawEmptyAssetDeltaChangeBarGraph,
    drawEmptyResidualMaturityPieGraph,
    drawEmptyExpectedReturnPieGraph,
    drawEmptyLiquidityReturnPositionScatterGraph,
    drawEmptyAverageReturnLineGraph,
    drawEmptyRiskIndicatorLineGraph
}