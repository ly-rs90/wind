import "webix";
import "webix/webix.css";
import "./styles/app.css";
import {JetApp, EmptyRouter, HashRouter } from "webix-jet";
import "webix/i18n/zh.js"

export default class MyApp extends JetApp{
	constructor(config){
		const defaults = {
			id 		: APPNAME,
			version : VERSION,
			router 	: BUILD_AS_MODULE ? EmptyRouter : HashRouter,
			debug 	: !PRODUCTION,
			start 	: "/demo"
		};

		super({ ...defaults, ...config });
		webix.i18n.setLocale("zh-CN");

		/*wjet::plugin*/
	}
}

if (!BUILD_AS_MODULE){
	webix.ready(() => new MyApp().render() );
}