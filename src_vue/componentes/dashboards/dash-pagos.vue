<template>
    <div>
        <div class="tab-struct custom-tab-1 mb-4">
            <ul class="nav nav-tabs" style="border-bottom:1px solid #CDCDCD">
                <li :class="altCss(section == 'resumen', 'active', '')" v-on:click="changeSection('resumen')"><a href="#">Resumen 1</a></li>
                <li :class="altCss(section == 'resumen_alt', 'active', '')" v-on:click="changeSection('resumen_alt')"><a href="#">Resumen 2</a></li>
                <li :class="altCss(section == 'money', 'active', '')" v-on:click="changeSection('money')"><a href="#">Datos financieros</a></li>
                <li :class="altCss(section == 'estructura', 'active', '')" v-on:click="changeSection('estructura')"><a href="#">Estructura</a></li>
                <li class="active"><a href="#" class="px-0" style="visibility:hidden">H</a></li>
            </ul>
        </div>
        <!-- **************************************************************** -->
        <!-- ********************** SECTION ESTRUCTURA ********************** -->
        <!-- **************************************************************** -->
        <div :class="showCss('section', 'estructura')">
            <div class="row">
                <div class="col-sm-3">
                    <div class="panel panel-default card-view border pt-4 pb-3">
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body py-0">
                                <span class="uppercase-font weight-500 font-14 block text-center txt-dark">TOTAL REGISTROS</span>
                                <div class="weight-500 txt-success text-center mt-2 fs-1" v-if="status_sch == state.LOADING">
                                    <i class="fa fa-spin fa-spinner"></i>
                                </div>
                                <div class="weight-500 txt-success text-center mt-2 fs-5" v-else-if="num_registros == -1">
                                    Sin analizar
                                </div>
                                <div class="weight-500 txt-success text-center mt-0 fs-1" style="line-height:1.2em" v-else>
                                    {{ numformat(num_registros) }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- END PANEL -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="pull-left">
                                <h6 class="panel-title txt-dark">Métricas</h6>
                            </div>
                            <div class="clearfix"></div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div  class="panel-body">
                                <div class="d-flex align-items-center pt-0 pb-3" v-if="status_sch == state.LOADING">
                                    <i class="fa fa-spin fa-spinner me-2 fs-4"></i> <span>Cargando métricas...</span>
                                </div>
                                <div v-else>
                                    <div v-for="(elm, i) in rawSchema.filter(elm => elm.field != '_id')" :key="i">
                                        <span class="font-12 head-font txt-dark">{{ pairs[elm.field] }}<span class="pull-right">{{ getPercent(elm.total) }}%</span></span>
                                        <div class="progress mt-0 mb-3">
                                            <div :class="elm.total == num_registros? 'progress-bar progress-bar-success': 'progress-bar progress-bar-danger'" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" :style="{width: getPercent(elm.total) + '%'}" role="progressbar"> <span class="sr-only">85% Complete (success)</span></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-9">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <h6 class="panel-title txt-dark">ESTRUCTURA DE LA BASE DE DATOS DE PAGOS</h6>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" v-if="status_sch == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                    <a href="javascript:void(0)" class="refresh me-2" v-on:click="getSchema(true)" v-else><i class="zmdi zmdi-replay"></i></a>
                                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body">
                                <div class="" v-if="status_sch == state.LOADING">
                                    <div class="d-flex align-items-center pt-0 pb-3">
                                        <i class="fa fa-spin fa-spinner me-3 fs-2"></i>
                                        <div>
                                            <div>Cargando estructura de la base de datos...</div>
                                            <div>{{ (rawSchema.length > 0)? rawSchema.length - 1: 0 }} de {{ campos.length }} campos cargados.</div>
                                        </div>
                                    </div>
                                    <div class="progress progress-lg mt-3">
                                        <div class="progress-bar progress-bar-success" :style="{width: porcion[pinload].per}" role="progressbar">{{ porcion[pinload].per }}</div>
                                    </div>
                                </div>
                                <table class="table" v-if="rawSchema.length > 0">
                                    <thead>
                                        <tr>
                                            <th class="colmin text-center">No.</th>
                                            <th>Nombre del campo</th>
                                            <th>Nombre corto</th>
                                            <th class="colmin text-center">Apariciones del campo</th>
                                            <th class="colmin text-center">Estado</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(elm, i) in rawSchema.filter(elm => elm.field != '_id')" :key="i">
                                            <td class="text-center">{{ i + 1 }}</td>
                                            <td>{{ pairs[elm.field] }}</td>
                                            <td>{{ elm.field }}</td>
                                            <td class="text-right">{{ numformat(elm.total) }}</td>
                                            <td class="text-center">
                                                <span class="label label-success px-2" v-if="num_registros == elm.total"><i class="fa fa-check me-1"></i>Completo</span>
                                                <span class="label label-danger px-2" v-else>- {{ num_registros - elm.total }}</span>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- ************************************************************* -->
        <!-- ********************** SECTION RESUMEN ********************** -->
        <!-- ************************************************************* -->
        <div :class="(section == 'resumen' || section == 'resumen_alt')? '': 'd-none'">
            <!-- END COUNTERS -->
            <div class="row">
                <div class="col-sm-3">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <h6 class="panel-title txt-dark">PERIODOS</h6>
                                <div>
                                    <a v-on:click="changeDisplay('table')" href="javascript:void(0)" :class="display == 'table'? 'txt-success me-2': 'me-2'"><i class="fa fa-list"></i></a>
                                    <a v-on:click="changeDisplay('chart')" href="javascript:void(0)" :class="display == 'chart'? 'txt-success': ''"><i class="fa fa-bar-chart-o"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body row pa-0">
                                <!-- TABLA 1 -->
                                <mng-time ref="xtime" :coleccion="'retec_pagos_' + indice" :alias="'time_pago_' + indice"></mng-time>
                            </div>
                        </div>
                    </div>
                    <local-counter ref="contador_1" class="border" texto="REGISTROS" valor="0" duracion="1" miles></local-counter>
                </div>
                <div class="col-sm-9">
                    <div :class="section == 'resumen'? 'row': 'd-none'">
                        <div class="col-sm-4">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <h6 class="panel-title txt-dark force-cap">Plan salud <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                        <div>
                                            <a href="javascript:void(0)" class="me-2" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                            <a href="javascript:void(0)" class="refresh me-2" v-on:click="reloadResumen" v-else><i class="zmdi zmdi-replay"></i></a>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_1" cols="_id:PLAN,total:FACTURAS" compact lastright sumar="total"></table-data>
                                        <am-pie :class="altCss(display == 'chart')" ref="gp_1" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor></am-pie>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <h6 class="panel-title txt-dark force-cap">TContra <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                        <div>
                                            <a href="javascript:void(0)" class="me-2" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                            <a href="javascript:void(0)" class="refresh me-2" v-on:click="reloadResumen" v-else><i class="zmdi zmdi-replay"></i></a>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_2" cols="_id:TCONTRA,total:FACTURAS" compact lastright sumar="total"></table-data>
                                        <am-bar :class="altCss(display == 'chart')" ref="gp_2" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor></am-bar>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <h6 class="panel-title txt-dark">Ámbito <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                        <div>
                                            <a href="javascript:void(0)" class="me-2" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                            <a href="javascript:void(0)" class="refresh me-2" v-on:click="reloadResumen" v-else><i class="zmdi zmdi-replay"></i></a>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_3" cols="_id:ÁMBITO,total:FACTURAS EVE" compact lastright sumar="total"></table-data>
                                        <am-pie :class="altCss(display == 'chart')" ref="gp_3" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor></am-pie>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div :class="section == 'resumen_alt'? 'row': 'd-none'">
                        <div class="col-sm-12">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <h6 class="panel-title txt-dark force-cap">TIPO USUARIO <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                        <div>
                                            <a href="javascript:void(0)" class="me-2" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                            <a href="javascript:void(0)" class="refresh me-2" v-on:click="reloadResumen" v-else><i class="zmdi zmdi-replay"></i></a>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_4" cols="_id:TIPO ID,total:PAGOS GENERAL" compact lastright sumar="total"></table-data>
                                        <am-bar :class="altCss(display == 'chart')" ref="gp_4" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor></am-bar>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <h6 class="panel-title txt-dark force-cap">TCONTRA EVE <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                        <div>
                                            <a href="javascript:void(0)" class="me-2" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                            <a href="javascript:void(0)" class="refresh me-2" v-on:click="reloadResumen" v-else><i class="zmdi zmdi-replay"></i></a>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_5" cols="_id:TIPO ID,total:PAGOS EVE" compact lastright sumar="total"></table-data>
                                        <am-bar :class="altCss(display == 'chart')" ref="gp_5" campo_categoria="_id" campo_valor="total" tooltip etiquetas sin_valores grilla="0" altura="180" multicolor></am-bar>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <h6 class="panel-title txt-dark force-cap">TCONTRA CAP <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                        <div>
                                            <a href="javascript:void(0)" class="me-2" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                            <a href="javascript:void(0)" class="refresh me-2" v-on:click="reloadResumen" v-else><i class="zmdi zmdi-replay"></i></a>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_6" cols="_id:TIPO ID,total:PAGOS CAP" compact lastright sumar="total"></table-data>
                                        <am-bar :class="altCss(display == 'chart')" ref="gp_6" campo_categoria="_id" campo_valor="total" tooltip etiquetas sin_valores grilla="0" altura="180" multicolor></am-bar>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <h6 class="panel-title txt-dark force-cap">TCONTRA PDR <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                        <div>
                                            <a href="javascript:void(0)" class="me-2" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner"></i></a>
                                            <a href="javascript:void(0)" class="refresh me-2" v-on:click="reloadResumen" v-else><i class="zmdi zmdi-replay"></i></a>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_7" cols="_id:TIPO ID,total:PAGOS PDR" compact lastright sumar="total"></table-data>
                                        <am-bar :class="altCss(display == 'chart')" ref="gp_7" campo_categoria="_id" campo_valor="total" tooltip etiquetas sin_valores grilla="0" altura="180" multicolor></am-bar>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- END COL-SM-9 -->
            </div>
        </div>
        <!-- *********************************************************** -->
        <!-- ********************** SECTION MONEY ********************** -->
        <!-- *********************************************************** -->
        <div :class="showCss('section', 'money')">
            <div class="alert alert-warning">
                <div class="d-flex">
                    <i class="fa fa-wrench me-2"></i>
                    <div><b class="me-2" style="font-weight:bold">Sección en construcción:</b> Pagos!</div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Counter from './../Contador_light.vue';
// import Xtable from './../table-data.vue';
import PieChart from './../amcharts/pie.vue';
import BarChart from './../amcharts/bar.vue';
import Xtime from './../mng-periodos.vue';
export default {
    // components: {'local-counter': Counter, 'lc-table': Xtable, 'am-pie': PieChart, 'am-bar': BarChart, 'mng-time': Xtime},
    components: {'local-counter': Counter, 'am-pie': PieChart, 'am-bar': BarChart, 'mng-time': Xtime},
    props: {
        indice: {type: String, default: ''}
    },
    data() {
        return {
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            campos: ['ifa', 'tpp', 'idp', 'nmp', 'pla', 'tra', 'idc', 'tus', 'ius', 'iau', 'fau', 'amb', 'ids', 'ser', 'dia', 'can', 'fp', 'fr', 'vdo', 'gde', 'mpa', 'vpbs', 'vpac', 'vppm'],
            pairs: {_id:'TOTAL REGISTROS', ifa:'IDFACTURA', tpp:'TIPOIDPRESTADOR', idp:'IDPRESTADOR', nmp:'NOMBREPRESTADOR', pla:'PLANSALUD', tra:'TCONTRA', idc:'IDCONTRATO', tus:'TIPOIDUSUARIO', ius:'IDUSUARIO', iau:'IDAUTORIZACION', fau:'FAUTO', amb:'AMBITO', ids:'IDSERVICIO', ser:'DESSERVICIO', dia:'DIAGPPAL', can:'CANT', fp:'FPRES', fr:'FRAD', vdo:'VLRFACTURADO', gde:'GLOSADEFINITIVA', mpa:'MECPAGO', vpbs:'VLRPAGADOPBS', vpac:'VLRPAGADOPAC', vppm:'VLRPAGADOPM'},
            lc_token: '',
            tokens: {},
            display: 'table',   // table | chart
            hoy: '',
            coleccion: '',      // Fixed in mounted.
            key_history: '',    // Fixed in mounted.
            section: 'estructura',
            num_registros: -1,
            lastTime: null,      // Fixed in catch event time-select
            rawData: null,
            rawSchema: [],
            status: 'ini',
            status_sch: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            pinload: 0,
            porcion: [
                {'a': 0, 'b': 5, 'per': '0'}, 
                {'a': 5, 'b': 10, 'per': '21%'}, 
                {'a': 10, 'b': 15, 'per': '42%'}, 
                {'a': 15, 'b': 20, 'per': '63%'}, 
                {'a': 20, 'b': 24, 'per': '83%'}, 
                {'per': '100%'}
            ],
        }
    },
    methods: {
        numformat: function(snum){
            var tm = new String(snum);
            return tm.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        getPercent: function(num){
            var tm = (num / this.num_registros) * 100;
            if(tm >= 99.9 && tm < 100){
                return 99.99;
            }
            return (tm % 1 == 0)? tm: tm.toFixed(2);
        },
        pad: function(arg){
            return (`0${arg}`).slice(-2);
        },
        makeToken: function(){
            var str = '';
            for(var i = 0; i < 5; i++){
                var num = Math.round(Math.random() * 25 + 65);
                str += String.fromCharCode(num);
            }
            str += Math.round(Math.random() * 999 + 1000);
            return str;
        },
        getNow: function(){
            if(this.hoy == ''){
                var tod = new Date();
                this.hoy = tod.getFullYear() + '-' + this.pad(tod.getMonth() + 1) + '-' + this.pad(tod.getDate());
            }
            return this.hoy;
        },
        showCss: function(att, val){
            return (this[att] == val)? '': 'd-none';
        },
        altCss: function(bool, a='', b='d-none'){
            return bool? a: b;
        },
        changeDisplay: function(arg){
            this.display = arg;
            localStorage.setItem('display_pay', arg);
        },
        changeSection: function(sect){
            // sect = estructura | resumen | money
            this.section = sect;
            if(this.section == 'estructura'){
                if(this.rawSchema.length == 0){
                    this.getSchema(false);
                }
            }else if(this.section == 'resumen' || this.section == 'resumen_alt'){
                if(this.rawData == null && this.lastTime != null){
                    this.getHistory(this.lastTime.periodo);
                    this.$refs.contador_1.setValor(this.lastTime.total);
                }
            }
        },
        loadSchema: function(tload){
            // facets.unshift("x_id:group:none:1");
            this.pinload = tload;
            if(this.pinload <= 4){
                var lim_a = this.porcion[this.pinload].a;
                var lim_b = this.porcion[this.pinload].b;
                var facets = [];
                var matches = [];
                if(this.pinload == 0){
                    facets = ["x_id:group:none:1"].concat(this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":group:none:1"));
                    matches = this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":" + elm + ":exists:true");
                }else if(this.pinload < 4){
                    facets = this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":group:none:1");
                    matches = this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":" + elm + ":exists:true");
                }else{
                    facets = this.campos.slice(lim_a).map(elm => "x_" + elm + ":group:none:1");
                    matches = this.campos.slice(lim_a).map(elm => "x_" + elm + ":" + elm + ":exists:true");
                }
                console.log('Load slice ' + this.pinload);
                console.log(this.porcion[this.pinload]);
                var pam = new FormData();
                pam.append('tema', this.coleccion);
                pam.append('facets', facets.join('|'));
                pam.append('match', matches.join('|'));
                this.status_sch = this.state.LOADING;
                console.log('Init load schema');
                axios.post(root_path + 'reservas/mng/facet', pam).then(res => {
                    if(res.data.length > 0){
                        var raw = res.data[0];
                        if(tload == 0){
                            this.rawSchema.push({'field': '_id', 'total': raw['x_id'][0].total});
                            this.num_registros = raw['x_id'][0].total;
                        }
                        this.campos.forEach(elm => {
                            if(raw['x_' + elm] != undefined){
                                if(raw['x_' + elm].length > 0){
                                    this.rawSchema.push({'field': elm, 'total': raw['x_' + elm][0].total});
                                }
                            }
                        });
                    }
                    this.addSchema(this.rawSchema);
                    this.status_sch = this.state.LOADED;
                    this.loadSchema(this.pinload + 1);
                }).catch(err => {
                    this.status_sch = this.state.FAILED;
                    console.log('Load schema failed!');
                    console.log(err);
                });
            }
        },
        loadSchemaParts: function(){
            this.rawSchema = [];
            this.pinload = 0;
            this.loadSchema(this.pinload);
        },
        loadFacetCandidate: function(arg){
            var crx = (arg == 0)? "exists:false": arg + ':int';
            //          Plan salud          TContra              Ámbito             Pending!           Grupo compuesto
            var gra = ["rs_1:group:pla:1", "rs_2:group:tra:1", "rs_3:group:amb:1", "rs_4:group:tus:1", "rs_5:group:tra-tus:1"];

            var gre = ["rs_1:crx:" + crx, "rs_2:crx:" + crx, "rs_3:crx:" + crx, "rs_4:crx:" + crx, "rs_5:crx:" + crx];
            var pam = new FormData();
            pam.append('tema', this.coleccion);
            pam.append('facets', gra.join('|'));
            if(arg != -1) pam.append('match', gre.join('|'));
            this.status = this.state.LOADING;
            axios.post(root_path + 'reservas/mng/facet', pam).then(res => {
                this.rawData = (res.data.length > 0)?  res.data[0]: {'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'rs_5': [], 'rs_6': []};
                this.writeCards();
                this.addHistory(arg, this.rawData);
                localStorage.setItem(this.alias, JSON.stringify({'data': this.periodos, 'current': this.periodo, 'update': this.getNow()}));

                this.status = this.state.LOADED;
            }).catch(err => {
                this.status = this.state.FAILED;
                console.log(err);
            });
        },
        addSchema: function(data){
            localStorage.setItem('sch_' + this.key_history, JSON.stringify(data));
        },
        addHistory: function(ym, data){
            // {update: 'y-m-d', 'per_ym(a)': facets, 'per_ym(b)': facets}
            var kid = 'per_' + ym;
            var tmp = localStorage.getItem(this.key_history);
            if(tmp == null){
                localStorage.setItem(this.key_history, JSON.stringify({kid: data}));
            }else{
                var result = JSON.parse(tmp);
                result[kid] = data;
                localStorage.setItem(this.key_history, JSON.stringify(result));
            }
            this.tokens[kid] = this.lc_token;
        },
        getSchema: function(force=false){
            var tmp = localStorage.getItem('sch_' + this.key_history);
            if(tmp == null || force){
                this.loadSchemaParts();
            }else{
                this.rawSchema = JSON.parse(tmp);
                var num = this.rawSchema.find(elm => elm.field == '_id');
                this.num_registros = (num == undefined)? -1: num.total;
            }
        },
        getHistory: function(ym){
            var tmp = localStorage.getItem(this.key_history);
            console.log('Here code down:');
            if(tmp == null){
                this.loadFacetCandidate(ym);
            }else{
                var result = JSON.parse(tmp);
                if(Object.keys(this.tokens).length === 0){      // First time!
                    Object.keys(result).forEach(elm => {
                        this.tokens[elm] = this.lc_token;
                    });
                }
                if(result['per_' + ym] == undefined){
                    this.loadFacetCandidate(ym);
                }else{
                    if(this.tokens['per_' + ym] == this.lc_token){
                        this.rawData = result['per_' + ym];
                        this.writeCards();
                    }else{
                        this.loadFacetCandidate(ym);
                    }
                }
            }
        },
        writeCards: function(){
            if(this.rawData != null){
                this.$refs.table_1.setDatos(this.rawData['rs_1']);
                this.$refs.table_2.setDatos(this.rawData['rs_2']);
                this.$refs.table_3.setDatos(this.rawData['rs_3']);
                this.$refs.table_4.setDatos(this.rawData['rs_4']);
                this.$refs.gp_1.setDatos(this.rawData['rs_1']); // Plan salud
                this.$refs.gp_2.setDatos(this.rawData['rs_2']); // TContra
                this.$refs.gp_3.setDatos(this.rawData['rs_3']); // Ámbito
                this.$refs.gp_4.setDatos(this.rawData['rs_4']); // TIPO USUARIO
                var eve = this.getDataGroup('EVE');
                var cap = this.getDataGroup('CAP');
                console.log('THIS IS CAP');
                console.log(cap);
                var pdr = this.getDataGroup('PDR');
                this.$refs.table_5.setDatos(eve);
                this.$refs.table_6.setDatos(cap);
                this.$refs.table_7.setDatos(pdr);
                this.$refs.gp_5.setDatos(eve);
                this.$refs.gp_6.setDatos(cap);
                this.$refs.gp_7.setDatos(pdr);
            }
        },
        getDataGroup: function(key){
            return this.rawData['rs_5'].filter(elm => elm._id.tm_tra == key).map(elm => {
                return {'_id': elm._id.tm_tus, 'total': elm.total};
            }).sort((a, b) => b.total - a.total);
        },
        reloadResumen: function(){
            if(this.section == 'resumen' || this.section == 'resumen_alt'){
                this.lc_token = this.makeToken();
                this.getHistory(this.lastTime.periodo);
                this.$refs.contador_1.setValor(this.lastTime.total);
            }
        },
        listen: function(){
            this.$eventBus.$on('time-select', obj => {
                this.lastTime = obj;
                if(this.section == 'resumen' || this.section == 'resumen_alt'){
                    this.getHistory(obj.periodo);
                    this.$refs.contador_1.setValor(obj.total);
                }
            });
            this.$eventBus.$on('time-refresh', bool => {
                this.lc_token = this.makeToken();
            });
        }
    },
    mounted() {
        this.lc_token = this.makeToken();
        this.display = (localStorage.getItem('display_pay') == null)? 'table': localStorage.getItem('display_pay');
        this.listen();
        this.coleccion = 'retec_pagos_' + this.indice;
        this.key_history = 'dash_pagos_' + this.indice;
        this.changeSection('resumen');
        this.$refs.xtime.getHistory();
    }
}
</script>
<style scoped>
.colmin {width: 1%; white-space: nowrap}
.bg-white {background: #FFF}
.btn-group > span.btn.bg-white {color:#000; border-left:1px solid #DEE2E6 !important; border-top:1px solid #DEE2E6 !important; border-right:1px solid #DEE2E6 !important}
.bg-inactive {background: #EDEDED}
.btn-group > span.btn.bg-inactive {color:#919191; border-top:1px solid #DEE2E6 !important}
.btn-group > span.btn:last-child {border-right:1px solid #DEE2E6 !important}
.btn-group > span.btn.bg-inactive + .bg-inactive {border-left:1px solid #CDD2D6 !important}
.force-cap {text-transform: lowercase}
.force-cap:first-letter {text-transform: capitalize}
.opaco {opacity: .35 !important}
</style>