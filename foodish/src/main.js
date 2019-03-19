import Vue from "vue";
import App from "@/App";
import router from "@/router";
import store from "@/store";
import request from "@/utils/request";
import * as utils from "@/utils/utils";
import * as API from "@/utils/api";
import { dateFormat, money } from "@/utils/filter.js";
import iView from 'iview';
import 'iview/dist/styles/iview.css';
import locale from 'iview/dist/locale/en-US';

Vue.use(iView, { locale });
Vue.config.productionTip = false;
Vue.prototype.$http = request;
Vue.prototype.API = API;
Vue.prototype.$utils = utils;

Vue.filter("money", money);
Vue.filter("dateFormat", dateFormat);
new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App)
});
