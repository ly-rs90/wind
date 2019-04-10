export const getXCoording = function (num, start, len) {
    let n = num || 96;
    let x = [];
    let nowBegin = new Date(new Date().toLocaleDateString()).getTime()/1000;
    let splitSec = 24*3600/n;
    for (let i = 0; i < n; i++) {
        let temp = nowBegin + splitSec * i;
        let t = new Date(temp*1000);
        let hour = t.getHours();
        let minute = t.getMinutes();
        if (minute < 10) minute = "0" + minute;
        x.push(hour + ":" + minute);
    }
    if (start !== undefined && len !== undefined) {
        x = x.slice(start, start + len);
    }
    return x;
};
export const timesData = function (arr, v) {
    let temp = [];
    arr.map(function (item) {
        temp.push((parseFloat(item)*v).toFixed(3));
    });
    return temp;
};
export const option1 = {
    title: {text: "新能源机组"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值", "预测均值", "计划区间上限", "计划区间下限"]},
    tooltip: {trigger: "axis"},
    xAxis: {name: "时间", data: getXCoording(), boundaryGap: false, splitLine: {interval: 3, show: false}, z: 3},
    yAxis: [{name: "兆瓦", nameGap: 8, z: 3}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "预测均值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "计划区间上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start', opacity: 0.3},
            data: []
        },
        {
            name: "计划区间下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start', color: '#146499', opacity: 1},
            data: []
        }
    ]
};
export const option2 = {
    title: {text: "传统机组"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值", "计划区间上限", "计划区间下限"]},
    tooltip: {trigger: "axis"},
    xAxis: {name: "时间", data: getXCoording(), boundaryGap: false, z: 3, splitLine: {show: false}},
    yAxis: [{name: "兆瓦", nameGap: 8, z: 3, scale: true}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "计划区间上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start', opacity: 0.3},
            data: []
        },
        {
            name: "计划区间下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {color: '#146499', opacity: 1, origin: 'start'},
            data: []
        }
    ]
};
export const option3 = {
    title: {text: "监视断面"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值", "计划区间上限", "计划区间下限", "上限", "下限"]},
    tooltip: {trigger: "axis"},
    xAxis: {name: "时间", data: getXCoording(), boundaryGap: false, z: 3, splitLine: {show: false}},
    yAxis: [{name: "兆瓦", nameGap: 8, z: 3}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "计划区间上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start'},
            data: []
        },
        {
            name: "计划区间下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {color: '#146499', origin: 'start', opacity: 1},
            data: []
        },
        {
            name: "上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start'},
            data: []
        },
        {
            name: "下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start', color: '#146499', opacity: 1},
            data: []
        }
    ]
};
export const option4 = {
    title: {text: "等值机组"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值"]},
    tooltip: {trigger: "axis"},
    xAxis: {name: "时间", data: getXCoording(), boundaryGap: false, splitLine: {interval: 3, show: false}},
    yAxis: [{name: "兆瓦", nameGap: 8}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        }
    ]
};

export const option5 = {
    grid: {x: 250, y: 30, x2: 50, y2: 30},
    xAxis: [
        {
            type: 'value', min: 1, max: 168, axisPointer: {show: true}, splitNumber: 7, interval: 24,
            splitLine: {show: false},
            "splitArea": {
                "show": true,
                "areaStyle": {
                    "color": [
                        "rgba(250,250,250,0.5)",
                        "rgba(200,200,200,0.2)"
                    ]
                }
            }
        },
        {splitLine: {show: false}, data: ['第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天']}
    ],
    yAxis: {type: 'category'},
    series: [{type: 'bar', barMaxWidth: 25}]
};

export const option6 = {
    title: {text: "新能源机组"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值", "预测均值", "计划区间上限", "计划区间下限"]},
    tooltip: {trigger: "axis"},
    xAxis: {
        name: "时间", data: (function () {
            let xData = [];
            for (let i=1;i<169;i++){
                xData.push(i);
            }
            return xData;
        })(),
        boundaryGap: false, splitLine: {interval: 3, show: false}, z: 3,
    },
    yAxis: [{name: "兆瓦", nameGap: 8, z: 3}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "预测均值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "计划区间上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start'},
            data: []
        },
        {
            name: "计划区间下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start', color: '#146499', opacity: 1},
            data: []
        }
    ]
};
export const option7 = {
    title: {text: "传统机组"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值", "计划区间上限", "计划区间下限"]},
    tooltip: {trigger: "axis"},
    xAxis: {
        name: "时间", data: (function () {
            let xData = [];
            for (let i=1;i<169;i++){
                xData.push(i);
            }
            return xData;
        })(),
        boundaryGap: false, z: 3, splitLine: {show: false}
    },
    yAxis: [{name: "兆瓦", nameGap: 8, z: 3, scale: true}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "计划区间上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start'},
            data: []
        },
        {
            name: "计划区间下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {color: '#146499', opacity: 1, origin: 'start'},
            data: []
        }
    ]
};
export const option8 = {
    title: {text: "监视断面"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值", "计划区间上限", "计划区间下限", "上限", "下限"]},
    tooltip: {trigger: "axis"},
    xAxis: {
        name: "时间", data: (function () {
            let xData = [];
            for (let i=1;i<169;i++){
                xData.push(i);
            }
            return xData;
        })(),
        boundaryGap: false, z: 3, splitLine: {show: false}
    },
    yAxis: [{name: "兆瓦", nameGap: 8, z: 3}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "计划区间上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start'},
            data: []
        },
        {
            name: "计划区间下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {color: '#146499', origin: 'start', opacity: 1},
            data: []
        },
        {
            name: "上限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start'},
            data: []
        },
        {
            name: "下限",
            type: "line",
            lineStyle: {width: 3},
            areaStyle: {origin: 'start', color: '#146499', opacity: 1},
            data: []
        }
    ]
};
export const option9 = {
    title: {text: "等值机组"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值"]},
    tooltip: {trigger: "axis"},
    xAxis: {
        name: "时间", data: (function () {
            let xData = [];
            for (let i=1;i<169;i++){
                xData.push(i);
            }
            return xData;
        })(),
        boundaryGap: false, splitLine: {interval: 3, show: false}
    },
    yAxis: [{name: "兆瓦", nameGap: 8}, {}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        }
    ]
};
export const option10 = {
    title: {text: "储能设备"},
    grid: {x: 60, y: 60, x2: 50, y2: 40},
    legend: {top: 20, data: ["优化设定值", "容量"]},
    tooltip: {trigger: "axis"},
    xAxis: {name: "时间", data: getXCoording(), boundaryGap: false, splitLine: {interval: 3, show: false}},
    yAxis: [{name: "兆瓦", nameGap: 8}, {name: "兆瓦时", nameGap: 8, splitLine: {show: false}}],
    series: [
        {
            name: "优化设定值",
            type: "line",
            lineStyle: {width: 3},
            data: []
        },
        {
            name: "容量",
            type: "line",
            yAxisIndex: 1,
            lineStyle: {width: 3},
            areaStyle: {opacity: 0.3},
            data: []
        }
    ]
};

export const readData = function (date, type, name) {
    let p = {date: date, type: type};
    if(name) p["name"] = name;
    return webix.ajax().post("/riqian", p);
};

export const readPowerData = function (date, type, name) {
    let p = {date: date, type: type};
    if(name) p["name"] = name;
    return webix.ajax().post("/powerplan", p);
};

export const readPlanData = function (date) {
    let p = {date: date};
    return webix.ajax().post("/devplan", p);
};