<template>
    <div :class="'component-' + status">
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">{{ clientetx }} - <strong>CONTRATOS</strong><br></h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de reservas técnicas</div>
            </div>
            <div class="d-flex">
                <div class="input-group me-4" v-if="clock != null">
                    <div class="input-group-addon" style="background:#FFF">
                        <i class="icon-clock"></i>
                    </div>
                    <input type="text" class="form-control" :value="clock_human">
                </div>
                <select-periodo ref="xtime" :coleccion="fuente" :alias="krache_time"></select-periodo>
                <div class="btn-group">
                    <button :class="display == 'chart'? 'btn btn-success': 'btn btn-default'" @click="display = 'chart'"><i class="fa fa-bar-chart"></i></button>
                    <button :class="display == 'table'? 'btn btn-success': 'btn btn-default'" @click="display = 'table'"><i class="fa fa-table"></i></button>
                </div>
            </div>
        </div>
        <div class="d-flex justify-content-between mb-4 df-options">
            <a :class="section == elm.code? 'flex-fill bg-target': 'flex-fill bg-custom'" href="javascript:void(0)" v-for="(elm, i) in opt" :key="i" @click="setSection(elm.code)">
                <div class="d-flex align-items-center">
                    <span class="lc-icon d-flex align-items-center justify-content-center me-2"><i :class="section == elm.code? 'fa fa-folder-open-o': 'fa fa-folder-o'"></i></span>
                    <span>{{ elm.tx }}</span>
                </div>
            </a>
        </div>
        <div :class="['basic', 'general'].includes(section)? '': 'd-none'">
            <div class="row">
                <div class="col-sm-3">
                    <local-counter ref="contador_1" class="border" texto="REGISTROS" valor="0" duracion="1" miles></local-counter>
                </div>
                <div :class="section == 'general'? 'd-none': 'col-sm-4'">
                    <local-counter ref="contador_4" class="border" texto="# DE PRESTADORES ÚNICOS" valor="0" duracion="1" miles></local-counter>
                </div>
                <div :class="section == 'basic'? 'd-none': 'col-sm-7'">
                    <div class="row">
                        <div class="col-sm-6">
                            <local-counter ref="contador_2" pretag="$ " class="border" texto="TBASE" valor="0" duracion="1" miles></local-counter>
                        </div>
                        <div class="col-sm-6">
                            <local-counter ref="contador_3" pretag="$ " class="border" texto="TACTUAL" valor="0" duracion="1" miles></local-counter>
                        </div>
                    </div>
                </div>
                <div :class="section == 'basic'? 'd-none': 'col-sm-2'">
                    <local-counter ref="contador_33" pretag="" class="border" texto="FACTOR DIFERENCIA" valor="0" duracion="1" miles></local-counter>
                </div>
            </div>
        </div>
        <div :class="section == 'basic'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">Primeros 20 prestadores <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.gp_6.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="table_6" cols="_id:PRESTADOR,suma:VALOR:$ ,total:REGISTROS" compact counter lastright sumar="total"></table-data>
                        <!-- <am-pie :class="altCss(display == 'chart')" ref="gp_60" campo_categoria="_id" campo_valor="total" sin_valores altura="500"></am-pie> -->
                        <am-ver :class="altCss(display == 'chart')" ref="gp_6" pretag="$ " grilla="0" multicolor campo_categoria="_id" campo_valor="suma" etiquetas tooltip sin_valores altura_minima="100" unidad="30"></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'general'? '': 'd-none'">
            <div class="row">
                <div class="col-sm-6">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading border-bottomx">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPOS DE TARIFAS <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <table-data :class="altCss(display == 'table')" ref="table_suma" cols="_id:TARIFA,valor:TOTAL:$ " compact lastright sumar="valor"></table-data>
                                <am-ver :class="altCss(display == 'chart')" ref="sumas" campo_categoria="_id" campo_valor="total" sin_valores redondear altura_minima="230" grilla="0" multicolor cursor tooltip etiquetas></am-ver>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-6">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading border-bottomx">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">Estado <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_3.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <table-data :class="altCss(display == 'table')" ref="table_3" cols="_id:ESTADO,suma:VALOR:$ ,total:REGISTROS" compact lastright sumar="total"></table-data>
                                <am-bar :class="altCss(display == 'chart')" ref="gp_3" redondeado campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="280" multicolor tooltip cursor lanzarevento="select-estado" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-6">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading border-bottomx">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">Plan salud <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <table-data :class="altCss(display == 'table')" ref="table_1" cols="_id:PLAN,suma:VALOR:$ ,total:REGISTROS" compact lastright sumar="total"></table-data>
                                <am-bar :class="altCss(display == 'chart')" ref="gp_1" redondeado campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor tooltip cursor lanzarevento="select-plan" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>
                    <!-- END MICRO TABLE -->
                </div>
                <div class="col-sm-6">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading border-bottomx">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">Tipo de prestador <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_2.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <table-data :class="altCss(display == 'table')" ref="table_2" cols="_id:TIPO DOC,suma:VALOR:$ ,total:REGISTROS" compact lastright sumar="total"></table-data>
                                <am-bar :class="altCss(display == 'chart')" ref="gp_2" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor tooltip cursor lanzarevento="select-tipo" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>
                    <!-- END MICRO TABLE -->
                </div>
            </div>
        </div>

        <div :class="section == 'schema'? '': 'd-none'">
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
                                <div v-else-if="status_sch == state.LOADED">
                                    <div v-for="(elm, i) in campos" :key="i">
                                        <span class="font-12 head-font txt-dark">{{ pairs[elm] }}<span class="pull-right">{{ getPercent(rawSchema['n_' + elm]) }}%</span></span>
                                        <div class="progress mt-0 mb-3">
                                            <div :class="rawSchema['n_' + elm] == num_registros? 'progress-bar progress-bar-success': 'progress-bar progress-bar-danger'" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" :style="{width: getPercent(rawSchema['n_' + elm]) + '%'}" role="progressbar"> <span class="sr-only">85% Complete (success)</span></div>
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
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ESTRUCTURA DE LA BASE DE DATOS DE CONTRATOS</h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
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
                                            <div>Analizando campos requeridos de la base de datos...</div>
                                        </div>
                                    </div>
                                    <div class="progress progress-lg mt-3">
                                        <div class="progress-bar progress-bar-success" :style="{width: porcion[pinload].per}" role="progressbar">{{ porcion[pinload].per }}</div>
                                    </div>
                                </div>
                                <table class="table" v-if="status_sch == state.LOADED">
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
                                        <tr v-for="(elm, i) in campos" :key="i">
                                            <td class="text-center">{{ i + 1 }}</td>
                                            <td>{{ pairs[elm] }}</td>
                                            <td>{{ elm }}</td>
                                            <td class="text-right">{{ numformat(rawSchema['n_' + elm]) }}</td>
                                            <td class="text-center">
                                                <span class="label label-success px-2" v-if="num_registros == rawSchema['n_' + elm]"><i class="fa fa-check me-1"></i>Completo</span>
                                                <span class="label label-danger px-2 dk-hand" @click="showRecord(elm)" v-else>- {{ num_registros - rawSchema['n_' + elm] }}</span>
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
        <!-- End section SCHEMA -->
        <div :class="section == 'import'? '': 'd-none'">
            <import-basic 
                :destino="fuente" 
                separador_mode="normal" 
                subtitulo="RESERVAS TÉCNICAS - CONTRATOS" 
                separador="|" 
                sindiccionario
                head="file_parse"
                fields="tpp:tipoIdPrestador|idp:idPrestador|nmp:nombrePrestador|pla:planSalud|idc:idContrato|stt:Estado|f1:FIniCon|f2:FFinCon|ids:idServicio|ser:DesServicio|tar:TTarifa|bas:TBase|act:TActual|f3:FIniTar|f4:FFinTar"
                rules=""
                codec_mode="show"
                error="ignore"
                error_mode="show"
                info
                extra
                withperiodo
                realtime
                :clientetx="clientetx">
            </import-basic>
            <div class="my-4"></div>
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <import-list :coleccion="fuente" titulo="BASE DE DATOS DE CONTRATOS"></import-list>
                    </div>
                </div>
            </div>
        </div>
        <local-modal 
            :coleccion="fuente" 
            cantidad="50"
            campos="tpp:tipoIdPrestador,idp:idPrestador,nmp:nombrePrestador,pla:planSalud,idc:idContrato,stt:Estado,f1:FIniCon,f2:FFinCon,ids:idServicio,ser:DesServicio,tar:Ttarifa,bas:Tbase,act:Tactual,f3:FIniTar,f4:FFinTar,crx:PERIODO">
        </local-modal>
    </div>
</template>
<script>
import Counter from './../Contador_light.vue';
import PieChart from './../amcharts/pie.vue';
import BarChart from './../amcharts/bar.vue';
import VBarChart from './../amcharts/bar-vertical.vue';
import Ztime from './../select-periodos.vue';
import Modal from './../modal_table_data.vue';

export default {
    components: {'local-counter': Counter, 'am-pie': PieChart, 'am-bar': BarChart, 'am-ver': VBarChart, 'select-periodo': Ztime, 'local-modal': Modal},
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''},
        cliente: {type: String, default: ''},
        clientetx: {type: String, default: ''},
        urol: {type: String, default: ''},
    },
    data() {
        return {
            tokens: {},
            keycode: '',
            pathsearch: this.pathdata.replace(/dash.*$/i, 'dash/consulta/auto'),
            fuente: (this.cliente == '0')? 'retec_contratos_0': this.cliente + '_retec_contratos',
            krache: 'dash_contrato_' + this.cliente,
            krache_time: 'time_contrato_' + this.cliente,
            section: 'general',
            display: 'chart',       // table | chart
            opt: [
                {'tx': 'General', 'code': 'general'}, 
                {'tx': 'Prestadores', 'code': 'basic'}, 
                // {'tx': 'Detalles', 'code': 'detail'}, 
                // {'tx': 'Consulta', 'code': 'list'}, 
                {'tx': 'Estructura', 'code': 'schema'}, 
                {'tx': 'Importar', 'code': 'import'}
            ],
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            campos: ['tpp', 'idp', 'nmp', 'pla', 'idc', 'stt', 'f1', 'f2', 'ids', 'ser', 'tar', 'bas', 'act', 'f3', 'f4'],
            pairs: {_id:'Total registros', tpp:'tipoIdPrestador', idp:'idPrestador', nmp:'nombrePrestador', pla:'planSalud', idc:'idContrato', stt:'Estado', f1:'FIniCon', f2:'FFinCon', ids:'idServicio', ser:'DesServicio', tar:'Ttarifa', bas:'Tbase', act:'Tactual', f3:'FIniTar', f4:'FFinTar'},
            rawData: null,
            rawSchema: [],
            periodo: 202106,
			datos: [],
            num_registros: -1,
            status: 'ini',
            status_sch: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            pinload: 0,
            porcion: [{'a': 0, 'b': 5, 'per': '0'}, {'a': 5, 'b': 10, 'per': '33%'}, {'a': 10, 'b': 15, 'per': '67%'}, {'per': '100%'}],
            clock: null,
            clock_human: '',
            seg: 0,
            runsearch: false,
        }
    },
    computed: {
        human_period: function(){
            let ym = this.periodo.toString();
            if(ym.length == 6){
                let anio = ym.slice(0, 4);
                let ms = ym.slice(-2);
                return this.meses[ms] + ' de ' + anio;
            }
            return '';
        }
    },
    methods: {
        clock_up: function(){
            if(this.clock != null){
                clearInterval(this.clock);
                this.clock = null;
            }
            this.seg = 0;
            this.clock = setInterval(() => {
                this.seg++;
                this.clock_human = this.getTime();
            }, 1000);
        },
        clock_down: function(){
            if(this.clock != null){
                clearInterval(this.clock);
            }
            this.clock = null;
            this.seg = 0;
        },
        getTime: function(){
            let mn = Math.floor(this.seg / 60).toString().padStart(2, '0');
            let rs = (this.seg % 60).toString().padStart(2, '0');
            return `${mn}:${rs} segundos`
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
        isEmpty: function(arg){
            if([undefined, null, ''].includes(arg)) return true;
            return /^\s*$/.test(arg);
        },
        numformat: function(snum){
            var tm = new String(snum);
            return tm.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        numfixed: function(num, dec=2, always=false){
            if(num % 1){
                return Number.parseFloat(Number.parseFloat(num).toFixed(dec));
            }
            return always? Number.parseFloat(Number.parseFloat(num).toFixed(dec)): num;
        },
        altCss: function(bool, a='', b='d-none'){
            return bool? a: b;
        },
        getPercent: function(num){
            var tm = (num / this.num_registros) * 100;
            if(tm >= 99.9 && tm < 100){
                return 99.99;
            }
            return (tm % 1 == 0)? tm: tm.toFixed(2);
        },
        openModal: function(bool){
            this.$eventBus.$emit('open-modal', {'open': bool});
        },
        setSection: function(arg){
            if(this.status != this.state.LOADING && this.status_sch != this.state.LOADING){
                this.section = arg;
                this.manager();
            }
        },
        loadData: function(arg){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('tema', this.fuente);
                pam.append('periodo', arg);
                this.status = this.state.LOADING;
                axios.post(this.pathdata + '/data', pam).then(res => {
                    this.rawData = (res.data.length > 0)?  res.data[0]: {'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'rs_5': [], 'rs_6': [], 'rs_7': [], 'rs_8': []};
                    registerJSON(this.krache, this.rawData, 'per_' + arg);
                    registerJSON(this.krache, arg, 'lastper');
                    this.writeCards();
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        writeCards: function(){
            // rs_1: Plan salud
            // rs_2: Tipo de prestador
            // rs_3: Estado
            // rs_4: Tbase
            // rs_5: Actual
            // rs_6: Listado (20)
            // rs_8: Ttarifa
            if(this.rawData != null){
                let smx = [{'_id': 'Tarifa base', 'valor': ''}, {'_id': 'Tarifa actual', 'valor': ''}];
                if(this.rawData['rs_4'].length > 0 && this.rawData['rs_5'].length > 0){
                    smx = [{'_id': 'Tarifa base', 'valor': this.rawData['rs_4'][0].suma}, {'_id': 'Tarifa actual', 'valor': this.rawData['rs_5'][0].suma}];
                    this.$refs.contador_2.setValor(this.rawData['rs_4'][0].suma);
                    this.$refs.contador_3.setValor(this.rawData['rs_5'][0].suma);
                    this.$refs.contador_1.setValor(this.rawData['rs_5'][0].alldoc);
                    let actual = parseInt(this.rawData['rs_5'][0].suma);
                    let base = parseInt(this.rawData['rs_4'][0].suma);
                    let diff = (actual / base).toFixed(3);
                    this.$refs.contador_33.setValor(diff);
                }else{
                    this.$refs.contador_1.setValor('');
                    this.$refs.contador_2.setValor('');
                    this.$refs.contador_3.setValor('');
                    this.$refs.contador_33.setValor('');
                }
                this.$refs.table_1.setDatos(this.rawData['rs_1']);
                this.$refs.table_2.setDatos(this.rawData['rs_2']);
                this.$refs.table_3.setDatos(this.rawData['rs_3']);
                this.$refs.table_6.setDatos(this.rawData['rs_6']);
                this.$refs.table_suma.setDatos(smx);
                this.$refs.gp_1.setDatos(this.rawData['rs_1']);
                this.$refs.gp_2.setDatos(this.rawData['rs_2']);
                this.$refs.gp_3.setDatos(this.rawData['rs_3']);
                this.$refs.gp_6.setDatos(this.rawData['rs_6'].sort((a, b) => a.suma - b.suma));
                console.log('marquilla');
                console.log(this.rawData['rs_8']);
                this.$refs.sumas.setDatos(this.rawData['rs_8']);
                this.$refs.contador_4.setValor(this.rawData['rs_7'].length);
            }
        },
        loadSchema: function(tload){
            // facets.unshift("x_id:group:none:1");
            this.pinload = tload;
            if(this.pinload <= 2){
                let lim_a = this.porcion[this.pinload].a;
                let lim_b = this.porcion[this.pinload].b;
                let facets = [];
                let matches = [];
                if(this.pinload == 0){
                    facets = ["x_id:group:none:1"].concat(this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":group:none:1"));
                    matches = this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":" + elm + ":exists:true");
                }else if(this.pinload < 2){
                    facets = this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":group:none:1");
                    matches = this.campos.slice(lim_a, lim_b).map(elm => "x_" + elm + ":" + elm + ":exists:true");
                }else{
                    facets = this.campos.slice(lim_a).map(elm => "x_" + elm + ":group:none:1");
                    matches = this.campos.slice(lim_a).map(elm => "x_" + elm + ":" + elm + ":exists:true");
                }
                var pam = new FormData();
                pam.append('tema', this.fuente);
                pam.append('facets', facets.join('|'));
                pam.append('match', matches.join('|'));
                pam.append('periodo', this.periodo);
                this.status_sch = this.state.LOADING;
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
                    registerJSON(this.krache, this.rawSchema, 'sch_' + this.periodo);
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
        getSchema: function(force=false){
            this.status_sch = this.state.LOADING;
            this.asyncRequest(
                'schema_ctro' + this.periodo,
                res => {
                    console.log('koi');
                    this.rawSchema = res[0];
                    console.log(this.rawSchema);
                    this.num_registros = this.rawSchema.total;
                    this.status_sch = this.state.LOADED;
                },
                this.pathdata + '/schema',
                {'tema': this.fuente, 'periodo': this.periodo},
                true,   // first param
                '',     // kcode param
                force   // force param
            );
        },
        manager: function(force=false){
            // this.rawData = getRegisterJSON(this.krache, 'per_' + this.periodo);
            // if(this.isEmpty(this.rawData)){
            //     this.loadData(this.periodo);
            // }else{
            //     this.writeCards();
            // }
            if('schema' == this.section){
                this.getSchema(force);
            }else{
                this.asyncRequest(
                    'raw_ctro_dat' + this.periodo,
                    res => {
                        this.rawData = (res.length > 0)?  res[0]: {'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'rs_5': [], 'rs_6': [], 'rs_7': []};
                        this.writeCards();
                    },
                    this.pathdata + '/data',
                    {'tema': this.fuente, 'periodo': this.periodo},
                    true,   // first param
                    '',     // kcode param
                    force   // force param
                );
            }
        },
        showRecord: function(field){
            this.$eventBus.$emit('open-modal', {'titulo': 'ESTRUCTURA - CAMPOS NO ENCONTRADOS', 'periodo': this.periodo, 'filtros': field + ':exists:false', 'foco': field});
        },
        asyncRequest: function(consulta, fun, writepath, params, first=true, kcode='', force=false){
            let initial = first;
            if(this.runsearch == false || first == false){
                if(this.runsearch == false && first){
                    this.runsearch = true;
                    this.status = this.state.LOADING;
                    this.clock_up();
                    console.log('Se inicia proceso de asyncRequest!');
                }
                if(force === true){
                    this.keycode = generatorKey();
                    let param = new FormData();
                    param.append('clave', this.keycode);
                    Object.entries(params).forEach(par => param.append(par[0], par[1]));
                    customPostBlind(writepath, param).then(arg => {console.log('Return async write request! (CustomPost)')}).catch(err => {console.log(err)});
                    setTimeout(() => this.asyncRequest(consulta, fun, writepath, {}, false, this.keycode), 4000);
                    // axios.post(writepath, param).then(arg => {console.log('Return async write request!')}).catch(err => {console.log(err)});
                    console.log('Se mandó a crear la consulta mongodb por la fuerza, con la clave: ' + this.keycode);
                }else{
                    let pam = new FormData();
                    pam.append('clave', kcode);
                    pam.append('consulta', consulta);
                    axios.post(this.pathsearch, pam).then(res => {
                        if(res.data.estado == 'void'){
                            if(initial){
                                this.keycode = generatorKey();
                                let param = new FormData();
                                param.append('clave', this.keycode);
                                Object.entries(params).forEach(par => param.append(par[0], par[1]));
                                customPostBlind(writepath, param).then(arg => {console.log('Return async write request! (CustomPost)')}).catch(err => {console.log(err)});
                                setTimeout(() => this.asyncRequest(consulta, fun, writepath, {}, false, this.keycode), 4000);
                                // axios.post(writepath, param).then(arg => {console.log('Return async write request!')}).catch(err => {console.log(err)});
                                console.log('Se mandó a crear la consulta mongodb porque se encontró void, con la clave: ' + this.keycode);
                            }
                        }else if(res.data.estado == 'close'){
                            console.log(`Consulta finalizada, con clave: '${kcode}'`);
                            console.log(res.data);
                            fun(res.data.contenido);
                            this.runsearch = false;
                            this.status = this.state.LOADED;
                            this.clock_down();
                        }else if(res.data.estado == 'failed'){
                            console.log(`La creación de consulta mongo falló, con clave: '${kcode}'`);
                            this.runsearch = false;
                            this.status = this.state.FAILED;
                            this.clock_down();
                        }else{
                            console.log(`El estado de la consulta es: '${res.data.estado}', se verifica dentro de 4 segundos!`);
                            setTimeout(() => this.asyncRequest(consulta, fun, writepath, {}, false, kcode), 4000);
                        }
                    }).catch(err => {
                        console.log(err);
                        console.log(`asyncRequest falló, se verifica dentro de 4 segundos!`);
                        setTimeout(() => this.asyncRequest(consulta, fun, writepath, {}, false, kcode), 4000);
                    });
                }
            }else{
                console.log('Se desechó la invocación de asyncRequest, porque ya hay un hilo ejecutándose!');
            }
        },
        listen: function(){
            this.$eventBus.$on('select-estado', arg => {
                console.log(arg);
                this.$eventBus.$emit('open-modal', {'titulo': 'ESTADO', 'periodo': this.periodo, 'filtros': 'stt:' + arg._id, 'foco': 'stt'});
            });
            this.$eventBus.$on('select-plan', arg => {
                console.log('Evento capturado!');
                console.log(arg);
                this.$eventBus.$emit('open-modal', {'titulo': 'PLAN SALUD', 'periodo': this.periodo, 'filtros': 'pla:' + arg._id, 'foco': 'pla'});
            });
            this.$eventBus.$on('select-tipo', arg => {
                console.log('Evento capturado!');
                console.log(arg);
                this.$eventBus.$emit('open-modal', {'titulo': 'TIPO DE PRESTADOR', 'periodo': this.periodo, 'filtros': 'tpp:' + arg._id, 'foco': 'tpp'});
            });
            this.$eventBus.$on('time-select', obj => {
                this.periodo = obj.periodo;
                this.manager();
            });
            this.$eventBus.$on('time-refresh', bool => {
                // unregisterJSON(this.krache);
                this.manager(true);
                //this.lc_token = this.makeToken();
            });
        }
    },
    mounted() {
        this.listen();
        if(this.urol == 'Consultor'){
            this.opt.pop();
        }
    }
}
</script>
<style>
.text-upper {text-transform: uppercase !important}
.dk-hand {cursor: pointer !important}
.text-bold {font-weight: bold !important}
.component-loading .card-view > div {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .panel-body.vega {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .df-options > a {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
</style>