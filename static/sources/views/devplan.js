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
                                {},
                                {view: 'label', label: '运行成本：', width: 180, id: 'gen:cost'},
                                {},
                                {view: 'label', label: '弃风指标：', width: 180, id: 'wind:cost'},
                                {},
                                {view: 'label', label: '旋备指标：', width: 180, id: 'spin:cost'},
                                {},
                                {view: 'label', label: '断面指标：', width: 180, id: 'margin:cost'},
                                {}
                            ]
                        },
                        {id: 'chart1', css: "panel"},
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
        readPlanData('' + now.getFullYear() + month + day).then(function (r) {
            let res = r.json();
            if (res.code !== 0) {
                console.log(res.msg);
            }
            else {
                $$('gen:cost').define('label', '运行成本：'+parseFloat(res.gen_cost).toFixed(2));
                $$('gen:cost').refresh();
                $$('wind:cost').define('label', '弃风指标：'+parseFloat(res.wind).toFixed(2));
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
                        let color = '#1a78cc';
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
        window.onresize = null;
        this.app.detachEvent("toggle:menu");
    }
}