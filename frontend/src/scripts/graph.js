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

function drawRelevanceScatterGraph (chart, data, title, key) {
    console.log(data);

    const mergeDistance = 0.01;

    // 计算点之间的距离并合并距离过近的点
    function mergeClosePoints (points, names, threshold) {
        const mergedPoints = [];
        const mergedNames = [];
        const visited = new Array(points.length).fill(false);

        for (let i = 0; i < points.length; i++) {
            if (visited[i]) {
                continue;
            }

            let sumX = points[i][0];
            let sumY = points[i][1];
            let count = 1;
            let name = names[i];

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
                }
            }

            mergedPoints.push([sumX / count, sumY / count]);
            mergedNames.push(name);
            visited[i] = true;
        }

        return [mergedPoints, mergedNames];
    }

    const [mergedData, mergedNames] = mergeClosePoints(data[key], data.name, mergeDistance);

    console.log(mergedData);
    console.log(mergedNames);

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
                data: mergedData,
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
    return drawRelevanceScatterGraph(chart, data, title, key);
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