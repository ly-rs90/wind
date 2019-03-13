import {JetView} from "webix-jet";


export default class Demo extends JetView{
    config() {
        return {
            rows: [
                {
                    view: "toolbar", padding: 3, css: "toolbar", borderless: 1,
                    elements: [
                        {
                            view: "button", type: "icon", icon: "bars", width: 30, css: "menu",
                            click: () => {
                                $$("sidebar").toggle();
                                this.app.callEvent("toggle:menu");
                            }
                        },
                        {width: 20},
                        {view: "icon", icon: "bookmark", width: 30},
                        {view: "label", label: "风电/光伏风险调度系统"}
                    ]
                },
                {
                    cols: [
                        {
                            view: "sidebar", id: "sidebar", css: "sidebar", collapsed: 1, borderless: 1, data: [
                                {id: "riqianyouhua", value: "日前优化", icon: "hourglass-o"},
                                {id: "riqianinfo", value: "日前详细结果展示", icon: "info-circle"},
                                {id: "rineiyouhua", value: "日内优化", icon: "hourglass-1"},
                                {id: "rineiinfo", value: "日内详细结果展示", icon: "info"},
                                {id: "devplan", value: "机组启停计划", icon: "play"},
                                {id: "powerplan", value: "周发电计划", icon: "battery-half"}
                            ],
                            on: {
                                onAfterSelect: function (id) {
                                    this.$scope.show(id);
                                }
                            }
                        },
                        {
                            $subview: true
                        }
                    ]
                }
            ]
        };
    }
    ready(_$view, _$url) {
        let sidebar = $$("sidebar");
        sidebar.select(sidebar.getFirstId());
    }
}
