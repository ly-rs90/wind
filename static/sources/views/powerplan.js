/**
 @name: powerplan.js
 @editor: PyCharm
 @Date: 2019/3/12 16:19
 @Author: ly
 @Description:
 */
import {JetView} from "webix-jet";
import {option6, option7, option8, option9, readPowerData, timesData} from "../models/data";
import echarts from "echarts";
import "models/walden.js";

let e1, e2, e3, e4;
let getData = function(dt, type, name) {
    readPowerData(dt, type, name).then(function (r) {
        let res = r.json();
        if (type === "basic") {
            $$("gen:cost").define("label", '运行成本：'+parseFloat(res.gen_cost).toFixed(2));
            $$("gen:cost").refresh();
            $$("wind").define("label", '弃风风险：'+parseFloat(res.wind).toFixed(2));
            $$("wind").refresh();
            $$("spin").define("label", '旋备成本：'+parseFloat(res.spin).toFixed(2));
            $$("spin").refresh();
            $$("margin").define("label", '断面指标：'+parseFloat(res.margin).toFixed(2));
            $$("margin").refresh();
            $$('conf:prob').setValue(parseFloat(res.conf).toFixed(2));

            $$("margin:dev").clearAll();
            $$("margin:dev").define("data", res.margin_dev);

            $$("wind:dev").clearAll();
            $$("wind:dev").define("data", res.wind_dev);

            $$("power:dev").clearAll();
            $$("power:dev").define("data", res.power_dev);

            $$("equ:dev").clearAll();
            $$("equ:dev").define("data", res.equ_dev);
            e1.setOption(option6, true);
            e2.setOption(option7, true);
            e1.setOption({
                legend: {top: 20, data: ["优化设定值", "预测均值", "计划区间上限", "计划区间下限"]},
                series: [
                    {data: timesData(res.wind_opt, 100)},
                    {data: timesData(res.wind_fur, 100)},
                    {data: timesData(res.wind_pub, 100)},
                    {data: timesData(res.wind_plb, 100)}
                ]
            });
            e2.setOption({
                series: [
                    {data: timesData(res.power_opt, 100)},
                    {data: timesData(res.power_pub, 100)},
                    {data: timesData(res.power_plb, 100)}
                ]
            });
            e3.setOption({series: [{data: []},{data: []},{data: []},{data: []},{data: []}]});
        }
        if (type === "wind") {
            let devName = $$('wind:dev').getSelectedItem().value;
            if (devName === '总和') {
                e1.setOption(option6, true);
                e1.setOption({
                    legend: {top: 20, data: ["优化设定值", "预测均值", "计划区间上限", "计划区间下限"]},
                    series: [
                        {data: timesData(res.wind_opt, 100)},
                        {data: timesData(res.wind_fur, 100)},
                        {data: timesData(res.wind_pub, 100)},
                        {data: timesData(res.wind_plb, 100)}
                    ]
                });
            }
            else {
                e1.setOption({
                    title: {text: "新能源机组"},
                    legend: {top: 20, data: ["优化设定值", "计划区间上限", "计划区间下限", "预测上限", "预测下限"]},
                    series: [
                        {
                            name: "优化设定值",
                            type: "line",
                            lineStyle: {width: 3},
                            data: timesData(res.wind_opt, 100)
                        },
                        {
                            name: "计划区间上限",
                            type: "line",
                            lineStyle: {width: 3},
                            areaStyle: {origin: 'start', opacity: 0.3},
                            data: timesData(res.wind_pub, 100)
                        },
                        {
                            name: "计划区间下限",
                            type: "line",
                            lineStyle: {width: 3},
                            areaStyle: {origin: 'start', color: '#146499', opacity: 1},
                            data: timesData(res.wind_plb, 100)
                        },
                        {
                            name: "预测上限",
                            type: "line",
                            lineStyle: {width: 3},
                            areaStyle: {origin: 'start', opacity: 0.3},
                            data: timesData(res.wind_cub, 100)
                        },
                        {
                            name: "预测下限",
                            type: "line",
                            lineStyle: {width: 3},
                            areaStyle: {origin: 'start', color: '#146499', opacity: 1},
                            data: timesData(res.wind_clb, 100)
                        }
                    ]
                });
            }
        }
        if (type === "power") {
            let devName = $$('power:dev').getSelectedItem().value;
            if (devName === '总和') {
                e2.setOption(option7, true);
                e2.setOption({
                    series: [
                        {data: timesData(res.power_opt, 100)},
                        {data: timesData(res.power_pub, 100)},
                        {data: timesData(res.power_plb, 100)}
                    ]
                });
            }
            else {
                e2.setOption({title: {text: "传统机组"},series: [{data: res.power_opt},{data: res.power_pub},{data: res.power_plb}]});
            }
        }
        if (type === "margin") {
            e3.setOption({series: [
                    {data: timesData(res.margin_opt, 100)},
                    {data: timesData(res.margin_pub, 100)},
                    {data: timesData(res.margin_plb, 100)},
                    {data: timesData(res.margin_max, 100)},
                    {data: timesData(res.margin_min, 100)},
                ]
            });
        }
        if (type === 'equ') {
            e4.setOption({series: [{data: timesData(res.equ_opt, 100)}]});
        }
        if (res.code !== 0){
            console.log(res.msg);
        }
    });
};

export default class PowerPlan extends JetView{
    config() {
        return {
            type: "space", css: 'top',
            rows: [
                {
                    css: 'panel',
                    cols: [
                        {
                            css: "date-picker date-picker-none", view: "datepicker", width: 180,
                            value: new Date(), format: "%Y/%m/%d", id: "date", stringResult: 1,
                            on: {
                                onChange: function () {
                                    let dat = $$("date").getValue().split(" ")[0].replace(/-/g, "");
                                    getData(dat, "basic");
                                }
                            }
                        },
                        {
                            view: "text", label: "置信区间", labelPosition: "left", width: 180, labelWidth: 100,
                            align: "center", css: "text", id: 'conf:prob'
                        },
                        {
                            view: "combo", label: "优化算法", width: 240, labelPosition: "left", labelWidth: 100,
                            align: "center", options: [
                                {id: "0", value: "确定性算法"},
                                {id: "1", value: "随机-鲁棒算法"}
                            ], css: "combo combo-opt", value: "0"
                        },
                        {view: "label", label: "计算启动时间", css: "label label-2"},
                        {view: "label", label: "计算用时", css: "label label-2"},
                        {view: "button", label: "启动计算", width: 120, align: "center", css: "button-normal"},
                        {view: "label", label: "运行成本：", css: "label", id: "gen:cost"},
                        {view: "label", label: "弃风风险：", css: "label", id: "wind"},
                        {view: "label", label: "旋备成本：", css: "label", id: "spin"},
                        {view: "label", label: "断面指标：", css: "label", id: "margin"}
                    ]
                },
                {
                    view: "scrollview", scroll: "y", borderless: 1,
                    body: {
                        rows: [
                            {
                                type: "wide",
                                cols: [
                                    {
                                        type: "wide", id: 'a',
                                        rows: [
                                            {
                                                responsive: 'a', type: 'wide',
                                                cols: [
                                                    {
                                                        css: "panel",
                                                        cols: [
                                                            {
                                                                width: 200, css: "panel-1", minHeight: 270,
                                                                rows: [
                                                                    {
                                                                        view: "search", placeholder: "输入关键字搜索", width: 180, align: "center",
                                                                        css: 'search',
                                                                        on: {
                                                                            onTimedKeyPress: function () {
                                                                                let dev = $$("wind:dev");
                                                                                let str = this.getValue();
                                                                                dev.filter(function(obj){
                                                                                    return obj.value.indexOf(str) !== -1;
                                                                                });
                                                                            }
                                                                        }
                                                                    },
                                                                    {height: 5},
                                                                    {
                                                                        view: "list", select: 1, borderless: 1, data: [],
                                                                        scroll: "y", css: "panel-1 list", id: "wind:dev",
                                                                        tooltip: function (obj) {
                                                                            return obj.value;
                                                                        },
                                                                        on: {
                                                                            onItemClick: function (id) {
                                                                                let item = $$("wind:dev").getItem(id);
                                                                                let d = $$("date").getValue().split(" ")[0].replace(/-/g, "");
                                                                                getData(d, "wind", item.value);
                                                                            }
                                                                        }
                                                                    }
                                                                ]
                                                            },
                                                            {id: "chart1", minWidth: 600}
                                                        ]
                                                    },
                                                    {
                                                        css: "panel",
                                                        cols: [
                                                            {
                                                                width: 200, css: "panel-1", minHeight: 270,
                                                                rows: [
                                                                    {
                                                                        view: "search", placeholder: "输入关键字搜索", width: 180, align: "center",
                                                                        css: 'search',
                                                                        on: {
                                                                            onTimedKeyPress: function () {
                                                                                let dev = $$("equ:dev");
                                                                                let str = this.getValue();
                                                                                dev.filter(function(obj){
                                                                                    return obj.value.indexOf(str) !== -1;
                                                                                });
                                                                            }
                                                                        }
                                                                    },
                                                                    {height: 5},
                                                                    {
                                                                        view: "list", select: 1, borderless: 1, data: [],
                                                                        scroll: "y", css: "panel-1 list", id: "equ:dev",
                                                                        tooltip: function (obj) {
                                                                            return obj.value;
                                                                        },
                                                                        on: {
                                                                            onItemClick: function (id) {
                                                                                let item = $$("equ:dev").getItem(id);
                                                                                let d = $$("date").getValue().split(" ")[0].replace(/-/g, "");
                                                                                getData(d, "equ", item.value);
                                                                            }
                                                                        }
                                                                    }
                                                                ]
                                                            },
                                                            {id: "chart4", minWidth: 600}
                                                        ]
                                                    }
                                                ]
                                            },
                                            {
                                                type: "wide", id: "row",
                                                rows: [
                                                    {
                                                        responsive: "row", type: "wide",
                                                        cols: [
                                                            {
                                                                css: "panel",
                                                                cols: [
                                                                    {
                                                                        width: 200, css: "panel-1", minHeight: 270,
                                                                        rows: [
                                                                            {
                                                                                view: "search", placeholder: "输入关键字搜索", width: 180, align: "center",
                                                                                css: 'search',
                                                                                on: {
                                                                                    onTimedKeyPress: function () {
                                                                                        let dev = $$("power:dev");
                                                                                        let str = this.getValue();
                                                                                        dev.filter(function(obj){
                                                                                            return obj.value.indexOf(str) !== -1;
                                                                                        });
                                                                                    }
                                                                                }
                                                                            },
                                                                            {height: 5},
                                                                            {
                                                                                view: "list", select: 1, borderless: 1, data: [],
                                                                                scroll: "y", css: "panel-1 list", id: "power:dev",
                                                                                tooltip: function (obj) {
                                                                                    return obj.value;
                                                                                },
                                                                                on: {
                                                                                    onItemClick: function (id) {
                                                                                        let item = $$("power:dev").getItem(id);
                                                                                        let d = $$("date").getValue().split(" ")[0].replace(/-/g, "");
                                                                                        getData(d, "power", item.value);
                                                                                    }
                                                                                }
                                                                            }
                                                                        ]
                                                                    },
                                                                    {id: "chart2", minWidth: 600}
                                                                ]
                                                            },
                                                            {
                                                                css: "panel",
                                                                cols: [
                                                                    {
                                                                        width: 200, css: "panel-1", minHeight: 270,
                                                                        rows: [
                                                                            {
                                                                                view: "search", placeholder: "输入关键字搜索", width: 180, align: "center",
                                                                                css: 'search',
                                                                                on: {
                                                                                    onTimedKeyPress: function () {
                                                                                        let dev = $$("margin:dev");
                                                                                        let str = this.getValue();
                                                                                        dev.filter(function(obj){
                                                                                            return obj.value.indexOf(str) !== -1;
                                                                                        });
                                                                                    }
                                                                                }
                                                                            },
                                                                            {height: 5},
                                                                            {
                                                                                view: "list", select: 1, borderless: 1, css: "panel-1 list",
                                                                                data: [], scroll: "y", id: "margin:dev",
                                                                                tooltip: function (obj) {
                                                                                    return obj.value;
                                                                                },
                                                                                on: {
                                                                                    onItemClick: function (id) {
                                                                                        let item = $$("margin:dev").getItem(id);
                                                                                        let d = $$("date").getValue().split(" ")[0].replace(/-/g, "");
                                                                                        getData(d, "margin", item.value);
                                                                                    }
                                                                                }
                                                                            }
                                                                        ]
                                                                    },
                                                                    {id: "chart3", minWidth: 600}
                                                                ]
                                                            }
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        };
    }

    init(_$view, _$url) {

    }
    ready(_$view, _$url) {
        e1 = echarts.init($$("chart1").getNode(), "walden");
        e2 = echarts.init($$("chart2").getNode(), "walden");
        e3 = echarts.init($$("chart3").getNode(), "walden");
        e4 = echarts.init($$("chart4").getNode(), "walden");
        window.onresize = function() {
            e1.resize();
            e2.resize();
            e3.resize();
            e4.resize();
        };
        this.on(this.app, "toggle:menu", function () {
            e1.resize();
            e2.resize();
            e3.resize();
            e4.resize();
        });

        setTimeout(function () {
            e1.resize();
            e1.setOption(option6);
            e2.resize();
            e2.setOption(option7);
            e3.resize();
            e3.setOption(option8);
            e4.resize();
            e4.setOption(option9);
            getData($$("date").getValue().split(" ")[0].replace(/-/g, ""), "basic");
        });
    }
    destroy() {
        // window.onresize = null;
        // this.app.detachEvent("toggle:menu");
    }
}