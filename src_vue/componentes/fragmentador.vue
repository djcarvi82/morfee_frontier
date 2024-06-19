<template>
    <div>
        <!-- <a href="#" class="btn btn-default btn-outline" v-on:click="openModal('all')">Modal all</a> -->
        <div class="btn-group d-flex align-items-end" style="margin-bottom:-1px">
            <span :class="tema == 'contrato'? 'btn bg-white': 'btn bg-inactive'" v-on:click="loadColection('contrato')">Contratos</span>
            <span :class="tema == 'auto'? 'btn bg-white': 'btn bg-inactive'" v-on:click="loadColection('auto')">Autorizaciones</span>
            <span :class="tema == 'factura'? 'btn bg-white': 'btn bg-inactive'" v-on:click="loadColection('factura')">Facturas</span>
            <span :class="tema == 'pago'? 'btn bg-white': 'btn bg-inactive'" v-on:click="loadColection('pago')">Pagos</span>
            <span :class="tema == 'inca'? 'btn bg-white': 'btn bg-inactive'" v-on:click="loadColection('inca')">Incapacidades</span>
        </div>
        <div class="border py-4 px-4 mb-5 bg-white">
            <div class="d-flex align-items-center" v-if="status == state.LOADING && status_save != state.NEXT"><i class="fa fa-spin fa-spinner me-2 fs-4"></i> Cargando datos, espere hasta que termine la operación!</div>
            <div v-else-if="status_save == state.NEXT || status == state.LOADED">
                <table class="table mb-0 table-borderedx">
                    <thead>
                        <tr>
                            <th>Año</th>
                            <th class="text-center" v-for="(elm, i) in filled" :key="i">{{ elm.min }}</th>
                        </tr>
                    </thead>
                    <tbody v-if="periodos.length > 0">
                        <tr v-for="(ani, i) in periodos" :key="i">
                            <td class="text-bold">{{ ani.anio }}</td>
                            <td :class="mes.total == 0? 'text-center': 'text-center hv-candidate'" v-for="(mes, m) in ani.meses" :key="m" v-on:click="openModalCRX(mes.ref, mes.total)">
                                <i class="fa fa-times text-danger fs-5" v-if="mes.total == 0"></i>
                                <span v-else>{{ miles(mes.total) }}</span>
                            </td>
                        </tr>
                    </tbody>
                    <tfoot v-else>
                        <tr>
                            <th colspan="13" class="text-danger">No hay segmentación de los registros en periodos de tiempo!</th>
                        </tr>
                    </tfoot>
                </table>
                <div class="alert alert-success mt-3" v-if="outdata.length == 0">
                    <div class="d-flex">
                        <i class="zmdi zmdi-check me-2"></i>
                        <p>Todos los registros tienen periodo establecido!</p>
                    </div>
                </div>
                <div class="mt-4 border px-2 py-1" style="background:#FAFAFA" v-else>
                    <table class="table my-0">
                        <thead>
                            <tr><th colspan="3">No. DE REGISTROS SIN PERIODO ESTABLECIDO</th></tr>
                            <tr>
                                <th class="colmin py-1">Fecha importación</th>
                                <th class="py-1">No. de registros</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(elm, i) in outdata" :key="i">
                                <td>{{ elm._id }}</td>
                                <td>{{ miles(elm.total) }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="text-center mt-2 mb-3">
                        <button class="btn btn-success" type="button" v-on:click="openModal('all')">
                            <i class="fa fa-calendar fs-3"></i>
                            <div>Establecer periodo</div>
                        </button>
                    </div>
                </div>
                <div class="d-flex align-items-center" v-if="status_save == state.LOADING"><i class="fa fa-spin fa-spinner me-2 fs-4"></i> Estableciendo el periodo de los registros indicados...</div>
                <div class="d-flex align-items-center" v-else-if="status_save == state.NEXT"><i class="fa fa-spin fa-spinner me-2 fs-4"></i> Refrescando datos...</div>
            </div>
        </div>
        <div id="local-modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="display: none;">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header" style="background:#F3F3F3">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h5 class="modal-title">ESTABLECER PERIODO</h5>
                    </div>
                    <div class="modal-body py-4">
                        <div class="form-group" v-if="f_crx != 'void'">
                            <label class="control-label">Periodo seleccionado:</label>
                            <input type="text" class="form-control" disabled :value="f_crx + ' (' + humanCRX(f_crx) + ')'">
                        </div>
                        <div v-else-if="f_fecha == 'all'">
                            <label class="control-label">Registros seleccionados:</label>
                            <div class="alert alert-warning">
                                <p>Todos los registros sin periodo establecido.</p>
                            </div>
                        </div>
                        <div class="form-group" v-else>
                            <label class="control-label">Fecha de importación de registros seleccionados:</label>
                            <input type="text" class="form-control" v-model="f_fecha" disabled>
                        </div>
                        <div class="form-group">
                            <label class="control-label">No. de registros seleccionados:</label>
                            <input type="text" class="form-control" disabled :value="miles(f_cantidad)" v-if="f_crx != 'void'">
                            <input type="text" class="form-control" disabled :value="miles(outdata.reduce((acum, elm) => acum + elm.total, 0))" v-else-if="f_fecha == 'all'">
                            <input type="text" class="form-control" disabled :value="miles(outdata.reduce((acum, elm) => acum + (elm._id == f_fecha? elm.total: 0), 0))" v-else>
                        </div>
                        <div class="form-group">
                            <label class="control-label mb-10">Seleccione el año y el mes:</label>
                            <div class="input-group">
                                <span class="input-group-btn"><button type="button" class="btn btn-default" v-on:click="sumAnio(-1)">-</button></span>
                                <input type="text" class="form-control bg-white text-center" v-model="f_anio" readonly>
                                <span class="input-group-btn"><button type="button" class="btn btn-default" v-on:click="sumAnio(1)">+</button></span>
                            </div>
                            <div class="btn-group btn-group-justified mt-2">
                                <a href="javascript:void(0)" :class="elm.num == f_mes? 'btn btn-success py-2': 'btn btn-default btn-outline py-2'" v-for="(elm, i) in filled" :key="i" v-on:click="f_mes = elm.num">{{ elm.min }}</a>
                            </div>
                        </div>
                        <div class="text-center mt-4">
                            <span class="letter" v-for="(elm, i) in letters()" :key="i">{{ elm }}</span>
                        </div>
                    </div>
                    <div class="modal-footer border-top" style="background:#F5F5F5" v-if="f_crx == 'void'">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Cerrar</button>
                        <button type="button" class="btn btn-danger" :disabled="f_anio == '' || f_mes == ''" v-on:click="saveCRX">Guardar</button>
                    </div>
                    <div class="modal-footer border-top" style="background:#F5F5F5" v-else>
                        <button type="button" class="btn btn-default" data-dismiss="modal">Cerrar</button>
                        <button type="button" class="btn btn-danger" :disabled="(f_crx == `${f_anio}${f_mes}`) || f_anio == '' || f_mes == ''" v-on:click="saveCRX">Cambiar periodo</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Counter from './Contador_light.vue';

export default {
    components: {'local-counter': Counter},
    props: {
        keyref: {type: String, default: ''},
        clientetx: {type: String, default: ''}
    },
    data() {
        return {
            css_basic: 'px-3 slot d-flex align-items-center',
            temas: {'contrato': 'retec_contratos', 'auto': 'retec_autorizacion', 'factura': 'retec_facturas', 'pago': 'retec_pagos', 'inca': 'retec_incapacidades'},
            tema: '',
            year: 0,
            tablas: [],
            tabla: null,
            periodos: [],
            outdata: [],
            f_fecha: '',
            f_anio: '',
            f_mes: '',
            f_crx: 'void',
            f_cantidad: 0,
            filled: [
                {'tx': 'Enero', 'min': 'Ene', 'num': '01', 'total': 0}, 
                {'tx': 'Febrero', 'min': 'Feb', 'num': '02', 'total': 0},
                {'tx': 'Marzo', 'min': 'Mar', 'num': '03', 'total': 0},
                {'tx': 'Abril', 'min': 'Abr', 'num': '04', 'total': 0},
                {'tx': 'Mayo', 'min': 'May', 'num': '05', 'total': 0},
                {'tx': 'Junio', 'min': 'Jun', 'num': '06', 'total': 0},
                {'tx': 'Julio', 'min': 'Jul', 'num': '07', 'total': 0},
                {'tx': 'Agosto', 'min': 'Ago', 'num': '08', 'total': 0},
                {'tx': 'Septiembre', 'min': 'Sep', 'num': '09', 'total': 0},
                {'tx': 'Octubre', 'min': 'Oct', 'num': '10', 'total': 0},
                {'tx': 'Noviembre', 'min': 'Nov', 'num': '11', 'total': 0},
                {'tx': 'Diciembre', 'min': 'Dic', 'num': '12', 'total': 0}
            ],
            status: 'ini',
            status_save: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'NEXT': 'next', 'FAILED': 'failed'}
        }
    },
    methods: {
        miles: function(snum){
            var tm = new String(snum);
            return tm.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        sumAnio: function(num){
            var tm = parseInt(this.f_anio) + num;
            this.f_anio = tm.toString();
            this.f_mes = '';
        },
        getTema: function(tem){
            return this.temas[tem];
        },
        letters: function(){
            var tm = `${this.f_anio}${this.f_mes}  `;
            return tm.split('').slice(0, 6);
        },
        humanCRX: function(per){
            var tm = per.toString().slice(-2);
            var rs = this.filled.reduce((acum, elm) => elm.num == tm? elm.tx: acum, 'Sin encontrar');
            return (rs == 'Sin encontrar')? rs: rs + ' de ' + this.f_anio;
        },
        loadPredata: function(){
            var params = new FormData();
            params.append('keyref', this.keyref);
            params.append('modulo', 'retec');
            axios.post(root_path + 'diccionario/cliente', params).then(res => {
                this.tablas = res.data;
            }).catch(err => {console.log(err)});
        },
        loadPeriodos: function(arg){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                var pam = new FormData();
                pam.append('tema', arg);
                axios.post(root_path + 'reservas/info/periodos', pam).then(res => {
                    // this.outdata = res.data[0].sonei;
                    this.outdata = [];
                    let tmp = [];
                    res.data[0].saved.forEach(elm => {
                        if(elm._id == null){
                            this.outdata.push({'_id': 'Sin periodo', 'total': elm.total});
                        }else{
                            tmp.push(elm);
                        }
                    });
                    this.extractPeriodos(tmp);
                    this.status = this.state.LOADED;
                    if(this.status_save == this.state.NEXT){
                        this.status_save = this.state.LOADED;
                    }
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        extractPeriodos: function(arr){
            var tmp = {};
            arr.forEach(elm => {
                var raw = elm._id.toString();
                var anio = raw.slice(0, 4);
                var mes = parseInt(raw.slice(-2));
                if(tmp[anio] == undefined){
                    tmp[anio] = {'anio': anio, 'meses': []};
                    tmp[anio].meses = this.filled.map(dato => {
                        var ref = parseInt(anio + dato.num);
                        return {'ref': ref, 'hasData': false, 'total': 0};
                    });
                }
                for(var i = 0; i < 12; i++){
                    if(tmp[anio].meses[i].ref == elm._id){
                        tmp[anio].meses[i].hasData = true;
                        tmp[anio].meses[i].total = elm.total;
                        break;
                    }
                }
            });
            this.periodos = Object.values(tmp);
        },
        loadColection: function(tem){
            if(this.status != this.state.LOADING && this.status_save != this.state.LOADING){
                this.tema = tem;
                this.loadPeriodos(this.getTema(tem));
            }
        },
        isTargetTable: function(arg){
            return (this.tabla != null && this.tabla.id == arg);
        },
        getStoreData: function(name, fun=null){
            if(localStorage.getItem(name) == null || localStorage.getItem == undefined){
                fun();
            }else{
                return localStorage.getItem(name);
            }
        },
        openModal: function(arg){
            this.f_crx = 'void';
            this.f_fecha = arg;
            this.f_anio = this.year.toString();
            this.f_mes = '';
            $('#local-modal').modal('show');
        },
        openModalCRX: function(per, tot){
            if(tot != 0){
                this.f_crx = per.toString();
                this.f_cantidad = tot;
                this.f_fecha = '';
                this.f_anio = this.f_crx.slice(0, 4);
                this.f_mes = this.f_crx.slice(-2);
                $('#local-modal').modal('show');
            }
        },
        saveCRX: function(){
            if((this.f_crx != 'void' || this.f_fecha != '') && this.f_anio != '' && this.f_mes != ''){
                var periodo = `${this.f_anio}${this.f_mes}`;
                var pam = new FormData();
                pam.append('tema', this.temas[this.tema]);
                pam.append('fecha', this.f_fecha);
                pam.append('periodo', periodo);
                pam.append('crx', this.f_crx);
                this.status_save = this.state.LOADING;
                axios.post(root_path + 'reservas/mng/fixed/crx', pam).then(res => {
                    this.status_save = this.state.NEXT;
                    this.loadColection(this.tema);
                }).catch(err => {
                    console.log('Failed update many');
                    this.status_save = this.state.FAILED;
                    console.log(err);
                });
                $('#local-modal').modal('hide');
            }
        }
        // function getResult(){
        //     if(localStorage.getItem('aut_dash') == null){
        //         loadDash();
        //     }else{
        //         console.log('Recuperado');
        //         var tmp = localStorage.getItem('aut_dash');
        //         result = JSON.parse(tmp);
        //         drawGraphics();
        //     }
        // }
    },
    mounted() {
        this.year = (new Date()).getFullYear();
        this.f_anio = this.year.toString();
        ['contrato', 'auto', 'factura', 'pago', 'inca'].forEach(elm => {
            // this.temas[elm] = '7_' + this.temas[elm];
            if(this.keyref == '0' || this.keyref == 0){
                this.temas[elm] += '_' + this.keyref;
            }else{
                this.temas[elm] = this.keyref + '_' + this.temas[elm];
            }
        });
        this.tema = 'contrato';
        // this.loadPredata();
        this.loadColection(this.tema);
    }
}
</script>
<style scoped>
.colmin {width: 1%; white-space: nowrap; text-align: center}
.slot {border-top:1px solid #DDD; padding-top:.65rem; padding-bottom: .65rem; cursor:pointer; user-select: none}
.slot.slot-active {background: linear-gradient(#FFF8E4, #FFEAAB, #FFF8E4); border-top-color:#FFD968 !important; border-bottom-color:#FFD968 !important}
.slot.slot-active + .slot {border-top-color:#FFD968 !important}
.slot.slot-active > * {color:#000 !important; font-weight: bold}
.bg-custom-green {background:#2ECD99; color:#FFF; border-top:1px solid #FFF; border-bottom:1px solid #FFF}
.text-focus {font-weight: bold; color:#3273DC; text-transform: uppercase}
.table thead th {font-weight: bold}
.bg-white {background: #FFF}
.btn-group > span.btn.bg-white {color:#000; border-left:1px solid #DEE2E6 !important; border-top:1px solid #DEE2E6 !important; border-right:1px solid #DEE2E6 !important}
.bg-inactive {background: #EDEDED}
.btn-group > span.btn.bg-inactive {color:#919191; border-top:1px solid #DEE2E6 !important}
.btn-group > span.btn:last-child {border-right:1px solid #DEE2E6 !important}
.btn-group > span.btn.bg-inactive + .bg-inactive {border-left:1px solid #CDD2D6 !important}
.control-label {text-transform: lowercase}
.control-label::first-letter {text-transform: uppercase}
.letter {display: inline-block; width: 2rem; height: 2rem;  font-size: 1.3rem; border:1px solid #2ECD99; text-align: center; vertical-align: middle}
.letter + .letter {margin-left:4px}
.letter:empty {background: #FF000033}
.hv-candidate:hover {background:#E3F0D6; color:#000; cursor:pointer}
.text-bold {font-weight: bold;}
</style>