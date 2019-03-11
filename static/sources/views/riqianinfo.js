import {JetView} from "webix-jet";

export default class Riqianinfo extends JetView{
    config() {
        return {
            type: "space",
            rows: [
                {template: "日前详细结果展示", css: "page-header", height: 60},
                {
                    type: "wide", height: 46,
                    cols: [
                        {
                            align: "center", css: "date-picker", minWidth: 200, maxWidth: 250,
                            view: "datepicker", value: new Date(), format: "%Y/%m/%d"
                        },
                        {
                            view: "combo", minWidth: 200, maxWidth: 250, css: "combo combo-dev",
                            align: "center", options: [
                                {id: 1, value: "优化算法1"},
                                {id: 2, value: "优化算法2"},
                                {id: 3, value: "优化算法3"},
                                {id: 4, value: "优化算法4"},
                            ]
                        },
                        {
                            view: "combo", minWidth: 200, maxWidth: 250, css: "combo combo-chart",
                            align: "center", options: [
                                {id: 1, value: "优化算法1"},
                                {id: 2, value: "优化算法2"},
                                {id: 3, value: "优化算法3"},
                                {id: 4, value: "优化算法4"},
                            ]
                        },
                        {}
                    ]
                },
                {css: "panel"},
                {css: "panel"}
            ]
        };
    }
}