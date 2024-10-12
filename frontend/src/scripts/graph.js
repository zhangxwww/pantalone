import * as echarts from "echarts/core";
import { LineChart, PieChart, ScatterChart, BarChart, CandlestickChart } from "echarts/charts";
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
    GraphicComponent
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
    UniversalTransition,
    GraphicComponent,
    CandlestickChart
]);

function initGraph (domId) {
    return echarts.init(document.getElementById(domId));
}

function drawAssetChangeLineGraph (chart, data) {
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

function drawAssetDeltaChangeBarGraph (chart, data) {
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

function drawPieGraph (chart, data, title) {
    console.log(data);
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

function drawResidualMaturityPieGraph (chart, data) {
    return drawPieGraph(chart, data, "剩余期限");
}

function drawExpectedReturnPieGraph (chart, data) {
    return drawPieGraph(chart, data, "预期收益");
}

function drawLiquidityReturnPositionScatterGraph (chart, data) {
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
            formatter: function (params) {
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

function drawAverageReturnLineGraph (chart, data) {
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

function drawCumulativeReturnLineGraph (chart, data) {
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


function drawDrawdownLineGraph (chart, data) {
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

function drawRiskIndicatorLineGraph (chart, data) {
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

function drawRelevanceScatterGraph (chart, data, states, title, key) {
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
            formatter: function (params) {
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

function drawEmptyAssetChangeLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        cashData: Array(dates.length).fill(Number.NaN),
        monetaryFundData: Array(dates.length).fill(Number.NaN),
        fixedDepositData: Array(dates.length).fill(Number.NaN),
        fundData: Array(dates.length).fill(Number.NaN),
    }
    return drawAssetChangeLineGraph(chart, data);
}

function drawEmptyAssetDeltaChangeBarGraph (chart, dates) {
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

function drawEmptyResidualMaturityPieGraph (chart) {
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

function drawEmptyExpectedReturnPieGraph (chart) {
    const data = [
        { value: 0, name: "<1%" },
        { value: 0, name: "1%-2%" },
        { value: 0, name: "2%-5%" },
        { value: 0, name: "5%-10%" },
        { value: 0, name: ">10%" },
    ]
    return drawExpectedReturnPieGraph(chart, data);
}

function drawEmptyLiquidityReturnPositionScatterGraph (chart) {
    const data = {
        data: [],
        amount: [],
        name: []
    }
    return drawLiquidityReturnPositionScatterGraph(chart, data);
}

function drawEmptyAverageReturnLineGraph (chart, dates) {
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

function drawEmptyCumulativeReturnLineGraph (chart, dates) {
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

function drawEmptyDrawdownLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        drawdownGeometric: Array(dates.length).fill(Number.NaN),
        drawdownArithmetic: Array(dates.length).fill(Number.NaN),
    }
    return drawDrawdownLineGraph(chart, data);
}

function drawEmptyRiskIndicatorLineGraph (chart, dates) {
    const data = {
        time: dates.map(date => timeFormat(date, true)),
        sharpeRatio: Array(dates.length).fill(Number.NaN),
        sharpeConfidence: Array(dates.length).fill({ lower: Number.NaN, upper: Number.NaN })
    }
    return drawRiskIndicatorLineGraph(chart, data);
}

function drawEmptyRelevanceScatterGraph (chart, title, key) {
    const data = {
        name: []
    };
    data[key] = [];
    const state = {};
    return drawRelevanceScatterGraph(chart, data, state, title, key);
}

function drawKLineGraph (chart) {
    // prettier-ignore
    const colorList = ['#c23531', '#2f4554', '#61a0a8', '#d48265', '#91c7ae', '#749f83', '#ca8622', '#bda29a', '#6e7074', '#546570', '#c4ccd3'];
    const labelFont = 'bold 12px Sans-serif';
    function calculateMA (dayCount, data) {
        let result = [];
        for (let i = 0, len = data.length; i < len; i++) {
            if (i < dayCount) {
                result.push('-');
                continue;
            }
            let sum = 0;
            for (let j = 0; j < dayCount; j++) {
                sum += +data[i - j][1];
            }
            result.push((sum / dayCount).toFixed(2));
        }
        return result;
    }
    // prettier-ignore
    const dates = ["2016-03-29", "2016-03-30", "2016-03-31", "2016-04-01", "2016-04-04", "2016-04-05", "2016-04-06", "2016-04-07", "2016-04-08", "2016-04-11", "2016-04-12", "2016-04-13", "2016-04-14", "2016-04-15", "2016-04-18", "2016-04-19", "2016-04-20", "2016-04-21", "2016-04-22", "2016-04-25", "2016-04-26", "2016-04-27", "2016-04-28", "2016-04-29", "2016-05-02", "2016-05-03", "2016-05-04", "2016-05-05", "2016-05-06", "2016-05-09", "2016-05-10", "2016-05-11", "2016-05-12", "2016-05-13", "2016-05-16", "2016-05-17", "2016-05-18", "2016-05-19", "2016-05-20", "2016-05-23", "2016-05-24", "2016-05-25", "2016-05-26", "2016-05-27", "2016-05-31", "2016-06-01", "2016-06-02", "2016-06-03", "2016-06-06", "2016-06-07", "2016-06-08", "2016-06-09", "2016-06-10", "2016-06-13", "2016-06-14", "2016-06-15", "2016-06-16", "2016-06-17", "2016-06-20", "2016-06-21", "2016-06-22"];
    const data = [[17512.58, 17633.11, 17434.27, 17642.81, 86160000], [17652.36, 17716.66, 17652.36, 17790.11, 79330000], [17716.05, 17685.09, 17669.72, 17755.7, 102600000], [17661.74, 17792.75, 17568.02, 17811.48, 104890000], [17799.39, 17737, 17710.67, 17806.38, 85230000], [17718.03, 17603.32, 17579.56, 17718.03, 115230000], [17605.45, 17716.05, 17542.54, 17723.55, 99410000], [17687.28, 17541.96, 17484.23, 17687.28, 90120000], [17555.39, 17576.96, 17528.16, 17694.51, 79990000], [17586.48, 17556.41, 17555.9, 17731.63, 107100000], [17571.34, 17721.25, 17553.57, 17744.43, 81020000], [17741.66, 17908.28, 17741.66, 17918.35, 91710000], [17912.25, 17926.43, 17885.44, 17962.14, 84510000], [17925.95, 17897.46, 17867.41, 17937.65, 118160000], [17890.2, 18004.16, 17848.22, 18009.53, 89390000], [18012.1, 18053.6, 17984.43, 18103.46, 89820000], [18059.49, 18096.27, 18031.21, 18167.63, 100210000], [18092.84, 17982.52, 17963.89, 18107.29, 102720000], [17985.05, 18003.75, 17909.89, 18026.85, 134120000], [17990.94, 17977.24, 17855.55, 17990.94, 83770000], [17987.38, 17990.32, 17934.17, 18043.77, 92570000], [17996.14, 18041.55, 17920.26, 18084.66, 109090000], [18023.88, 17830.76, 17796.55, 18035.73, 100920000], [17813.09, 17773.64, 17651.98, 17814.83, 136670000], [17783.78, 17891.16, 17773.71, 17912.35, 80100000], [17870.75, 17750.91, 17670.88, 17870.75, 97060000], [17735.02, 17651.26, 17609.01, 17738.06, 95020000], [17664.48, 17660.71, 17615.82, 17736.11, 81530000], [17650.3, 17740.63, 17580.38, 17744.54, 80020000], [17743.85, 17705.91, 17668.38, 17783.16, 85590000], [17726.66, 17928.35, 17726.66, 17934.61, 75790000], [17919.03, 17711.12, 17711.05, 17919.03, 87390000], [17711.12, 17720.5, 17625.38, 17798.19, 88560000], [17711.12, 17535.32, 17512.48, 17734.74, 86640000], [17531.76, 17710.71, 17531.76, 17755.8, 88440000], [17701.46, 17529.98, 17469.92, 17701.46, 103260000], [17501.28, 17526.62, 17418.21, 17636.22, 79120000], [17514.16, 17435.4, 17331.07, 17514.16, 95530000], [17437.32, 17500.94, 17437.32, 17571.75, 111990000], [17507.04, 17492.93, 17480.05, 17550.7, 87790000], [17525.19, 17706.05, 17525.19, 17742.59, 86480000], [17735.09, 17851.51, 17735.09, 17891.71, 79180000], [17859.52, 17828.29, 17803.82, 17888.66, 68940000], [17826.85, 17873.22, 17824.73, 17873.22, 73190000], [17891.5, 17787.2, 17724.03, 17899.24, 147390000], [17754.55, 17789.67, 17664.79, 17809.18, 78530000], [17789.05, 17838.56, 17703.55, 17838.56, 75560000], [17799.8, 17807.06, 17689.68, 17833.17, 82270000], [17825.69, 17920.33, 17822.81, 17949.68, 71870000], [17936.22, 17938.28, 17936.22, 18003.23, 78750000], [17931.91, 18005.05, 17931.91, 18016, 71260000], [17969.98, 17985.19, 17915.88, 18005.22, 69690000], [17938.82, 17865.34, 17812.34, 17938.82, 90540000], [17830.5, 17732.48, 17731.35, 17893.28, 101690000], [17710.77, 17674.82, 17595.79, 17733.92, 93740000], [17703.65, 17640.17, 17629.01, 17762.96, 94130000], [17602.23, 17733.1, 17471.29, 17754.91, 91950000], [17733.44, 17675.16, 17602.78, 17733.44, 248680000], [17736.87, 17804.87, 17736.87, 17946.36, 99380000], [17827.33, 17829.73, 17799.8, 17877.84, 85130000], [17832.67, 17780.83, 17770.36, 17920.16, 89440000]];
    const volumes = [86160000, 79330000, 102600000, 104890000, 85230000, 115230000, 99410000, 90120000, 79990000, 107100000, 81020000, 91710000, 84510000, 118160000, 89390000, 89820000, 100210000, 102720000, 134120000, 83770000, 92570000, 109090000, 100920000, 136670000, 80100000, 97060000, 95020000, 81530000, 80020000, 85590000, 75790000, 87390000, 88560000, 86640000, 88440000, 103260000, 79120000, 95530000, 111990000, 87790000, 86480000, 79180000, 68940000, 73190000, 147390000, 78530000, 75560000, 82270000, 71870000, 78750000, 71260000, 69690000, 90540000, 101690000, 93740000, 94130000, 91950000, 248680000, 99380000, 85130000, 89440000];
    const dataMA5 = calculateMA(5, data);
    const dataMA10 = calculateMA(10, data);
    const dataMA20 = calculateMA(20, data);
    const option = {
        animation: false,
        color: colorList,
        title: {
            left: 'center',
            text: 'Candlestick on Mobile'
        },
        legend: {
            top: 30,
            data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        tooltip: {
            transitionDuration: 0,
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
                realtime: false,
                start: 20,
                end: 70,
                top: 65,
                height: 15,
            },
            {
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 40,
                end: 70,
                top: 30,
                height: 20
            }
        ],
        xAxis: [
            {
                type: 'category',
                data: dates,
                boundaryGap: false,
                axisLabel: {
                    formatter: function (value) {
                        return echarts.time.format(value, '{MM}-{dd}');
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
                        color: '#B80C00'
                    }
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
                top: 110,
                height: 120
            },
            {
                left: 20,
                right: 20,
                height: 40,
                top: 260
            }
        ],
        graphic: [
            {
                type: 'group',
                left: 'center',
                top: 70,
                width: 400,
                bounding: 'raw',
                children: [
                    {
                        id: 'MA5',
                        type: 'text',
                        style: { fill: colorList[1], font: labelFont },
                        left: 0
                    },
                    {
                        id: 'MA10',
                        type: 'text',
                        style: { fill: colorList[2], font: labelFont },
                        left: 'center'
                    },
                    {
                        id: 'MA20',
                        type: 'text',
                        style: { fill: colorList[3], font: labelFont },
                        right: 0
                    }
                ]
            }
        ],
        series: [
            {
                name: 'Volume',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                itemStyle: {
                    color: '#7fbe9e'
                },
                emphasis: {
                    itemStyle: {
                        color: '#140'
                    }
                },
                data: volumes
            },
            {
                type: 'candlestick',
                name: '日K',
                data: data,
                itemStyle: {
                    color: '#ef232a',
                    color0: '#14b143',
                    borderColor: '#ef232a',
                    borderColor0: '#14b143'
                },
                emphasis: {
                    itemStyle: {
                        color: 'black',
                        color0: '#444',
                        borderColor: 'black',
                        borderColor0: '#444'
                    }
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: dataMA5,
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: dataMA10,
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: dataMA20,
                smooth: true,
                showSymbol: false,
                lineStyle: {
                    width: 1
                }
            }
        ]
    };
    chart.setOption(option);
    return chart;
}

export {
    initGraph,

    drawAssetChangeLineGraph,
    drawAssetDeltaChangeBarGraph,
    drawResidualMaturityPieGraph,
    drawExpectedReturnPieGraph,
    drawLiquidityReturnPositionScatterGraph,
    drawAverageReturnLineGraph,
    drawCumulativeReturnLineGraph,
    drawDrawdownLineGraph,
    drawRiskIndicatorLineGraph,
    drawRelevanceScatterGraph,
    drawKLineGraph,

    drawEmptyAssetChangeLineGraph,
    drawEmptyAssetDeltaChangeBarGraph,
    drawEmptyResidualMaturityPieGraph,
    drawEmptyExpectedReturnPieGraph,
    drawEmptyLiquidityReturnPositionScatterGraph,
    drawEmptyAverageReturnLineGraph,
    drawEmptyCumulativeReturnLineGraph,
    drawEmptyDrawdownLineGraph,
    drawEmptyRiskIndicatorLineGraph,
    drawEmptyRelevanceScatterGraph
}