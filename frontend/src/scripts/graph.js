import * as echarts from "echarts/core";
import { LineChart, PieChart, ScatterChart, BarChart, CandlestickChart, GraphChart } from "echarts/charts";
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    ToolboxComponent,
    DataZoomComponent,
    MarkPointComponent,
    MarkLineComponent,
    MarkAreaComponent,
    GraphicComponent,
    SingleAxisComponent
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import { LabelLayout, UniversalTransition } from "echarts/features";

import { timeFormat } from "@/scripts/formatter";
import { FOLLOWED_DATA_NAME_2_CATEGORY, PERCENTILE_CHART_CATEGORY_COLOR, INSTRUMENT_INDICATOR_TRANSLATION_SHORT } from "./constant";

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
    SingleAxisComponent,
    GraphicComponent,
    LineChart,
    PieChart,
    ScatterChart,
    BarChart,
    CandlestickChart,
    GraphChart,
    CanvasRenderer,
    LabelLayout,
    UniversalTransition,
]);

export function initGraph (domId) {
    return echarts.init(document.getElementById(domId));
}

export function connectGraph (charts) {
    echarts.connect(charts);
}

export function drawAssetChangeLineGraph (chart, data) {
    console.log(data);
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
            x: "center",
            y: "bottom"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLabel: {
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
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

export function drawAssetDeltaChangeBarGraph (chart, data) {
    console.log(data);
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
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
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
                type: "line",
                data: data.cashDeltaData,
                smooth: true
            },
            {
                name: "货币基金",
                type: "line",
                data: data.monetaryFundDeltaData,
                smooth: true
            },
            {
                name: "定期存款",
                type: "line",
                data: data.fixedDepositDeltaData,
                smooth: true
            },
            {
                name: "基金",
                type: "line",
                data: data.fundDeltaData,
                smooth: true
            },
            {
                name: "总资产",
                type: "line",
                data: data.totalDeltaData,
                smooth: true
            }
        ]
    }
    chart.setOption(option);
    return chart;
}

export function drawPieGraph (chart, data, title) {
    console.log(data);
    const option = {
        title: {
            text: title,
            x: "center",
            y: "top",
            textAlign: "center"
        },
        tooltip: {
            formatter: (params) => {
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

export function drawResidualMaturityPieGraph (chart, data) {
    return drawPieGraph(chart, data, "剩余期限");
}

export function drawExpectedReturnPieGraph (chart, data) {
    return drawPieGraph(chart, data, "预期收益");
}

export function drawLiquidityReturnPositionScatterGraph (chart, data) {
    console.log(data);
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
            formatter: (params) => {
                return `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${data.name[params.dataIndex]}</b></td>
                        </tr>
                        <tr>
                            <td align="left">流动性：</td>
                            <td align="right"><b>${params.data[0]}</b></td>
                        </tr>
                        <tr>
                            <td align="left">年化收益：</td>
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

export function drawAverageReturnLineGraph (chart, data) {
    console.log(data);
    const option = {
        title: {
            text: "平均年化收益",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLabel: {
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
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
            },
            {
                name: "1年期LPR利率",
                type: "line",
                data: data.lpr,
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

export function drawCumulativeReturnLineGraph (chart, data) {
    console.log(data);
    const option = {
        title: {
            text: "累计持有收益",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLabel: {
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
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
            x: "center",
            y: "bottom"
        },
        series: [
            {
                name: "累计收益（几何平均）",
                type: "line",
                data: data.cumReturn.geometric,
                smooth: true
            },
            {
                name: "累计收益（算术平均）",
                type: "line",
                data: data.cumReturn.arithmetic,
                smooth: true
            },
            {
                name: "上证指数",
                type: "line",
                data: data.cumReturn['000001'],
                smooth: true
            },
            {
                name: "国债指数",
                type: "line",
                data: data.cumReturn['000012'],
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

export function drawDrawdownLineGraph (chart, data) {
    console.log(data);
    const option = {
        title: {
            text: "历史回撤",
            x: "center",
            y: "top",
            textAlign: "center"
        },
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: data.time,
            axisLabel: {
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            type: "value",
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(1) + "%";
                }
            }
        },
        series: [
            {
                name: "回撤（几何平均）",
                type: "line",
                data: data.drawdownGeometric,
                smooth: true
            },
            {
                name: "回撤（算术平均）",
                type: "line",
                data: data.drawdownArithmetic,
                smooth: true
            }
        ],
        legend: {
            x: "center",
            y: "bottom"
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

export function drawRiskIndicatorLineGraph (chart, data) {
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
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
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
                type: "line",
                data: help.sharpeRatio,
                lineStyle: {
                    opacity: 0
                },
                stack: "confidence-sharpe",
                symbol: "none",
                smooth: true
            },
            {
                type: "line",
                data: interval.sharpeRatio,
                lineStyle: {
                    opacity: 0
                },
                areaStyle: {
                    color: "#eaeaea"
                },
                stack: "confidence-sharpe",
                symbol: "none",
                smooth: true
            }
        ],
        tooltip: {
            trigger: "axis",
            textStyle: {
                align: "left"
            },
            formatter: params => {
                const dataIndex = params[0].dataIndex;
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
                        <td align="right"><b>${params[i].value.toFixed(2)}</b>±${data.sharpeConfidence[dataIndex].upper.toFixed(2)}</td>
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

export function drawFundAmountChangeByAssetLineGraph (chart, data) {
    console.log(data);
    const option = {
        title: {
            text: "基金大类资产总额",
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
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            type: "value",
            name: "资产规模",
            position: "left",
            boundaryGap: false
        },
        series: []
    }
    for (const [cls, seriesData] of Object.entries(data.data)) {
        option.series.push({
            name: cls,
            type: "line",
            data: seriesData,
            smooth: true,
            stack: "x",
            areaStyle: {}
        });
    }
    console.log(option.series);
    chart.setOption(option);
    return chart;
}


export function drawFundAmountRatioChangeByAssetLineGraph (chart, data) {
    console.log(data);
    const option = {
        title: {
            text: "基金大类资产占比",
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
                        <td align="right"><b>${(params[i].value * 100).toFixed(2)}%</b></td>
                    </tr>`;
                }
                name += "</tbody></table>";
                return name;
            }
        },
        legend: {
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
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            type: "value",
            name: "资产占比",
            position: "left",
            boundaryGap: false,
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(1) + "%";
                }
            }
        },
        series: []
    }
    for (const [cls, seriesData] of Object.entries(data.data)) {
        option.series.push({
            name: cls,
            type: "line",
            data: seriesData,
            smooth: true,
            stack: "x",
            areaStyle: {}
        });
    }
    console.log(option.series);
    chart.setOption(option);
    return chart;
}


export function drawFundReturnChangeByAssetLineGraph (chart, data) {
    console.log(data);
    const option = {
        title: {
            text: "基金大类资产收益",
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
                    if (Number.isNaN(params[i].value)) {
                        continue;
                    }
                    name += `<tr>
                        <td align="left">${params[i].marker}${params[i].seriesName}：</td>
                        <td align="right"><b>${(params[i].value * 100).toFixed(2)}%</b></td>
                    </tr>`;
                }
                name += "</tbody></table>";
                return name;
            }
        },
        legend: {
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
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            type: "value",
            name: "资产收益",
            position: "left",
            boundaryGap: false,
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(1) + "%";
                }
            }
        },
        series: []
    }
    for (const [cls, seriesData] of Object.entries(data.data)) {
        option.series.push({
            name: cls,
            type: "line",
            data: seriesData,
            smooth: true,
        });
    }
    console.log(option.series);
    chart.setOption(option);
    return chart;
}


export function drawFundDrawdownChangeByAssetLineGraph (chart, data) {
    console.log(data);
    const option = {
        title: {
            text: "基金大类资产收益回撤",
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
                    if (Number.isNaN(params[i].value)) {
                        continue;
                    }
                    name += `<tr>
                        <td align="left">${params[i].marker}${params[i].seriesName}：</td>
                        <td align="right"><b>${(params[i].value * 100).toFixed(2)}%</b></td>
                    </tr>`;
                }
                name += "</tbody></table>";
                return name;
            }
        },
        legend: {
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
                formatter: function (value) {
                    return echarts.time.format(value, '{yyyy}-{MM}');
                }
            },
            min: 'dataMin',
            max: 'dataMax'
        },
        yAxis: {
            type: "value",
            name: "收益回撤",
            position: "left",
            boundaryGap: false,
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(1) + "%";
                }
            }
        },
        series: []
    }
    for (const [cls, seriesData] of Object.entries(data.data)) {
        option.series.push({
            name: cls,
            type: "line",
            data: seriesData,
            smooth: true,
        });
    }
    console.log(option.series);
    chart.setOption(option);
    return chart;
}

export function drawRelevanceScatterGraph (chart, data, states, title, key) {
    console.log(data);

    const mergeDistance = 0.001;

    function mergeClosePoints (points, states, names, symbols, threshold) {
        const mergedPoints = [];
        const mergedNames = [];
        const mergedStates = []; // 1: holding, 2: not holding, 3: mixed
        const visited = new Array(points.length).fill(false);

        for (let i = 0; i < points.length; i++) {
            if (visited[i]) {
                continue;
            }

            let sumX = points[i][0];
            let sumY = points[i][1];
            let count = 1;
            let name = names[i];
            let state = states[symbols[i]] ? 1 : 2;

            for (let j = i + 1; j < points.length; j++) {
                if (visited[j]) {
                    continue;
                }

                const dx = points[i][0] - points[j][0];
                const dy = points[i][1] - points[j][1];
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < threshold) {
                    sumX += points[j][0];
                    sumY += points[j][1];
                    count++;
                    visited[j] = true;
                    name += `<br>${names[j]}`;
                    if (states[symbols[j]] !== states[symbols[i]]) {
                        state = 3;
                    }
                }
            }

            mergedPoints.push([sumX / count, sumY / count]);
            mergedNames.push(name);
            mergedStates.push(state);
            visited[i] = true;
        }

        return [mergedPoints, mergedNames, mergedStates];
    }

    const [mergedData, mergedNames, mergedStates] = mergeClosePoints(data[key], states, data.name, data.order, mergeDistance);

    console.log(mergedData);
    console.log(mergedNames);
    console.log(mergedStates);

    const option = {
        title: {
            text: title,
            x: "center",
            y: "top",
            textAlign: "center"
        },
        xAxis: {
            axisTick: { show: false },
            axisLabel: { show: false }
        },
        yAxis: {
            axisTick: { show: false },
            axisLabel: { show: false }
        },
        tooltip: {
            formatter: (params) => {
                return `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${mergedNames[params.dataIndex]}</b></td>
                        </tr>
                    </tbody>
                </table>
                `
            }
        },
        series: [
            {
                type: 'scatter',
                data: mergedData.map((value, index) => {
                    return {
                        value: value,
                        itemStyle: {
                            color: mergedStates[index] === 1 ?
                                '#5470c6' : mergedStates[index] === 2 ?
                                    '#91cc75' : '#fc8452',
                        }
                    }
                }),
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

export function drawKLineGraph (chart, data, title, period, indicator) {
    console.log(title, period, indicator);
    const dates = data.map(d => d.date);
    const oclhv = data.map(d => [d.open, d.close, d.low, d.high, d.volume]);
    const volumes = data.map(d => d.volume);
    const isUp = data.map((d, i) => {
        if (i === 0) {
            return true;
        } else {
            return d.close > data[i - 1].close;
        }
    });
    const upColor = '#d12c2f';
    const downColor = '#019f02';

    const klineName = period === 'daily' ? '日K' : period === 'weekly' ? '周K' : '月K';

    const option = {
        animation: false,
        title: {
            left: 'center',
            text: title
        },
        legend: {
            top: 460,
            data: [klineName]
        },
        tooltip: {
            transitionDuration: 0,
            confine: true,
            borderRadius: 4,
            borderWidth: 1,
            borderColor: '#333',
            backgroundColor: 'rgba(255,255,255,0.9)',
            textStyle: {
                fontSize: 12,
                color: '#333'
            },
            position: (pos, params, el, elRect, size) => {
                const obj = {
                    top: 60
                };
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 5;
                return obj;
            },
            axisPointer: {
                type: 'cross',
                animation: false,
                label: {
                    backgroundColor: '#ccc',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    shadowBlur: 0,
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    color: '#222'
                }
            },
            formatter: (param) => {
                const index = Array.isArray(param) ? param[0].dataIndex : param.dataIndex;
                const html = `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${dates[index]}</b></td>
                        </tr>
                        <tr>
                            <td align="left"><b>开盘价：</b></td>
                            <td align="right">${data[index].open}</td>
                        </tr>
                        <tr>
                            <td align="left"><b>收盘价：</b></td>
                            <td align="right">${data[index].close}</td>
                        </tr>
                        <tr>
                            <td align="left"><b>最低价：</b></td>
                            <td align="right">${data[index].low}</td>
                        </tr>
                        <tr>
                            <td align="left"><b>最高价：</b></td>
                            <td align="right">${data[index].high}</td>
                        </tr>
                        <tr>
                            <td align="left"><b>成交额：</b></td>
                            <td align="right">${data[index].volume.toLocaleString()}</td>
                        </tr>
                    </tbody>
                </table>
                `
                return html;
            }
        },
        axisPointer: {
            link: [
                {
                    xAxisIndex: [0, 1]
                }
            ]
        },
        dataZoom: [
            {
                type: 'slider',
                xAxisIndex: [0, 1],
                realtime: true,
                top: 420,
                height: 20,
                startValue: data.length - 64,
                endValue: data.length - 1
            },
        ],
        xAxis: [
            {
                type: 'category',
                data: dates,
                boundaryGap: false,
                axisLabel: {
                    formatter: function (value) {
                        return echarts.time.format(value, '{yy}-{MM}-{dd}');
                    }
                },
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    show: true
                }
            },
            {
                type: 'category',
                gridIndex: 1,
                data: dates,
                boundaryGap: false,
                axisLine: { lineStyle: { color: '#777' } },
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    type: 'shadow',
                    label: { show: false },
                    triggerTooltip: true,
                    handle: {
                        show: true,
                        margin: 30,
                        color: 'rgba(0,0,0,0)',
                    }
                },
                axisLabel: {
                    show: false
                },
                axisTick: {
                    show: false
                }
            }
        ],
        yAxis: [
            {
                scale: true,
                splitNumber: 2,
                axisLine: { lineStyle: { color: '#777' } },
                splitLine: { show: true },
                axisTick: { show: false },
                axisLabel: {
                    inside: true,
                    formatter: '{value}\n'
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: { show: false },
                axisLine: { show: false },
                axisTick: { show: false },
                splitLine: { show: false }
            }
        ],
        grid: [
            {
                left: 20,
                right: 20,
                top: 50,
                height: 260
            },
            {
                left: 20,
                right: 20,
                top: 330,
                height: 80
            }
        ],
        graphic: [
            {
                type: 'group',
                left: 'center',
                top: 70,
                width: 400,
                bounding: 'raw',
            }
        ],
        series: [
            {
                name: 'Volume',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                itemStyle: {
                    color: params => isUp[params.dataIndex] ? '#ffffff' : downColor,
                    borderWidth: 1
                },
                data: volumes.map((d, i) => {
                    return {
                        value: d,
                        itemStyle: {
                            borderColor: isUp[i] ? upColor : downColor,
                        }
                    }
                })
            },
            {
                type: 'candlestick',
                name: klineName,
                data: oclhv,
                itemStyle: {
                    color: '#ffffff',
                    color0: downColor,
                    borderColor: upColor,
                    borderColor0: downColor
                },
            },
        ]
    };
    if (indicator.value === 'boll') {
        const bollColor = {
            upper: '#fab842',
            mid: '#272727',
            lower: '#e624e1'
        }
        for (const line of ['upper', 'mid', 'lower']) {
            const name = line.toUpperCase();
            option.legend.data.push(name);
            option.series.push({
                name: name,
                type: 'line',
                data: data.map(d => d[line]),
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1,
                    color: bollColor[line]
                },
                itemStyle: {
                    color: bollColor[line]
                },
                emphasis: {
                    itemStyle: {
                        color: 'transparent',
                        borderColor: 'transparent'
                    }
                }
            });
        }
    }
    chart.setOption(option);
    return chart;
}

export function drawMarketPriceLineGraph (chart, data, title) {
    console.log(data);

    const translation = INSTRUMENT_INDICATOR_TRANSLATION_SHORT;

    const showPercent = {
        '1年期LPR': true,
        '5年期LPR': true,
        '短期贷款利率': true,
        '中长期贷款利率': true,
        'USD/CNY': false,
        'EUR/CNY': false,
        'JPY/CNY': false,
        'GBP/CNY': false,
        'HKD/CNY': false,
        'THB/CNY': false,
        '居民部门': true,
        '非金融企业部门': true,
        '政府部门': true,
        '中央政府': true,
        '地方政府': true,
        '实体经济部门': true,
        '金融部门资产方': true,
        '金融部门负债方': true,
        '全国城镇': true,
        '31个大城市': true,
        '本地户籍': true,
        '外来户籍': true,
        '16-24岁': true,
        '25-59岁': true,
        '16-24岁不含在校生': true,
        '25-29岁不含在校生': true,
        '30-59岁不含在校生': true,
        '社会融资规模增量': false,
        '人民币贷款': false,
        '委托贷款外币贷款': false,
        '委托贷款': false,
        '信托贷款': false,
        '未贴现银行承兑汇票': false,
        '企业债券': false,
        '非金融企业境内股票融资': false,
        '今值': false,
        '预测值': false,
        '前值': false,
    };

    const names = [];
    const series = [];
    let dates = [];
    for (const [name, values] of Object.entries(data)) {
        const translated = translation[name];
        names.push(translated);
        series.push({
            name: translated,
            type: 'line',
            data: values.map(value => value.price),
            smooth: true,
            showSymbol: false
        });
        if (dates.length === 0) {
            dates = values.map(value => value.date);
        }
    }

    const option = {
        animation: false,
        title: {
            text: title,
            left: "center",
        },
        legend: {
            top: 455,
            data: names
        },
        tooltip: {
            transitionDuration: 0,
            confine: true,
            borderRadius: 4,
            borderWidth: 1,
            borderColor: '#333',
            backgroundColor: 'rgba(255,255,255,0.9)',
            textStyle: {
                fontSize: 12,
                color: '#333'
            },
            position: (pos, params, el, elRect, size) => {
                const obj = {
                    top: 60
                };
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 5;
                return obj;
            },
            axisPointer: {
                type: 'cross',
                animation: false,
                label: {
                    backgroundColor: '#ccc',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    shadowBlur: 0,
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    color: '#222'
                }
            },
            formatter: (param) => {
                const index = Array.isArray(param) ? param[0].dataIndex : param.dataIndex;
                let html = `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${dates[index]}</b></td>
                        </tr>
                `
                for (const s of series) {
                    const value = s.data[index];
                    const info = value ? `${value.toFixed(2)}${showPercent[s.name] ? '%' : ''}` : '暂无'
                    html += `
                    <tr>
                        <td align="left"><b>${s.name}：</b></td>
                        <td align="right">${info}</td>
                    </tr>
                    `
                }
                html += `
                    </tbody >
                </table >
                `
                return html;
            }
        },
        dataZoom: [
            {
                type: 'slider',
                realtime: true,
                top: 420,
                height: 20,
                startValue: dates.length - 64,
                endValue: dates.length - 1
            },
        ],
        xAxis: {
            type: 'category',
            data: dates,
            boundaryGap: false,
            axisLabel: {
                formatter: function (value) {
                    return echarts.time.format(value, '{yy}-{MM}-{dd}');
                }
            },
            min: 'dataMin',
            max: 'dataMax',
            axisPointer: {
                show: true
            },
        },
        yAxis: {
            scale: true,
            axisLine: { lineStyle: { color: '#777' } },
            axisLabel: {
                inside: true,
                formatter: `{value}${showPercent[names[0]] ? '%' : ''}\n`
            },
            type: "value"
        },
        grid: {
            left: 20,
            right: 20,
            top: 50,
            height: 355
        },
        graphic: {
            type: 'group',
            left: 'center',
            top: 70,
            width: 400,
            bounding: 'raw',
        },
        series: series
    }
    chart.setOption(option);
    return chart;
}

export function drawPercentileGraph (chart, data, titles) {
    const title = [
        {
            text: '标的价格百分位',
            left: 'center',
            top: 'top'
        }
    ];
    const singleAxis = [];
    const series = [];
    const nLines = data.length;
    const axis = Array.from({ length: 101 }, (_, i) => i);
    data.forEach((d, idx) => {
        title.push({
            textBaseline: 'middle',
            top: ((idx + 0.5) * 95) / nLines + 5 + '%',
            text: titles[idx]
        });
        singleAxis.push({
            left: 150,
            type: 'value',
            boundaryGap: false,
            data: axis,
            min: 0,
            max: 100,
            top: (idx * 95) / nLines + 5 + 5 + '%',
            height: 95 / nLines - 10 + '%',
            axisLabel: {
                interval: 10
            }
        });
        const seriesData = [];
        for (const [name, value] of Object.entries(d.percentile)) {
            const category = FOLLOWED_DATA_NAME_2_CATEGORY[name];
            const color = PERCENTILE_CHART_CATEGORY_COLOR[category];
            seriesData.push({
                value: [value, name],
                itemStyle: {
                    color: color
                }
            });
        }
        series.push({
            singleAxisIndex: idx,
            coordinateSystem: 'singleAxis',
            type: 'scatter',
            data: seriesData,
            symbol: 'rect',
            symbolSize: [3, 15],
        });
    })
    const option = {
        tooltip: {
            position: 'top',
            formatter: (params) => {
                return `<b>${params.value[1]}</b>: ${params.value[0].toFixed(2)}`;
            }
        },
        title: title,
        singleAxis: singleAxis,
        series: series
    };
    chart.setOption(option);

    chart.on('mouseover', function (params) {
        if (params.seriesIndex !== undefined && params.dataIndex !== undefined) {
            option.series.forEach((_, seriesIndex) => {
                chart.dispatchAction({
                    type: 'highlight',
                    seriesIndex: seriesIndex,
                    dataIndex: params.dataIndex
                });
            });
        }
    });

    chart.on('mouseout', function (params) {
        if (params.seriesIndex !== undefined && params.dataIndex !== undefined) {
            option.series.forEach((_, seriesIndex) => {
                chart.dispatchAction({
                    type: 'downplay',
                    seriesIndex: seriesIndex,
                    dataIndex: params.dataIndex
                });
            });
        }
    });

    return chart;
}

export function drawRelationGraph (chart, graph) {
    console.log(graph);
    graph.nodes.forEach(node => {
        const cat = graph.categories[node.category].name;
        if (cat === '基金') {
            node.symbolSize = 20;
        } else if (cat === '股票' || cat === '债券') {
            node.symbolSize = 12;
        } else {
            node.symbolSize = 8;
        }
        node.draggable = true;
    })
    const option = {
        title: {
            text: '基金持仓关联',
            x: "center",
            y: "top",
            textAlign: "center"
        },
        tooltip: {
            formatter: param => {
                if (param.dataType === 'node') {
                    const cat = graph.categories[param.data.category].name;
                    let html = '<table><tbody>';
                    if (cat === '股票' || cat === '债券') {
                        html += `
                        <tr>
                            <td align="left">${param.marker}<b>${cat}信息</b></td>
                        </tr>
                        <tr>
                            <td align="left"><b>${cat}名称</b></td>
                            <td align="right">${param.data.extra.name || '暂无'}</td>
                        </tr>
                        <tr>
                            <td align="left"><b>${cat}简称</b></td>
                            <td align="right">${param.data.extra.abbr || '暂无'}</td>
                        </tr>
                        <tr>
                            <td align="left"><b>${cat}代码</b></td>
                            <td align="right">${param.data.extra.code || '暂无'}</td>
                        </tr>
                        `;
                    } else {
                        html += `
                        <tr>
                            <td align="left">${param.marker}<b>${cat}</b></td>
                        </tr>
                        <tr>
                            <td align="left">${param.data.name}</td>
                        </tr>
                        `;
                    }
                    html += '</tbody></table>';

                    return html;
                } else {  // edge
                    return '';
                }
            }
        },
        legend: [
            {
                data: graph.categories.map(c => c.name),
                top: 30
            }
        ],
        series: [
            {
                type: 'graph',
                layout: 'force',
                data: graph.nodes,
                links: graph.links,
                categories: graph.categories,
                roam: true,
                label: {
                    show: true,
                    position: 'right',
                    formatter: '{b}'
                },
                labelLayout: {
                    hideOverlap: true
                },
                scaleLimit: {
                    min: 0.4,
                    max: 2
                },
                legendHoverLink: false,
                focusNodeAdjacency: true,
                lineStyle: {
                    color: 'source',
                    curveness: 0.3
                },
                force: {
                    edgeLength: 120
                }
            }
        ]
    };
    chart.setOption(option);
    return chart;
}

export function drawGeneralLineGraph (chart, data, legend) {
    console.log(data);
    console.log(legend);
    const dates = data.map(d => d.date.split('T')[0]);
    const option = {
        xAxis: {
            type: "category",
            boundaryGap: false,
            data: dates,
            axisLabel: {
                formatter: function (value) {
                    return echarts.time.format(value, '{yy}-{MM}-{dd}');
                }
            },
            min: 'dataMin',
            max: 'dataMax',
            axisPointer: {
                show: true
            },
        },
        yAxis: {
            type: "value",
            scale: true,
            axisLine: { lineStyle: { color: '#777' } },
        },
        legend: {
            x: "center",
            y: "bottom",
        },
        series: legend.map((name, index) => {
            return {
                name: name,
                type: 'line',
                data: data.map(d => d[`value_${index}`]),
                smooth: false,
                showSymbol: false
            };
        }),
        tooltip: {
            transitionDuration: 0,
            confine: true,
            borderRadius: 4,
            borderWidth: 1,
            borderColor: '#333',
            backgroundColor: 'rgba(255,255,255,0.9)',
            textStyle: {
                fontSize: 12,
                color: '#333'
            },
            position: function (pos, params, el, elRect, size) {
                const obj = {
                    top: 60
                };
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 5;
                return obj;
            },
            axisPointer: {
                type: 'cross',
                animation: false,
                label: {
                    backgroundColor: '#ccc',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    shadowBlur: 0,
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    color: '#222'
                }
            },
            formatter: (param) => {
                console.log(param);
                let html = '<table><tbody>';
                const index = param.dataIndex;
                const d = data[index];
                html += `<tr><td align="left"><b>${dates[index]}</b></td></tr>`;
                legend.forEach((le, idx) => {
                    const key = `value_${idx}`
                    html += `
                    <tr>
                        <td align="left"><b>${le}</b></td>
                        <td align="right">${d[key].toFixed(2)}</td>
                    </tr>`;
                });
                html += '</tbody></table>';
                return html;
            }
        },
    };
    chart.setOption(option);
    return chart;
}

export function drawExpectedReturnGraph (chart, data, months, p) {
    console.log(data);

    data.sort((a, b) => {
        if (b.expected !== a.expected) {
            return b.upper - a.upper;
        } else {
            return a.lower - b.lower;
        }
    });

    const BAR_COLOR = '#889bd8';

    const baseBar = [];
    const valueBar = [];
    data.forEach(d => {
        if (d.upper * d.lower > 0) {
            baseBar.push(d.lower > 0 ? d.lower : d.upper)
            valueBar.push(d.lower > 0 ? d.upper - d.lower : d.lower - d.upper)
        } else {
            baseBar.push({
                value: d.upper,
                itemStyle: {
                    borderColor: 'transparent',
                    color: BAR_COLOR
                },
                emphasis: {
                    itemStyle: {
                        borderColor: 'transparent',
                        color: BAR_COLOR
                    }
                },
            });
            valueBar.push(d.lower);
        }
    });

    const option = {
        title: {
            text: `${months}个月预期收益率\n{small|\n（${(p * 100)}%置信度）}`,
            x: 'center',
            y: 'top',
            textStyle: {
                rich: {
                    small: {
                        fontSize: 12,
                        color: '#999'
                    }
                }
            }
        },
        xAxis: {
            type: 'category',
            data: data.map(d => INSTRUMENT_INDICATOR_TRANSLATION_SHORT[d.code]),
            axisTick: {
                show: false
            },
            axisLabel: {
                interval: 0,
                rotate: 35,
                width: 110,
                overflow: 'break'
            },
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: value => {
                    return (value * 100).toFixed(2) + '%';
                }
            },
            axisPointer: {
                label: {
                    formatter: params => {
                        return (params.value * 100).toFixed(2) + '%';
                    }
                }
            }
        },
        series: [
            {
                type: 'bar',
                data: baseBar,
                stack: 'interval',
                itemStyle: {
                    borderColor: 'transparent',
                    color: 'transparent'
                },
                emphasis: {
                    itemStyle: {
                        borderColor: 'transparent',
                        color: 'transparent'
                    }
                },
                barWidth: 1
            },
            {
                type: 'bar',
                data: valueBar,
                stack: 'interval',
                itemStyle: {
                    borderColor: 'transparent',
                    color: BAR_COLOR
                },
                emphasis: {
                    itemStyle: {
                        borderColor: 'transparent',
                        color: BAR_COLOR
                    }
                },
                barWidth: 1
            },
            {
                type: 'scatter',
                data: data.map(d => d.lower),
                symbol: 'rect',
                symbolSize: [10, 1],
                itemStyle: {
                    borderColor: 'transparent',
                    color: BAR_COLOR
                },
                emphasis: {
                    itemStyle: {
                        borderColor: 'transparent',
                        color: BAR_COLOR
                    }
                },
            },
            {
                type: 'scatter',
                data: data.map(d => d.upper),
                symbol: 'rect',
                symbolSize: [10, 1],
                itemStyle: {
                    borderColor: 'transparent',
                    color: BAR_COLOR
                },
                emphasis: {
                    itemStyle: {
                        borderColor: 'transparent',
                        color: BAR_COLOR
                    }
                },
            }
        ],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                label: {
                    backgroundColor: '#6a7985',
                    show: true
                }
            },
            formatter: params => {
                const index = params.dataIndex;
                const name = `
                <table>
                    <tbody>
                        <tr>
                            <td align="left"><b>${INSTRUMENT_INDICATOR_TRANSLATION_SHORT[data[index].code]}</b></td>
                        </tr>
                <tr>
                        <td align="left">
                        <b>${(data[index].expected * 100).toFixed(2)}%</b>
                        <small>(${(data[index].lower * 100).toFixed(2)}% ~ ${(data[index].upper * 100).toFixed(2)}%)</small>
                        </td>
                    </tr>
                </tbody></table>`;
                return name;
            }
        },
    }
    chart.setOption(option);
    return chart;
}

export function drawEmptyAssetChangeLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        cashData: Array(dates.length).fill(Number.NaN),
        monetaryFundData: Array(dates.length).fill(Number.NaN),
        fixedDepositData: Array(dates.length).fill(Number.NaN),
        fundData: Array(dates.length).fill(Number.NaN),
    }
    return drawAssetChangeLineGraph(chart, data);
}

export function drawEmptyAssetDeltaChangeBarGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        cashDeltaData: Array(dates.length).fill(Number.NaN),
        monetaryFundDeltaData: Array(dates.length).fill(Number.NaN),
        fixedDepositDeltaData: Array(dates.length).fill(Number.NaN),
        fundDeltaData: Array(dates.length).fill(Number.NaN),
        totalDeltaData: Array(dates.length).fill(Number.NaN),
    }
    return drawAssetDeltaChangeBarGraph(chart, data);
}

export function drawEmptyResidualMaturityPieGraph (chart) {
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
    return drawResidualMaturityPieGraph(chart, data);
}

export function drawEmptyExpectedReturnPieGraph (chart) {
    const data = [
        { value: 0, name: "<1%" },
        { value: 0, name: "1%-2%" },
        { value: 0, name: "2%-5%" },
        { value: 0, name: "5%-10%" },
        { value: 0, name: ">10%" },
    ]
    return drawExpectedReturnPieGraph(chart, data);
}

export function drawEmptyLiquidityReturnPositionScatterGraph (chart) {
    const data = {
        data: [],
        amount: [],
        name: []
    }
    return drawLiquidityReturnPositionScatterGraph(chart, data);
}

export function drawEmptyAverageReturnLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        data: {
            holding: Array(dates.length).fill(Number.NaN),
            latest: Array(dates.length).fill(Number.NaN),
        },
        yields: Array(dates.length).fill(Number.NaN),
        lpr: Array(dates.length).fill(Number.NaN),
    }
    return drawAverageReturnLineGraph(chart, data);
}

export function drawEmptyCumulativeReturnLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        cumReturn: {
            geometrc: Array(dates.length).fill(Number.NaN),
            arithmetic: Array(dates.length).fill(Number.NaN),
            '000001': Array(dates.length).fill(Number.NaN),
            '000012': Array(dates.length).fill(Number.NaN),
        }
    }
    return drawCumulativeReturnLineGraph(chart, data);
}

export function drawEmptyDrawdownLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        drawdownGeometric: Array(dates.length).fill(Number.NaN),
        drawdownArithmetic: Array(dates.length).fill(Number.NaN),
    }
    return drawDrawdownLineGraph(chart, data);
}

export function drawEmptyRiskIndicatorLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        sharpeRatio: Array(dates.length).fill(Number.NaN),
        sharpeConfidence: Array(dates.length).fill({ lower: Number.NaN, upper: Number.NaN })
    }
    return drawRiskIndicatorLineGraph(chart, data);
}

export function drawEmptyFundAmountChangeByAssetLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        data: {}
    }
    console.log(data);
    return drawFundAmountChangeByAssetLineGraph(chart, data);
}

export function drawEmptyFundAmountRatioChangeByAssetLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        data: {}
    }
    console.log(data);
    return drawFundAmountRatioChangeByAssetLineGraph(chart, data);
}

export function drawEmptyFundReturnChangeByAssetLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        data: {}
    }
    console.log(data);
    return drawFundReturnChangeByAssetLineGraph(chart, data);
}

export function drawEmptyFundDrawdownChangeByAssetLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        data: {}
    }
    console.log(data);
    return drawFundDrawdownChangeByAssetLineGraph(chart, data);
}

export function drawEmptyRelevanceScatterGraph (chart, title, key) {
    const data = {
        name: []
    };
    data[key] = [];
    const state = {};
    return drawRelevanceScatterGraph(chart, data, state, title, key);
}

export function drawEmptyMarketPriceLineGraph (chart, title) {
    const data = {};
    return drawMarketPriceLineGraph(chart, data, title);
}
