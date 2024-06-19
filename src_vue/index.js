//import Vue from "vue";

window.axios = require('axios');
window.axios.defaults.xsrfHeaderName = "X-CSRFToken";
window.axios.defaults.xsrfCookieName = "csrftoken";

// const { MongoClient } = require('mongodb');
//window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
//window.token = document.head.querySelector("meta[name='csrf-token']").content;
/*if(token){
    alert(token.content);
    window.axios.defaults.headers.common['X-CSRF-TOKEN'] = token.content;
}else{
    alert('No se encontró el token');
}*/

window.registerJSON = function(hash, data, prop=null){
    let fc = new Date();
    let update = [fc.getFullYear(), (fc.getMonth() + 1).toString().padStart(2, '0'), fc.getDate().toString().padStart(2, '0')].join('-');
    if(prop != null){
        let raw = localStorage.getItem(hash);
        if(raw != null){
            let tmp = JSON.parse(raw);
            tmp.data[prop] = data;
            localStorage.setItem(hash, JSON.stringify(tmp));
        }else{
            let datajs = {};
            datajs[prop] = data;
            localStorage.setItem(hash, JSON.stringify({'data': datajs, 'update': update}));
        }
    }else{
        localStorage.setItem(hash, JSON.stringify({'data': data, 'update': update}));
    }
    // this.tokens[kid] = this.lc_token;
}

window.getRegisterJSON = function(hash, prop=null){
    let tmp = localStorage.getItem(hash);
    if(tmp != null){
        let rs = JSON.parse(tmp);
        if(prop == null){
            return rs.data;
        }else{
            return (rs.data == undefined)? null: rs.data[prop];
        }
        // return (prop == null)? rs.data: rs.data[prop];
    }
    return null;
}

window.unregisterJSON = function(hash){
    localStorage.removeItem(hash);
}

window.customPost = async function(url = '', data={}){
    // data.append('csrfmiddlewaretoken', $('#csrf-helper input[name="csrfmiddlewaretoken"]').attr('value'));    
    // data['csrfmiddlewaretoken'] = token_root;
    let config = {
        'method': 'POST', 
        'mode': 'cors', 
        'cache': 'no-cache',
        'credentials': 'same-origin',
        'headers': {
            'Accept': 'application/json',
            // 'Content-Type': 'application/json',
            // 'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': token_root,
        },
        // 'Content-Type': 'application/x-www-form-urlencoded',
        'redirect': 'follow',
        'referrerPolicy': 'no-referrer',
        'body': data
        // 'body': JSON.stringify(data)
    };
    const response = await fetch(url, config);
    return response.json();
}

window.customPostBlind = async function(url = '', data={}){
    let config = {
        'method': 'POST', 
        'mode': 'cors', 
        'cache': 'no-cache',
        'credentials': 'same-origin',
        'headers': {
            'Accept': 'application/json',
            'X-CSRFToken': token_root,
        },
        'redirect': 'follow',
        'referrerPolicy': 'no-referrer',
        'body': data
    };
    const response = fetch(url, config);
    return {'status': 'blind'};
}

window.generatorKey = function(){
    let fc = new Date();
    let ini = fc.getFullYear() + '' + fc.getMonth() + '' + fc.getDate() + '_';
    let code = ini + [1, 2, 3, 4, 5].reduce((ac, elm) => ac += String.fromCharCode(Math.round(Math.random() * 25) + 65), '');
    return code;
}

window.Vue = require('vue');
window.Vue.prototype.$eventBus = new Vue();

Vue.component('contador', require('./componentes/Contador.vue').default);
Vue.component('contador-light', require('./componentes/Contador_light.vue').default);
Vue.component('navegador', require('./componentes/navegacion.vue').default);
Vue.component('consultar-usuario', require('./componentes/formConsulta.vue').default);

Vue.component('ejemplo', require('./componentes/amcharts/ejemplo.vue').default);
Vue.component('amchart-linea', require('./componentes/amcharts/line.vue').default);
Vue.component('amchart-piramide', require('./componentes/amcharts/piramide.vue').default);
Vue.component('amchart-area', require('./componentes/amcharts/area.vue').default);
Vue.component('amchart-barra', require('./componentes/amcharts/bar.vue').default);
Vue.component('amchart-barra-vertical', require('./componentes/amcharts/bar-vertical.vue').default);
Vue.component('amchart-barra-two', require('./componentes/amcharts/bar-two.vue').default);
Vue.component('amchart-torta', require('./componentes/amcharts/pie.vue').default);
Vue.component('amchart-micro', require('./componentes/amcharts/micro.vue').default);

Vue.component('tool-ymonth', require('./componentes/tools/ymonth.vue').default);
Vue.component('tool-poblacion', require('./componentes/tools/poblacion.vue').default);
Vue.component('tool-vacunados', require('./componentes/tools/vacunados.vue').default);
Vue.component('tool-pagination', require('./componentes/tools/paginacion.vue').default);
Vue.component('tool-busqueda', require('./componentes/busqueda_afiliados.vue').default);
Vue.component('tool-busqueda-lma', require('./componentes/busqueda_lma.vue').default);

Vue.component('google-map', require('./componentes/mapas/googlemap.vue').default);
Vue.component('simple-map', require('./componentes/mapas/simple-map.vue').default);
Vue.component('amchart-colombia', require('./componentes/mapas/colombia.vue').default);
Vue.component('amchart-sucre', require('./componentes/mapas/sucre.vue').default);
Vue.component('amchart-sucre-lista', require('./componentes/mapas/sucreList.vue').default);
Vue.component('amchart-departamentos', require('./componentes/amcharts/departamentos.vue').default);

Vue.component('foto', require('./componentes/Foto.vue').default);
Vue.component('import-lma', require('./componentes/importSystem.vue').default);

Vue.component('fuente-create', require('./componentes/FuenteCreate.vue').default);
Vue.component('fuente-campos-create', require('./componentes/FuenteCamposCreate.vue').default);
Vue.component('fuente-import', require('./componentes/FuenteImport.vue').default);

Vue.component('import-ase', require('./componentes/importAse.vue').default);
Vue.component('import-basic', require('./componentes/import-basic.vue').default);
Vue.component('import-list', require('./componentes/import-list.vue').default);

Vue.component('reader-data', require('./componentes/reader-data.vue').default);
Vue.component('diccionarios', require('./componentes/diccionarios.vue').default);
Vue.component('fragmentador', require('./componentes/fragmentador.vue').default);
Vue.component('geo-location', require('./componentes/geo-location.vue').default);
Vue.component('table-data', require('./componentes/table-data.vue').default);

Vue.component('dash-contratos', require('./componentes/dashboards/dash-contratos.vue').default);
Vue.component('dash-autorizaciones', require('./componentes/dashboards/dash-autorizaciones.vue').default);
Vue.component('dash-facturas', require('./componentes/dashboards/dash-facturas.vue').default);
Vue.component('dash-pagos', require('./componentes/dashboards/dash-pagos.vue').default);
Vue.component('dash-incapacidades', require('./componentes/dashboards/dash-incapacidades.vue').default);

Vue.component('new-dash-contratos', require('./componentes/dashboards/new-dash-contratos.vue').default);
Vue.component('new-dash-autorizaciones', require('./componentes/dashboards/new-dash-autorizaciones.vue').default);
Vue.component('new-dash-facturas', require('./componentes/dashboards/new-dash-facturas.vue').default);
Vue.component('new-dash-pagos', require('./componentes/dashboards/new-dash-pagos.vue').default);
Vue.component('new-dash-incapacidades', require('./componentes/dashboards/new-dash-incapacidades.vue').default);

Vue.component('audit-resumen', require('./componentes/audit_resumen.vue').default);
Vue.component('audit-general', require('./componentes/audit_general.vue').default);
Vue.component('audit-import-rips', require('./componentes/audit_import_rips.vue').default);
Vue.component('audit-facturacion', require('./componentes/audit_facturacion.vue').default);
Vue.component('audit-glosa', require('./componentes/audit_glosa.vue').default);
Vue.component('audit-estado', require('./componentes/audit_estado.vue').default);
Vue.component('audit-kpi', require('./componentes/audit_kpi.vue').default);

Vue.component('audit-asignacion', require('./componentes/audit_asignacion.vue').default);
Vue.component('audit-qr-list', require('./componentes/qr_list.vue').default);
Vue.component('audit-qr-make', require('./componentes/qr_make_acta.vue').default);
Vue.component('retec-piramide', require('./componentes/piramide.vue').default);

Vue.component('retec-custom-a', require('./componentes/custom_1.vue').default);
Vue.component('retec-custom-b', require('./componentes/custom_2.vue').default);

Vue.component('ia-eps-cuentas', require('./componentes/ia_eps.vue').default);
Vue.component('ia-search', require('./componentes/ia_search.vue').default);
Vue.component('ase-geocode', require('./componentes/ase_geocode.vue').default);
Vue.component('ase-manager', require('./componentes/ase_manager.vue').default);

Vue.component('serv-hc-show', require('./componentes/serv_hc_show.vue').default);
Vue.component('serv-hc-register', require('./componentes/serv_hc_register.vue').default);
Vue.component('ghg-compras', require('./componentes/ghg_compras.vue').default);
Vue.component('ghg-import', require('./componentes/ghg_import.vue').default);

Vue.component('root-periodos', require('./componentes/select-periodos.vue').default);
Vue.component('load-and-time', require('./componentes/load_and_time.vue').default);

window.app = new Vue({
    el: '#mainApp'
});
