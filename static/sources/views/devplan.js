/**
 @name: devplan.js
 @editor: PyCharm
 @Date: 2019/3/12 10:26
 @Author: ly
 @Description:
 */
import {JetView} from "webix-jet";
import {option5, readPlanData} from "../models/data";
import echarts from "echarts";
import "models/walden.js";

let e1;
let getData = function (date) {
    readPlanData(date).then(function (r) {
        let res = r.json();
        e1.setOption(option5, true);
        if (res.code !== 0) {
            console.log(res.msg);
        }
        else {
            $$('gen:cost').define('label', '运行成本：'+parseFloat(res.gen_cost).toFixed(2));
            $$('gen:cost').refresh();
            $$('wind:cost').define('label', '弃风风险：'+parseFloat(res.wind).toFixed(2));
            $$('wind:cost').refresh();
            $$('spin:cost').define('label', '旋备指标：'+parseFloat(res.spin).toFixed(2));
            $$('spin:cost').refresh();
            $$('margin:cost').define('label', '断面指标：'+parseFloat(res.margin).toFixed(2));
            $$('margin:cost').refresh();
            let xData = [];
            let data = [];
            let seriesData = [];
            for (let key in res.data) {
                if (res.data.hasOwnProperty(key)) {
                    xData.push(key);
                    data.push(res.data[key]);
                }
            }
            for (let i = 0; i < 168; i++) {
                let temp = [];
                data.forEach(function (d1) {
                    temp.push(d1[i]);
                });
                let temp1 = [];
                temp.forEach(function (d2) {
                    let color = '#1d98ff';
                    if (d2 === '0') {
                        color = '#c1250d';
                    }
                    temp1.push({value: 1.993, itemStyle: {color: color}});
                });
                seriesData.push({stack: '1', type: 'bar', data: temp1});
            }
            e1.setOption({yAxis: {data: xData}, series: seriesData});
        }
    });
};
export default class DevPlan extends JetView {
    config() {
        return {
            type: 'wide',
            cols: [
                {width: 10},
                {
                    type: 'wide',
                    rows: [
                        {height: 5},
                        {
                            css: "panel",
                            cols: [
                                {
                                    css: "date-picker date-picker-none", view: "datepicker", width: 180,
                                    value: new Date(), format: "%Y/%m/%d", id: "date", stringResult: 1,
                                    on: {
                                        onChange: function () {
                                            let dat = $$("date").getValue().split(" ")[0].replace(/-/g, "");
                                            getData(dat);
                                        }
                                    }
                                },
                                {},
                                {view: 'label', label: '运行成本：', width: 180, id: 'gen:cost', css: 'label'},
                                {},
                                {view: 'label', label: '弃风风险：', width: 180, id: 'wind:cost', css: 'label'},
                                {},
                                {view: 'label', label: '旋备指标：', width: 180, id: 'spin:cost', css: 'label'},
                                {},
                                {view: 'label', label: '断面指标：', width: 180, id: 'margin:cost', css: 'label'},
                                {}
                            ]
                        },
                        {
                            rows: [
                                {height: 10, css: 'panel'},
                                {
                                    height: 30, css: 'panel',
                                    cols: [
                                        {},
                                        {view: 'button', width: 40, css: 'start-btn'},
                                        {view: 'label', label: '启', css: 'label', autowidth: 1},
                                        {width: 30},
                                        {view: 'button', width: 40, css: 'stop-btn'},
                                        {view: 'label', label: '停', css: 'label', autowidth: 1},
                                        {}
                                    ]
                                },
                                {id: 'chart1', css: "panel"}
                            ]
                        },
                        {height: 5}
                    ]
                },
                {width: 10}
            ]
        };
    }
    init(_$view, _$url) {
        e1 = echarts.init($$('chart1').getNode(), "walden");
        e1.setOption(option5);
        let now = new Date();
        let month = now.getMonth() + 1;
        let day = now.getDate();
        if (month < 9) month = '0' + month;
        if (day < 9) day = '0' + day;
        getData(''+now.getFullYear()+month+day);

    }
    ready(_$view, _$url) {
        window.onresize = function() {
            e1.resize();
        };
        this.on(this.app, "toggle:menu", function () {
            e1.resize();
        });
    }

    destroy() {
        //window.onresize = null;
        //this.app.detachEvent("toggle:menu");
    }
}