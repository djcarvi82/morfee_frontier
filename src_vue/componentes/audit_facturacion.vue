<template>
    <div>
        <div :class="display == 'normal'? '': 'd-none'">
            <div class="d-flex justify-content-between mt-3 mb-3">
                <div>
                    <h5 class="txt-dark mb-0">FACTURACIÓN</h5>
                    <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de auditorías</div>
                </div>
                <div class="d-flex">
                    <div class="me-3">
                        <select class="form-control" v-model="f_user">
                            <option value="">Todos los usuarios</option>
                            <option :value="user._id" v-for="(user, i) in users" :key="i">{{ user._id }}</option>
                        </select>
                    </div>
                    <div class="me-3" style="width:300px">
                        <select name="" id="" class="form-control" v-model="f_nipre">
                            <option :value="{'_id': '', 'prestador': ''}">Todos los prestadores</option>
                            <option :value="ips" v-for="(ips, i) in ipss" :key="i">{{ ips.prestador }}</option>
                        </select>
                    </div>
                    <div>
                        <button class="btn btn-success" @click="loadFacturacion"><i class="fa fa-search me-2"></i>Buscar</button>
                    </div>
                </div>
            </div>

            <div :class="'panel panel-default card-view border ' + status">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <h5 class="text-center text-uppercase text-bold">Vencimiento de 20 días de facturas radicadas</h5>
                        <am-line ref="g_line" campo_categoria="fecha" campo_valor="total" altura="350" puntos etiquetas cursor paleta="2" grosor="2" lanzarevento="kona" procesar_fechas></am-line>
                        <div class="alert alert-warning mb-0">
                            De click en los puntos del gráfico de líneas para visualizar las facturas.
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border" v-if="status_gru == state.LOADING">
                <div class="panel-heading">
                    <h6 class="panel-title fs-5">FACTURAS SELECCIONADAS SEGÚN FECHA LÍMITE PARA AUDITAR</h6>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="d-flex align-items-center">
                            <i class="fa fa-spinner fa-spin me-2 fs-4"></i>
                            <span>Cargando facturas...</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border" v-else-if="status_gru == state.LOADED">
                <div class="panel-heading">
                    <h6 class="panel-title fs-5">FACTURAS SELECCIONADAS SEGÚN FECHA LÍMITE PARA AUDITAR</h6>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body row pa-0">
                        <div class="table-wrap">
                            <div class="table-responsive">
                                <table class="table table-hover mb-0x">
                                    <thead>
                                        <tr>
                                            <th class="colmin">No.</th>
                                            <th>Razón social</th>
                                            <th class="colmin">Factura</th>
                                            <th class="colmin">Auditor</th>
                                            <th class="colmin">Fecha radicado</th>
                                            <th class="colmin">Límite para auditar</th>
                                            <th class="colmin">Est. Aud. técnica</th>
                                            <th class="colmin">Est. Aud. Médica</th>
                                            <th class="colmin">Est. conciliación</th>
                                            <th class="colmin">Neto</th>
                                            <!-- <th class="colmin">Consecutivo</th>
                                            <th class="colmi">Usuario que radica</th> -->
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(elm, i) in grupo" :key="i" v-on:click="setFactura(elm)">
                                            <td class="py-2 text-center">{{ i + 1 }}</td>
                                            <td class="py-2">{{ elm.razon_social }}</td>
                                            <td class="py-2">{{ elm.factura }}</td>
                                            <td class="py-2">{{ elm.usuario_auditoria_tecnica }}</td>
                                            <td class="py-2">{{ elm.fecha_radicado }}</td>
                                            <td class="py-2 colmin"><span :class="hasTimeFree(addDays20(elm.fecha_radicado))? 'label label-success px-3': 'label label-danger px-3'">{{ addDays20(elm.fecha_radicado) }}</span></td>
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
                    </div>
                </div>
            </div>
        </div>
        <!-- End display normal -->
        <div :class="display == 'factura'? '': 'd-none'" v-if="targetFac != null">
            <div class="row">
                <div class="col-sm-4">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <h5>Factura No. <span class="txt-primary text-bold">{{ targetFac.factura }}</span></h5>
                                <h5>Contrato No. <span class="txt-primary text-bold">{{ targetFac.numero_contrato }}</span></h5>
                                <!-- <a href="javascript:void(0)" class="inline-block fs-5 text-danger" v-on:click="setDisplay"><i class="fa fa-times"></i></a> -->
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body row pa-0">
                                <div class="table-wrap" v-if="factura != null">
                                    <div class="table-responsive">
                                        <table class="table">
                                            <tbody>
                                                <tr>
                                                    <td class="py-2">
                                                        <div class="text-boldx">Prestador:</div>
                                                        <div class="txt-dark">{{ factura.razon_social }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2">
                                                        <div class="text-boldx">Nit:</div>
                                                        <div class="txt-dark">{{ factura.nit }}-{{ factura.digito_verificacion }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2">
                                                        <div class="text-boldx">Código de habilitación:</div>
                                                        <div class="txt-dark">{{ factura.codigo_prestador }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2">
                                                        <div class="text-boldx">Tipo de contrato:</div>
                                                        <div class="txt-dark">{{ factura.tipo_contrato }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2">
                                                        <div class="text-boldx">Modalidad de contrato:</div>
                                                        <div class="txt-dark">{{ factura.modalidad_contrato }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2">
                                                        <div class="text-boldx">Tipo de régimen:</div>
                                                        <div class="txt-dark">{{ factura.tipo_regimen }}</div>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                                <div class="px-4" v-else>
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="fa fa-spinner fa-spin me-2 fs-4"></i>
                                        <span>Cargando facturas...</span>
                                    </div>
                                </div>
                                <div class="px-3 mb-3">
                                    <button class="btn btn-danger btn-block btn-xs" type="button" v-on:click="setDisplay">Cerrar detalles</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="panel panel-default card-view border" v-if="factura != null">
                        <div class="panel-heading">
                            <h5 class="text-uppercase">Radicación de la factura</h5>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body row pa-0">
                                <div class="table-wrap">
                                    <div class="table-responsive">
                                        <table class="table">
                                            <tbody>
                                                <tr>
                                                    <td class="py-2">
                                                        <div>Fecha de radicación:</div>
                                                        <div class="txt-dark">{{ factura.fecha_radicado }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2">
                                                        <div>Consecutivo de radicado:</div>
                                                        <div class="txt-dark">{{ factura.consecutivo_radica }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2">
                                                        <div>Usuario que radica:</div>
                                                        <div class="txt-dark">{{ factura.usuario_radica }}</div>
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
                <div class="col-sm-4">
                    <div class="panel panel-default card-view border" v-if="factura != null">
                        <div class="panel-heading">
                            <h5 class="text-uppercase">ESTADOS DE LAS AUDITORÍAS</h5>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body">
                                <div class="py-2 px-3 border-start border-primary border-2 mb-4 bg-custom-grey">
                                    <h5 class="mt-0 mb-3">Auditoría técnica</h5>
                                    <div class="mb-3">
                                        <div class="txt-grey">Estado:</div>
                                        <div class="txt-danger" v-if="isEmpty(factura.estado_tecnica)">Sin datos!</div>
                                        <div class="txt-dark text-bold" v-else>{{ factura.estado_tecnica }}</div>
                                    </div>
                                    <div class="mb-3">
                                        <div class="txt-grey">Usuario auditoría técnica:</div>
                                        <div class="txt-danger" v-if="isEmpty(factura.usuario_auditoria_tecnica)">Sin datos!</div>
                                        <div class="txt-dark text-bold" v-else>{{ factura.usuario_auditoria_tecnica }}</div>
                                    </div>
                                    <div class="mb-3">
                                        <div class="txt-grey">Fecha de cierre de auditoría técnica:</div>
                                        <div class="txt-danger" v-if="isEmpty(factura.fecha_cierre_auditoria_tecnica)">Sin datos!</div>
                                        <div class="txt-dark text-bold" v-else>{{ factura.fecha_cierre_auditoria_tecnica }}</div>
                                    </div>
                                    <div class="mb-3x">
                                        <div class="txt-grey">Usuario cierre de auditoría técnica:</div>
                                        <div class="txt-danger" v-if="isEmpty(factura.usuario_cierre_auditoria_tecnica)">Sin datos!</div>
                                        <div class="txt-dark text-bold" v-else>{{ factura.usuario_cierre_auditoria_tecnica }}</div>
                                    </div>
                                </div>
                                <div class="py-2 px-3 border-start border-primary border-2 mb-4 bg-custom-grey">
                                    <h5 class="mt-0 mb-3">Auditoría médica</h5>
                                    <div class="mb-3">
                                        <div class="txt-grey">Estado:</div>
                                        <div class="txt-danger" v-if="isEmpty(factura.usuario_auditoria_medica)">Sin datos!</div>
                                        <div class="txt-dark text-bold" v-else>{{ factura.usuario_auditoria_medica }}</div>
                                    </div>
                                    <div class="mb-3x">
                                        <div class="txt-grey">Usuario auditoría médica:</div>
                                        <div class="txt-danger" v-if="isEmpty(factura.estado_medica)">Sin datos!</div>
                                        <div class="txt-dark text-bold" v-else>{{ factura.estado_medica }}</div>
                                    </div>
                                </div>
                                <div class="py-2 px-3 border-start border-primary border-2 mb-0 bg-custom-grey">
                                    <h5 class="mt-0 mb-3">Conciliación</h5>
                                    <div class="mb-3x">
                                        <div class="txt-grey">Estado factura conciliación:</div>
                                        <div class="txt-danger" v-if="isEmpty(factura.estado_factura_conciliacion)">Sin datos!</div>
                                        <div class="txt-dark text-bold" v-else>{{ factura.estado_factura_conciliacion }}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-4">
                    <div class="panel panel-default card-view border" v-if="factura != null">
                        <div class="panel-heading">
                            <h5 class="text-uppercase">VALOR FACTURA</h5>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body">
                                <div class="table-wrap">
                                    <div class="table-responsive">
                                        <table class="table mb-0">
                                            <tbody>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-success me-2"></i>Valor neto</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.valor_neto) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-danger me-2"></i>Total glosa</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.total_glosa) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="pt-2 pb-1 ps-1 text-bold" colspan="2" style="background:#F3F3F3; font-family:Arial">Glosa 1</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1" colspan="2">
                                                        <div class="d-flex">
                                                            <div class="me-4">
                                                                Fecha respuesta (eps):
                                                                <div class="txt-danger" v-if="isEmpty(factura.fecha_respuesta_eps_glosa_1)">Sin datos!</div>
                                                                <div class="txt-dark text-bold" v-else>{{ factura.fecha_respuesta_eps_glosa_1 }}</div>
                                                            </div>
                                                            <div>
                                                                Usuario respuesta (eps):
                                                                <div class="txt-danger" v-if="isEmpty(factura.usuario_respuesta_eps_glosa_1)">Sin datos!</div>
                                                                <div class="txt-dark text-bold" v-else>{{ factura.usuario_respuesta_eps_glosa_1 }}</div>
                                                            </div>
                                                        </div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-danger me-2"></i>Valor aceptado (eps):</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.valor_aceptado_eps_1) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-success me-2"></i>Saldo (eps):</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.saldo_eps_1) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="pt-2 pb-1 ps-1 text-bold" colspan="2" style="background:#F3F3F3; font-family:Arial">Glosa 2</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1" colspan="2">
                                                        Fecha respuesta (ips):
                                                        <div class="txt-danger" v-if="isEmpty(factura.fecha_respuesta_ips_glosa_2)">Sin datos!</div>
                                                        <div class="txt-dark text-bold" v-else>{{ factura.fecha_respuesta_ips_glosa_2 }}</div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-danger me-2"></i>Valor aceptado (ips):</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.valor_aceptado_ips_2) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-success me-2"></i>Saldo (ips):</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.saldo_ips_2) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1" colspan="2">
                                                        <div class="d-flex">
                                                            <div class="me-4">
                                                                Fecha respuesta (eps):
                                                                <div class="txt-danger" v-if="isEmpty(factura.fecha_respuesta_eps_glosa_2)">Sin datos!</div>
                                                                <div class="txt-dark text-bold" v-else>{{ factura.fecha_respuesta_eps_glosa_2 }}</div>
                                                            </div>
                                                            <div>
                                                                Usuario respuesta (eps):
                                                                <div class="txt-danger" v-if="isEmpty(factura.usuario_respuesta_eps_glosa_2)">Sin datos!</div>
                                                                <div class="txt-dark text-bold" v-else>{{ factura.usuario_respuesta_eps_glosa_2 }}</div>
                                                            </div>
                                                        </div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-danger me-2"></i>Valor aceptado (eps):</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.valor_aceptado_eps_2) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-success me-2"></i>Saldo (eps):</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.saldo_eps_2) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="pt-2 pb-1 ps-1 text-bold" colspan="2" style="background:#F3F3F3; font-family:Arial">Conciliación</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1" colspan="2">
                                                        <div class="d-flex">
                                                            <div class="me-4">
                                                                Fecha conciliación gerencial:
                                                                <div class="txt-danger" v-if="isEmpty(factura.fecha_conciliacion_gerencial)">Sin datos!</div>
                                                                <div class="txt-dark text-bold" v-else>{{ factura.fecha_conciliacion_gerencial }}</div>
                                                            </div>
                                                            <div>
                                                                Usuario conciliación gerencial:
                                                                <div class="txt-danger" v-if="isEmpty(factura.usuario_conciliacion_gerencial)">Sin datos!</div>
                                                                <div class="txt-dark text-bold" v-else>{{ factura.usuario_conciliacion_gerencial }}</div>
                                                            </div>
                                                        </div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-success me-2"></i>Valor aceptado gerencia EPS:</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.valor_aceptado_eps_gerencial) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-success me-2"></i>Valor aceptado gerencia IPS:</td>
                                                    <td class="py-2 pe-0 text-right txt-dark">{{ formatMiles(factura.valor_aceptado_ips_gerencial) }}</td>
                                                </tr>
                                                <tr>
                                                    <td class="pt-2 pb-1 ps-1 text-bold" colspan="2" style="background:#F3F3F3; font-family:Arial">COSTO FINAL</td>
                                                </tr>
                                                <tr>
                                                    <td class="py-2 ps-1"><i class="fa fa-caret-right txt-success me-2"></i>Valor final:</td>
                                                    <td class="py-2 pe-0 text-right txt-dark"></td>
                                                </tr>
                                                <!-- 
                                                    fecha_respuesta_ips_glosa_2
                                                    valor_aceptado_ips_2
                                                    saldo_ips_2

                                                    fecha_respuesta_eps_glosa_2
                                                    usuario_respuesta_eps_glosa_2
                                                    valor_aceptado_eps_2
                                                    saldo_eps_2


                                                    valor_aceptado_ips_gerencial
                                                    valor_aceptado_eps_gerencial
                                                 -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Counter from './Contador_light.vue';
import PieChart from './amcharts/pie.vue';
import BarChart from './amcharts/bar.vue';
import LineChart from './amcharts/line.vue';
import VerticalChart from './amcharts/bar-vertical.vue';

export default {
    components: {'local-counter': Counter, 'am-pie': PieChart, 'am-bar': BarChart, 'am-ver': VerticalChart, 'am-line': LineChart},
    props: {
        fillpath: {type: String, default: ''},
    },
    data() {
        return {
            mss: ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            ipss: [],
            times: [],
            users: [],
            f_nipre: {'_id': '', 'prestador': ''},
            f_periodo: '',
            f_user: '',
            display: 'normal', // normal | factura
            // festivos: {'2022-01-10': true, '2022-03-21': true, '2022-04-14': true, '2022-04-15': true, '2022-05-30': true, '2022-06-20': true, '2022-06-27': true, '2022-07-04': true, '2022-07-20': true, '2022-08-15': true, '2022-10-17': true, '2022-11-07': true, '2022-11-14': true, '2022-12-08': true, '2023-01-09': true, '2023-03-20': true, '2023-04-06': true, '2023-04-07': true, '2023-05-01': true, '2023-05-22': true, '2023-06-12': true, '2023-06-19': true, '2023-07-03': true, '2023-07-20': true, '2023-08-07': true, '2023-08-21': true, '2023-10-16': true, '2023-11-06': true, '2023-11-13': true, '2023-12-08': true, '2023-12-25': true},
            targetFac: null,
            factura: null,
            num_today: 0,
            after20: {},
            datos: [],
            grupo: [],  // Grupo de facturas
            status: 'ini',
            status_gru: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            ope: '',
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
        setFactura: function(elm){
            this.targetFac = elm;
            this.display = 'factura';
            this.loadFactura(this.targetFac.factura);
        },
        setDisplay: function(){
            this.display = 'normal';
            this.targetFac = null;
        },
        // isFestivo: function(day, fecha){
        //     if(day % 6 == 0){
        //         return true;
        //     }
        //     return (this.festivos[fecha] === true);
        // },
        loadFacturacion: function(){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('nit', this.f_nipre._id);
                pam.append('periodo', this.f_periodo);
                pam.append('user', this.f_user);
                this.status = this.state.LOADING;
                axios.post(root_path + 'auditorias/vue/facturas/fecha', pam).then(res => {
                    let blk = {};
                    let tmr = res.data[0].facet_group.map(elm => {
                        elm.fecha = this.addDays20(elm._id);
                        return elm;
                    });
                    tmr.forEach(elm => {
                        if(blk[elm.fecha] == undefined){
                            blk[elm.fecha] = {'fecha': elm.fecha, 'total': 0, 'origen': []};
                        }
                        blk[elm.fecha].total += elm.total;
                        blk[elm.fecha].origen.push(elm._id);
                    });
                    this.datos = Object.values(blk);
                    this.$refs.g_line.setDatos(this.datos);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        loadPoint: function(fecha){
            if(this.status_gru != this.state.LOADING){
                let pam = new FormData();
                pam.append('fecha', fecha);
                pam.append('nit', this.f_nipre._id);
                pam.append('periodo', this.f_periodo);
                pam.append('user', this.f_user);
                this.status_gru = this.state.LOADING;
                axios.post(root_path + 'auditorias/vue/facturas/point', pam).then(res => {
                    this.grupo = res.data[0].repu;
                    this.status_gru = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status_gru = this.state.FAILED;
                });
            }
        },
        loadFactura: function(fac){
            let pam = new FormData();
            pam.append('factura', fac);
            axios.post(root_path + 'auditorias/vue/factura', pam).then(res => {
                this.factura = res.data;
            }).catch(err => {
                console.log(err);
            });
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
        hasTimeFree: function(ymd){
            let num = parseInt(ymd.toString().replaceAll('-', ''));
            return (num > this.num_today)? true: false;
        },
        loadFiltros: function(){
            axios.post(this.fillpath).then(res => {
                this.ipss = res.data[0].ipss;
                this.users = res.data[0].users.map(elm => {
                    let aux = elm._id == ''? '(Vacio)': elm._id;
                    return {'_id': aux, 'total': elm.total};
                });
            }).catch(err => {console.log(err)});
        },
        listen: function(){
            this.$eventBus.$on('kona', arg => {
                this.loadPoint(arg.origen.join('|'));
            });
        }
    },
    mounted() {
        this.num_today = parseInt((new Date()).toISOString().slice(0, 10).replaceAll('-', ''));
        this.listen();
        this.loadFacturacion();
        this.loadFiltros();
    }
}
</script>
<style scoped>
.colmin {width:1%; white-space: nowrap; text-align: center}
.loading {opacity: .4}
.text-bold {font-weight: bold}
.bg-custom-grey {background: #FAFAFA !important; border-top:1px solid #DDD !important; border-bottom:1px solid #DDD !important; border-right: 1px solid #DDD !important}
/* table.table.table-hover > tbody > tr > td {user-select: none !important} */
</style>