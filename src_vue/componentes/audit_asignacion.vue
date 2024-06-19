<template>
    <div>
        <div class="d-flex justify-content-betweenx mb-4">
            <a :class="section == 'visual'? 'flex-fillx bg-target': 'flex-fillx bg-custom'" href="javascript:void(0)" v-on:click="section = 'visual'">
                <div class="d-flex align-items-center">
                    <span class="lc-icon d-flex align-items-center justify-content-center me-2"><i class="fa fa-bar-chart-o"></i></span>
                    <span>Visual</span>
                </div>
            </a>
            <a :class="section == 'search'? 'flex-fillx bg-target': 'flex-fillx bg-custom'" href="javascript:void(0)" v-on:click="section = 'search'">
                <div class="d-flex align-items-center">
                    <span class="lc-icon d-flex align-items-center justify-content-center me-2"><i class="fa fa-search"></i></span>
                    <span>Búsqueda</span>
                </div>
            </a>
        </div>
        <div :class="section == 'visual'? '': 'd-none'">
            <div :class="display == 'general'? '': 'd-none'">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-end">
                            <a href="javascript:void(0)" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="row">
                                <div class="col-sm-6">
                                    <h6 class="fs-5 mb-4 text-center">ESTADO GENERAL DE LA ASIGNACIÓN</h6>
                                    <am-pie 
                                        ref="g_global" 
                                        paleta="#5470C5,#86BD6C,#FAC858,#EE6666,#73C0DE,#3BA272,#FC8452,#9A60B4" 
                                        campo_categoria="_id" campo_valor="total" campo_color="color"
                                        altura="450" 
                                        etiquetas 
                                        lanzarevento="open-distri" 
                                        radio="60"
                                        totalizar="28|Total facturas|12"
                                        leyenda="bottom"></am-pie>
                                </div>
                                <div class="col-sm-6">
                                    <h6 class="fs-5 mb-4 text-center">ASIGNACIÓN DE FACTURAS</h6>
                                    <am-pie 
                                        ref="g_asign" 
                                        paleta="#5470C5,#86BD6C,#FAC858,#EE6666,#73C0DE,#3BA272,#FC8452,#9A60B4" 
                                        campo_categoria="_id" campo_valor="total" 
                                        altura="450" 
                                        etiquetas="value" 
                                        grilla="0" 
                                        tooltip 
                                        lanzarevento="open-distri" 
                                        leyenda="right" 
                                        compact
                                        label_alignx></am-pie>
                                </div>
                            </div>
                            <div v-if="latest.status != 'ini'">
                                <div class="border-bottom mt-4 mb-2"></div>
                                <p class="mt-0 mb-0 py-0" style="font-size:.8rem; color:#444; line-height:1rem">Fecha de última actualización: <strong>{{ latest.update }}</strong></p>
                                <p class="mt-0 mb-0 py-0" style="font-size:.8rem; color:#444; line-height:1rem">Total registros última actualización: <strong>{{ formatMiles(latest.total) }}</strong></p>
                            </div>

                            <am-bar class="d-none" ref="g_asignx" campo_categoria="_id" campo_valor="total" altura="250" etiquetas grilla="0" sin_valores tooltip cursor lanzarevento="open-distri"></am-bar>
                        </div>
                    </div>
                </div>
                <div :class="status_fec == state.LOADING? 'panel panel-default card-view border': 'd-none'">
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="d-flex align-items-center justify-content-center">
                                <i class="fa fa-spinner fa-spin me-2 fs-4"></i>
                                <span>Cargando facturas...</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div :class="status_fec == state.LOADED? 'panel panel-default card-view border': 'd-glass'">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title fs-5 text-center" v-if="f_tecnico == ''">Número de facturas sin asignar según vencimiento a los 20 días</h6>
                            <h6 class="panel-title fs-5 text-center" v-else>Número de facturas asignadas a <span class="txt-primary">{{ f_tecnico == '-alltec-'? 'TODOS LOS TÉCNICOS': f_tecnico }}</span></h6>
                            <a href="javascript:void(0)" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <am-line 
                                ref="g_line" 
                                campo_categoria="fecha" 
                                campo_valor="total" 
                                altura="230" 
                                sin_valores 
                                puntos 
                                etiquetas 
                                cursor 
                                paleta="2" 
                                grosor="2" 
                                min="0"
                                lanzarevento="open-point" 
                                procesar_fechas></am-line>
                        </div>
                    </div>
                </div>
            </div>
            <!-- End display general -->
            <div :class="display == 'factura'? '': 'd-none'">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title fs-5" v-if="f_tecnico == ''">FACTURAS SIN ASIGNAR ({{ facturas.length }})</h6>
                                <h6 class="panel-title fs-5" v-else>FACTURAS ASIGNADAS A <span class="txt-primary">{{ f_tecnico == '-alltec-'? 'TODOS LOS TÉCNICOS': f_tecnico }}</span> ({{ facturas.length }})</h6>
                                <p class="mb-0">Fecha límite: {{ f_fecha }}</p>
                            </div>
                            <a href="javascript:void(0)" data-effect="fadeOut" v-on:click="setDisplay('general')">
                                <i class="zmdi zmdi-close"></i>
                            </a>                        
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <ul role="tablist" class="nav nav-tabs">
                                <li :class="vista == 'speed'? 'active': ''"><a data-toggle="tab" role="tab" href="javascript:void(0)" v-on:click="vista = 'speed'">Vista rápida</a></li>
                                <li :class="vista == 'detail'? 'active': ''"><a  data-toggle="tab" role="tab" href="javascript:void(0)" v-on:click="vista = 'detail'">Vista detallada</a></li>
                            </ul>
                            <div v-if="vista == 'speed'">
                                <div class="table-wrap">
                                    <div class="table-responsive">
                                        <table class="table table-hover mb-0x">
                                            <thead>
                                                <tr>
                                                    <th class="colmin">No.</th>
                                                    <th>Razón social</th>
                                                    <th class="colmin">Factura</th>
                                                    <th class="colmin">Fecha radicado</th>
                                                    <th class="colmin">Límite para auditar</th>
                                                    <th>Usuario aud. técnica</th>
                                                    <th>Usuario aud. médica</th>
                                                    <th class="colmin">Est. Aud. técnica</th>
                                                    <th class="colmin">Est. Aud. Médica</th>
                                                    <th class="colmin">Est. conciliación</th>
                                                    <th class="colmin">Neto</th>
                                                    <!-- <th class="colmin">Consecutivo</th>
                                                    <th class="colmi">Usuario que radica</th> -->
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="(elm, i) in facturas" :key="i" v-on:click="setFactura(elm, i)">
                                                    <td class="py-2 text-center">{{ i + 1 }}</td>
                                                    <td class="py-2">{{ elm.razon_social }}</td>
                                                    <td class="py-2">{{ elm.factura }}</td>
                                                    <td class="py-2">{{ elm.fecha_radicado }}</td>
                                                    <td class="py-2 colmin"><span :class="hasTimeFree(addDaysAlt20(elm.fecha_radicado))? 'label label-success px-3': 'label label-danger px-3'">{{ addDaysAlt20(elm.fecha_radicado) }}</span></td>
                                                    <td class="py-2">{{ elm.usuario_auditoria_tecnica }}</td>
                                                    <td class="py-2">{{ elm.usuario_auditoria_medica }}</td>
                                                    <td class="py-2">{{ elm.estado_tecnica }}</td>
                                                    <td class="py-2">{{ elm.estado_medica }}</td>
                                                    <td class="py-2">{{ elm.estado_factura_conciliacion }}</td>
                                                    <td class="py-2 text-right">{{ formatMiles(elm.valor_neto) }}</td>
                                                    <!-- <td class="py-2">{{ elm.consecutivo_radica }}</td>
                                                    <td class="py-2">{{ elm.usuario_radica }}</td> -->
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>                        
                            </div><!-- End view speed -->
                            <div v-if="vista == 'detail'">
                                <div class="row mt-4">
                                    <div class="col-sm-3">
                                        <div class="form-group mb-0">
                                            <label class="control-label">Estado técnica</label>
                                            <select class="form-control" v-model="fil_tec">
                                                <option value=""></option>
                                                <option v-for="(elm, i) in fil_tec_opt" :key="i" :value="elm">{{ elm }}</option>
                                            </select>
                                        </div>
                                        <!-- <div class="form-group mb-0">
                                            <label class="control-label">Estado técnica</label>
                                            <div class="input-group">
                                                <input type="text" class="form-control" autocomplete="off">
                                                <span class="input-group-btn">
                                                    <button class="btn btn-success" type="button"><i class="fa fa-search"></i></button>
                                                </span>
                                            </div>
                                        </div> -->
                                    </div>
                                </div>
                                <div class="table-wrap">
                                    <div class="table-responsive">
                                        <table class="table table-hover mb-0x" v-if="vista == 'detail'">
                                            <thead>
                                                <tr>
                                                    <th class="colmin">No.</th>
                                                    <th>Fecha rad.</th>
                                                    <th>Límite 20 días</th>
                                                    <th>Conse. rad.</th>
                                                    <th>Factura</th>
                                                    <th>Valor neto</th>
                                                    <th>Usuario aud. técnica</th>
                                                    <th>Usuario aud. médica</th>
                                                    <th>Estado técnica</th>
                                                    <th>Estado médica</th>
                                                    <th>NIT</th>
                                                    <th>Razón Social</th>
                                                    <th>Número contrato</th>
                                                    <th>Tipo contrato</th>
                                                    <th>Modalidad</th>
                                                    <th>Total glosa</th>
                                                    <!-- <th class="text-center">Acción</th> -->
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr v-for="(elm, i) in getFacturas()" :key="i" v-on:click="setFactura(elm)">
                                                    <td class="py-2 text-center">{{ i + 1 }}</td>
                                                    <td class="py-2 colmin">{{ elm.fecha_radicado }}</td>
                                                    <td class="py-2 colmin"><span :class="hasTimeFree(addDaysAlt20(elm.fecha_radicado))? 'label label-success px-3': 'label label-danger px-3'">{{ addDaysAlt20(elm.fecha_radicado) }}</span></td>
                                                    <td class="py-2">{{ elm.consecutivo_radica }}</td>
                                                    <td class="py-2">{{ elm.factura }}</td>
                                                    <td class="py-2">{{ formatMiles(elm.valor_neto) }}</td>
                                                    <td class="py-2">{{ elm.usuario_auditoria_tecnica }}</td>
                                                    <td class="py-2">{{ elm.usuario_auditoria_medica }}</td>
                                                    <td class="py-2">{{ elm.estado_tecnica }}</td>
                                                    <td class="py-2">{{ elm.estado_medica }}</td>
                                                    <td class="py-2">{{ elm.nit }}</td>
                                                    <td class="py-2">{{ elm.razon_social }}</td>
                                                    <td class="py-2">{{ elm.numero_contrato }}</td>
                                                    <td class="py-2">{{ elm.tipo_contrato }}</td>
                                                    <td class="py-2">{{ elm.modalidad_contrato }}</td>
                                                    <td class="py-2">{{ elm.total_glosas }}</td>
                                                    <!-- <td class="py-2"></td> -->
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <!-- End view detail -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'search'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <h6 class="panel-title txt-dark">BÚSQUEDA DE FACTURAS</h6>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="border pt-2 px-3 bg-custom-grey" >
                            <div class="row">
                                <div class="col-sm-3">
                                    <div class="form-group">
                                        <label class="control-label">Número de contrato:</label>
                                        <input type="text" class="form-control" v-model="s_contrato">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="form-group">
                                        <label class="control-label">No. Factura:</label>
                                        <input type="text" class="form-control" v-model="s_factura">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="form-group">
                                        <label class="control-label">Razón Social:</label>
                                        <input type="text" class="form-control" v-model="s_razon">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="form-group">
                                        <label class="control-label">&nbsp;</label>
                                        <button type="button" class="btn btn-success btn-block" v-on:click="loadSearch">Buscar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <!-- End form grey -->
                        <div class="border-bottom mb-3"></div>
                        <div class="table-wrap">
                            <div class="table-responsive">
                                <table class="table table-hover mb-0">
                                    <thead>
                                        <tr>
                                            <th class="colmin">No.</th>
                                            <th>Fecha rad.</th>
                                            <th>Límite 20 días</th>
                                            <th>Conse. rad.</th>
                                            <th>Factura</th>
                                            <th>Valor neto</th>
                                            <th>Usuario aud. técnica</th>
                                            <th>Usuario aud. médica</th>
                                            <th>Estado técnica</th>
                                            <th>Estado médica</th>
                                            <th>NIT</th>
                                            <th>Razón Social</th>
                                            <th>Número contrato</th>
                                            <th>Tipo contrato</th>
                                            <th>Modalidad</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(elm, i) in search_data" :key="i">
                                            <td class="py-2 text-center">{{ i + 1 }}</td>
                                            <td class="py-2 colmin">{{ elm.fecha_radicado }}</td>
                                            <td class="py-2 colmin"><span :class="hasTimeFree(addDaysAlt20(elm.fecha_radicado))? 'label label-success px-3': 'label label-danger px-3'">{{ addDaysAlt20(elm.fecha_radicado) }}</span></td>
                                            <td class="py-2">{{ elm.consecutivo_radica }}</td>
                                            <td class="py-2">{{ elm.factura }}</td>
                                            <td class="py-2">{{ formatMiles(elm.valor_neto) }}</td>
                                            <td class="py-2">{{ elm.usuario_auditoria_tecnica }}</td>
                                            <td class="py-2">{{ elm.usuario_auditoria_medica }}</td>
                                            <td class="py-2">{{ elm.estado_tecnica }}</td>
                                            <td class="py-2">{{ elm.estado_medica }}</td>
                                            <td class="py-2">{{ elm.nit }}</td>
                                            <td class="py-2">{{ elm.razon_social }}</td>
                                            <td class="py-2">{{ elm.numero_contrato }}</td>
                                            <td class="py-2">{{ elm.tipo_contrato }}</td>
                                            <td class="py-2">{{ elm.modalidad_contrato }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <!-- End panel-body -->
                </div>
            </div>
        </div>
        <!-- End display factura -->
        <div id="audit-asign-modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h5 class="modal-title">Asignar auditor técnico</h5>
                    </div>
                    <div class="modal-body" v-if="factura != null">
                        <div class="border mb-4" style="background:#FAFAFA">
                            <div class="d-flex justify-content-between py-1 px-3">
                                <div>No. Factura</div>
                                <div class="txt-dark">{{ factura.factura }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-1 px-3 border-top">
                                <div>Consecutivo radicado</div>
                                <div class="txt-dark">{{ factura.consecutivo_radica }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-1 px-3 border-top">
                                <div>Razón Social</div>
                                <div class="txt-dark">{{ factura.razon_social }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-1 px-3 border-top">
                                <div>NIT</div>
                                <div class="txt-dark">{{ factura.nit }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-1 px-3 border-top">
                                <div>No. de contrato</div>
                                <div class="txt-dark">{{ factura.numero_contrato }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-1 px-3 border-top">
                                <div>Tipo contrato</div>
                                <div class="txt-dark">{{ factura.tipo_contrato }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-1 px-3 border-top">
                                <div>Valor neto</div>
                                <div class="txt-dark">{{ factura.valor_neto }}</div>
                            </div>

                        </div>
                        <form>
                            <div class="form-group">
                                <label for="recipient-name" class="control-label mb-10">Usuario para auditoría técnica:</label>
                                <input type="text" class="form-control" v-model="f_user_pretend">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-danger" v-on:click="saveAssignOne">Guardar cambios</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- End modal -->
    </div>
</template>
<script>
import PieChart from './amcharts/pie.vue';
import BarChart from './amcharts/bar.vue';
import LineChart from './amcharts/line.vue';
import VerticalChart from './amcharts/bar-vertical.vue';

export default {
    components: {'am-pie': PieChart, 'am-bar': BarChart, 'am-ver': VerticalChart, 'am-line': LineChart},
    data() {
        return {
            section: 'visual',      // visual | search
            display: 'general',     // general | factura
            vista: 'detail',        // speed | detail
            num_today: 0,
            latest: {'status': 'ini'},
            anios: {},
            festivos: {'2022-01-10': true, '2022-03-21': true, '2022-04-14': true, '2022-04-15': true, '2022-05-30': true, '2022-06-20': true, '2022-06-27': true, '2022-07-04': true, '2022-07-20': true, '2022-08-15': true, '2022-10-17': true, '2022-11-07': true, '2022-11-14': true, '2022-12-08': true, '2023-01-09': true, '2023-03-20': true, '2023-04-06': true, '2023-04-07': true, '2023-05-01': true, '2023-05-22': true, '2023-06-12': true, '2023-06-19': true, '2023-07-03': true, '2023-07-20': true, '2023-08-07': true, '2023-08-21': true, '2023-10-16': true, '2023-11-06': true, '2023-11-13': true, '2023-12-08': true, '2023-12-25': true},
            after20: {},
            data_root: [],
            users: [],
            fechas: [],
            facturas: [],
            factura: null,
            search_data: [],
            fil_tec_opt: [],
            fil_tec: '',
            indice: -1,
            f_tecnico: '',
            f_fecha: '',
            f_user_pretend: '',
            s_contrato: '',
            s_factura: '',
            s_razon: '',
            has_change: false,
            status: 'ini',
            status_fec: 'ini',
            status_fac: 'ini',
            status_gru: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
        }
    },
    methods: {
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        isEmpty: function(a){
            return (a == "" || a == undefined || a == null)? true: false;
        },
        toNumber: function(tx){
            return this.isEmpty(tx)? 0: parseFloat(tx);
        },
        setDisplay: function(arg){
            this.display = arg;
            if(this.display == 'general' && this.has_change){
                this.loadAsign();
            }
        },
        altCss: function(bool, a='', b='d-none'){
            return bool? a: b;
        },
        addDays20: function(ymd){
            if(this.after20[ymd] == undefined){
                let axu = [26, 28, 28, 28, 28, 28, 27];
                let yin = ymd.toString().split('-').map(num => parseInt(num));
                let fec = new Date(yin[0], yin[1] - 1, yin[2]);
                let days = yin[2] + axu[fec.getDay()];
                fec.setDate(days);
                this.after20[ymd] = [fec.getFullYear(), fec.getMonth() + 1, fec.getDate()].map(num => num < 10? `0${num}`: num).join('-');
            }
            return this.after20[ymd];
        },
        loadLastImport: function(){
            let pam = new FormData();
            pam.append('coleccion', 'audit_facturas_0');
            axios.post(root_path + 'users/admin/last/import', pam).then(res => {
                if(res.data.status == 'success'){
                    this.latest = {'update': res.data.fecha, 'total': res.data.total, 'status': 'success'};
                }else if(res.data.status == 'empty'){
                    this.latest = {'update': res.data.fecha, 'total': res.data.total, 'status': 'empty'};
                }
            }).catch(err => {
                console.log('Error generate!');
                console.log(err);
            });
        },
        loadAsign: function(){
            axios.post(root_path + 'auditorias/vue/facturas/asignacion').then(res => {
                let tm = {};
                this.users = res.data;
                this.$refs.g_asign.setDatos(this.users.map(elm => {
                    if(elm._id == ''){
                        if(tm.orphan == undefined) tm.orphan = {'_id': 'Sin asignar', 'total': 0, 'color': '#EB4747', 'grupo': elm._id};
                        tm.orphan.total += elm.total;
                    }else{
                        if(tm.data == undefined) tm.data = {'_id': 'Asignadas', 'total': 0, 'color': '#5B9F3B', 'grupo': elm._id};
                        tm.data.total += elm.total;
                    }
                    return {'_id': (elm._id == '')? 'Sin asignar': elm._id, 'total': elm.total, 'grupo': elm._id}
                }).filter(elm => elm._id != 'Sin asignar'));
                this.data_root = Object.values(tm);
                this.$refs.g_global.setDatos(this.data_root);
                this.has_change = false;
            }).catch(err => {console.log(err)});
        },
        loadStatus: function(arg){  // Function deprecada (no invoke)
            let pam = new FormData();
            pam.append('item', 'estados');
            pam.append('tecnico', arg);
            axios.post(root_path + 'auditorias/vue/facturas/asignacion', pam).then(res => {
                console.log(res.data);
                // this.users = res.data;
                // this.$refs.g_asign.setDatos(this.users.map(elm => {
                //     return {'_id': (elm._id == '')? 'Sin asignar': elm._id, 'total': elm.total}
                // }));
            }).catch(err => {console.log(err)});
        },
        loadFechas: function(tec){
            let pam = new FormData();
            pam.append('item', 'fechas');
            pam.append('tecnico', tec);
            this.status_fec = this.state.LOADING;
            this.fechas = [];
            axios.post(root_path + 'auditorias/vue/facturas/asignacion', pam).then(res => {
                let blk = {};
                let tmr = res.data[0].puntos.map(elm => {
                    elm.fecha = this.addDaysAlt20(elm._id);
                    return elm;
                });
                tmr.forEach(elm => {
                    if(blk[elm.fecha] == undefined){
                        blk[elm.fecha] = {'fecha': elm.fecha, 'total': 0, 'origen': []};
                    }
                    blk[elm.fecha].total += elm.total;
                    blk[elm.fecha].origen.push(elm._id);
                });
                this.fechas = Object.values(blk);
                this.$refs.g_line.setDatos(this.fechas);
                this.status_fec = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status_fec = this.state.FAILED;
            });
        },
        loadPoint: function(fecha){
            this.facturas = [];
            this.fil_tec_opt = [];
            this.fil_tec = '';
            let pam = new FormData();
            pam.append('item', 'facturas');
            pam.append('tecnico', this.f_tecnico);
            pam.append('fecha', fecha);
            this.status_fac = this.state.LOADING;
            this.display = 'factura';
            let tmp = {};
            axios.post(root_path + 'auditorias/vue/facturas/asignacion', pam).then(res => {
                this.facturas = res.data;
                res.data.forEach(elm => tmp[elm.estado_tecnica] = '');
                this.fil_tec_opt = Object.keys(tmp).sort();
                // this.grupo = res.data;
                this.status_fac = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status_fac = this.state.FAILED;
            });
        },
        loadSearch: function(){
            if(!this.isEmpty(this.s_contrato) || !this.isEmpty(this.s_factura) || !this.isEmpty(this.s_razon)){
                let pam = new FormData();
                pam.append('item', 'search');
                if(!this.isEmpty(this.s_contrato)){
                    pam.append('contrato', this.s_contrato);
                }
                if(!this.isEmpty(this.s_factura)){
                    pam.append('factura', this.s_factura);
                }
                if(!this.isEmpty(this.s_razon)){
                    pam.append('rsocial', this.s_razon);
                }
                axios.post(root_path + 'auditorias/vue/facturas/asignacion', pam).then(res => {
                    this.search_data = res.data;
                }).catch(err => {
                    console.log(err);
                });
            }
        },
        setFactura: function(fac, ind){
            this.indice = ind;
            this.factura = fac;
            this.f_user_pretend = this.factura.usuario_auditoria_tecnica;
            $('#audit-asign-modal').modal('show');
        },
        getFacturas: function(){
            return this.fil_tec == ''? this.facturas: this.facturas.filter(elm => elm.estado_tecnica == this.fil_tec);
        },
        saveAssignOne: function(){
            let pam = new FormData();
            pam.append('oid', this.factura._id.$oid);
            pam.append('tecnico', this.f_user_pretend);
            axios.post(root_path + 'auditorias/vue/factura/edit/one', pam).then(res => {
                if(res.data.status == 'success'){
                    if(this.facturas[this.indice]._id.$oid == this.factura._id.$oid){
                        this.facturas[this.indice].usuario_auditoria_tecnica = this.f_user_pretend;
                    }
                    this.has_change = true;
                }
                $('#audit-asign-modal').modal('hide');
            }).catch(err => {
                console.log(err);
                $('#audit-asign-modal').modal('hide');
            });
        },
        hasTimeFree: function(ymd){
            let num = parseInt(ymd.toString().replaceAll('-', ''));
            return (num > this.num_today)? true: false;
        },
		makeTimer: function(vige){
			let tmr = [];
			for(var i = 0; i < 12; i++){
				var fc = new Date(vige, i, 1);
                tmr.push({'m': i + 1, 'f': 1, 't': (new Date(vige, i + 1, 0)).getDate(), 'd': fc.getDay()});
			}
			return tmr;
		},
        fillAnio: function(year){
            if(this.anios[year] == undefined){
                this.anios[year] = [];
                // {'ymd': '2022-01-01', 'd': 6, 'fes': true},
                this.makeTimer(year).forEach(elm => {
                    let di = elm.d;
                    for(let i = 1; i <= elm.t; i++){
                        let ymd = year + '-' + this.leftZero(elm.m, 2) + '-' + this.leftZero(i, 2);
                        this.anios[year].push({'ymd': ymd, 'd': di, 'fes': this.isFestivo(di, ymd)});
                        di = (di == 6)? 0: di + 1;
                    }
                });
            }
        },
        leftZero: function(num, len){
            return num.toString().padStart(len, '0');
        },
        isFestivo: function(day, fecha){
            if(day % 6 == 0){   // Day 0 or 6 is festivo!
                return true;
            }
            return (this.festivos[fecha] === true);
        },
        addDaysAlt20: function(fecha){
            if(this.after20[fecha] == undefined){
                let year = fecha.slice(0, 4);
                if(this.anios[year] == undefined) this.fillAnio(year);
                let ini = this.anios[year].findIndex(elm => elm['ymd'] == fecha);
                if(ini == -1){
                    return fecha;
                }
                let count = 0;
                let date = '';
                for(let i = ini; i < this.anios[year].length; i++){
                    if(i > ini && this.anios[year][i].fes == false){
                        count++;
                    }
                    if(count == 20){
                        date = this.anios[year][i].ymd;
                        break;
                    }
                }
                if(count < 20){
                    let nextYear = (parseInt(year) + 1).toString();
                    if(this.anios[nextYear] == undefined) this.fillAnio(nextYear);
                    for(let k = 0; k < this.anios[nextYear].length; k++){
                        if(this.anios[nextYear][k].fes == false){
                            count++;
                        }
                        if(count == 20){
                            date = this.anios[nextYear][k].ymd;
                            break;
                        }
                    }
                }
                this.after20[fecha] = date;
            }
            return this.after20[fecha];
        },
        listen: function(){
            this.$eventBus.$on('open-distri', arg => {
                this.f_tecnico = arg._id == 'Sin asignar'? '': arg._id;
                if(arg._id == 'Asignadas') this.f_tecnico = '-alltec-';
                this.loadFechas(this.f_tecnico);
            });
            this.$eventBus.$on('open-point', arg => {
                this.f_fecha = arg.fecha;
                this.loadPoint(arg.origen.join('|'));
            });
        }
    },
    mounted() {
        this.num_today = parseInt((new Date()).toISOString().slice(0, 10).replaceAll('-', ''));
        this.listen();
        // this.loadFacturacion();
        this.loadLastImport();
        this.loadAsign();
        this.fillAnio(new Date().getFullYear());
    }
}
</script>
<style scoped>
    .nav.nav-tabs > li.active > a {background:#2ECD99; color:#FFF}
    .colmin {width:1%; white-space: nowrap; text-align: center}
    .bg-target {cursor:pointer; background:#F0C541; padding:14px 20px; color:#FFF}
    .bg-target:hover {color:#FFF}
    .bg-custom {cursor:pointer; background:#DEDEDE; padding:14px 20px}
    .bg-custom + .bg-custom {border-left:1px solid #FEFEFE}
    .bg-custom:hover {background: #DEDEDEAA}
    .bg-custom-grey {background:#F9F9F9}
    .lc-icon {display:inline-block; width:35px !important; height:35px !important; background:#FFF; color:#8F908F; border-radius:50% !important}
    .lc-icon > i {font-size:16px}
    .d-glass {visibility: hidden}
</style>