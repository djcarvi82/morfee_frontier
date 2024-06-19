<template>
    <div>
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">RESUMEN</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de auditorías</div>
            </div>
            <div class="d-flex">
                <div class="me-3">
                    <select name="" id="" class="form-control" v-model="d_depto">
                        <option value="">Departamento...</option>
                        <option :value="dep._id" v-for="(dep, i) in deptos" :key="i">{{ dep._id }}</option>
                    </select>
                </div>
                <div class="me-3">
                    <select name="" id="" class="form-control" v-model="d_tcc">
                        <option value="">Todos...</option>
                        <option :value="con" v-for="(con, a) in tcc" :key="a">{{ con }}</option>
                    </select>
                </div>
                <div class="me-3">
                    <select name="" id="" class="form-control" v-model="d_audit">
                        <option value="">Todos los auditores</option>
                        <option :value="aud.valor" v-for="(aud, a) in auditores" :key="a">{{ aud.auditor }}</option>
                    </select>
                </div>
                <div class="me-3" style="max-width:300px">
                    <select name="" id="" class="form-control" v-model="d_nipre">
                        <option :value="{'nit': '', 'prestador': ''}">Todos los prestadores</option>
                        <option :value="ips" v-for="(ips, i) in ipss" :key="i">{{ ips.prestador }}</option>
                    </select>
                </div>
                <div class="me-3">
                    <div class="input-group">
                        <select name="" id="" class="form-control" v-model="d_periodo">
                            <option value="">Todos...</option>
                            <optgroup :label="elm.anio" v-for="(elm, i) in times" :key="i">
                                <option v-for="(mes, m) in elm.meses" :key="m" :value="mes.ym">{{ mes.tx }} ({{ formatMiles(mes.total) }} registros)</option>
                            </optgroup>
                        </select>
                        <span class="input-group-btn">
                            <button class="btn btn-success" @click="manager"><i class="fa fa-search"></i></button>
                        </span>
                    </div>
                </div>
            </div>
        </div>
        <div class="d-flex justify-content-between mb-4 df-options">
            <a :class="section == elm.code? 'flex-fill bg-target ' + status: 'flex-fill bg-custom ' + status" href="javascript:void(0)" v-for="(elm, i) in opciones" :key="i" @click="setSection(elm.code)">
                <div class="d-flex align-items-center">
                    <span class="lc-icon d-flex align-items-center justify-content-center me-2"><i :class="section == elm.code? 'fa fa-folder-open-o': 'fa fa-folder-o'"></i></span>
                    <span>{{ elm.tx }}</span>
                </div>
            </a>
        </div>
        <!-- *************** -->
        <!-- RESULT SECTIONS -->
        <!-- *************** -->
        <div :class="section == 'razon_social'? 'panel panel-default card-view border': 'd-none'">
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <div class="mb-4">
                        <h5 class="text-center text-uppercase fs-5">Número de facturas radicadas por prestador</h5>
                        <div class="text-center fs-6">{{ getTitleDepto() }}</div>
                        <div class="text-center fs-6" v-if="human_period != ''">Primeros 20 - {{ human_period }}</div>
                    </div>
                    <am-ver ref="gp_social" campo_categoria="_id" campo_valor="count" etiquetas grilla="0" multicolor tooltip unidad="30" altura_minima="100"></am-ver>
                </div>
            </div>
        </div>
        <div :class="section == 'cifras'? '': 'd-none'">
            <div class="row">
                <div class="col-sm-7">
                    <div class="row">
                        <div class="col-sm-4">
                            <local-counter ref="contador_1" fontsize="22px" class="border" pretag="$" valor="0" duracion="1" miles texto="VALOR FACTURACIÓN"></local-counter>
                        </div>
                        <div class="col-sm-4">
                            <local-counter ref="contador_2" fontsize="22px" class="border" pretag="$" valor="0" duracion="1" miles texto="TOTAL GLOSA"></local-counter>
                        </div>
                        <div class="col-sm-4">
                            <local-counter ref="contador_3" fontsize="22px" class="border" pretag="$" valor="0" duracion="1" miles texto="TOTAL ACEPTA EPS"></local-counter>
                        </div>
                    </div>
                </div>
                <div class="col-sm-5">
                    <div class="row">
                        <div class="col-sm-6">
                            <local-counter ref="contador_4" fontsize="22px" class="border" pretag="$" valor="0" duracion="1" miles texto="TOTAL ACEPTA IPS"></local-counter>
                        </div>
                        <div class="col-sm-6">
                            <local-counter ref="contador_5" fontsize="22px" class="border" pretag="$" valor="0" duracion="1" miles texto="DIFERENCIA"></local-counter>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-7">
                    <div class="row">
                        <div class="col-sm-4">
                            <local-counter ref="por_1" fontsize="22px" class="border" valor="0" duracion="1" miles texto="% FACTURACIÓN"></local-counter>
                        </div>
                        <div class="col-sm-4">
                            <local-counter ref="por_2" fontsize="22px" class="border" valor="0" duracion="1" miles texto="% GLOSA"></local-counter>
                        </div>
                        <div class="col-sm-4">
                            <local-counter ref="por_3" fontsize="22px" class="border" valor="0" duracion="1" miles texto="% ACEPTA EPS"></local-counter>
                        </div>
                    </div>
                </div>
                <div class="col-sm-5">
                    <div class="row">
                        <div class="col-sm-6">
                            <local-counter ref="por_4" fontsize="22px" class="border" valor="0" duracion="1" miles texto="% ACEPTA IPS"></local-counter>
                        </div>
                        <div class="col-sm-6">
                            <local-counter ref="por_5" fontsize="22px" class="border" valor="0" duracion="1" miles texto="% DIFERENCIA"></local-counter>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-10">
                    <div class="panel panel-default card-view border">
                        <div class="panel-wrapper collapse in">
                            <div class="panel-body">
                                <div class="mb-3">
                                    <span :class="subitem == 'general'? 'badge badge-success df-hand': 'badge df-hand'" @click="setSubitem('general')">Vista general</span>
                                    <span :class="subitem == 'detail'? 'badge badge-success df-hand': 'badge df-hand'" @click="setSubitem('detail')">Vista detallada</span>
                                </div>
                                <div :class="subitem == 'general'? '': 'd-none'">
                                    <div class="mb-4">
                                        <h5 class="text-center text-uppercase">Facturación por periodos</h5>
                                        <div class="text-center fs-6">{{ getTitleDepto() }}</div>
                                        <div class="text-center fs-6" v-if="human_period != ''">{{ human_period }}</div>
                                    </div>
                                    <am-bar ref="gp_dual" campo_categoria="_id" campo_valor="count" etiquetas grilla="0" paleta="#FA6065" lanzarevento="select-per" tooltip :custom="txtool" cursor sin_valores></am-bar>
                                </div>
                                <div :class="subitem == 'detail'? '': 'd-none'">
                                    <div class="mb-4">
                                        <h5 class="text-center text-uppercase">{{ d_periodo == ''? 'FACTURACIÓN POR PRESTADOR': 'FACTURACIÓN POR PRESTADOR' }}</h5>
                                        <div class="text-center fs-6">{{ getTitleDepto() }}</div>
                                        <div class="text-center fs-6" v-if="human_period != ''">Primeros 20 - {{ human_period }}</div>
                                    </div>
                                    <am-ver ref="gp_1" campo_categoria="_id" campo_valor="count" pretag="$" etiquetas grilla="0" multicolor tooltip unidad="30" altura_minima="100"></am-ver>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-2">
                    <local-counter ref="por_77" class="border" valor="0" duracion="1" miles texto="% GLOSA RATIFICADA"></local-counter>
                </div>
            </div>
        </div>
        <div :class="section == 'tipo_regimen'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="mb-4">
                            <h5 class="text-center text-uppercase">Facturación según tipo de contratación</h5>
                            <div class="text-center fs-6">{{ getTitleDepto() }}</div>
                            <div class="text-center fs-6" v-if="human_period != ''">{{ human_period }}</div>
                        </div>
                        <am-bar ref="gp_regimen" campo_categoria="_id" campo_valor="total" custom="{valueY}" altura="400" redondeado multicolor etiquetas tooltip cursor></am-bar>
                        <div class="d-flex justify-content-center">
                            <button class="btn btn-success" type="button" @click="setEvgroup(false)" v-if="evgroup">Agrupar evento</button>
                            <button class="btn btn-success loading" type="button" @click="setEvgroup(true)" v-else>Agrupar evento</button>
                            <div class="btn-group ms-4">
                                <button :class="evsuma? 'btn btn-success': 'btn btn-default'" @click="setEvsuma(true)">Total factura</button>
                                <button :class="evsuma == false? 'btn btn-success': 'btn btn-default'" @click="setEvsuma(false)">Total registros</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'case'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="mb-4">
                            <h5 class="text-center text-uppercase">Estado técnico</h5>
                            <div class="text-center fs-6">{{ getTitleDepto() }}</div>
                            <div class="text-center fs-6" v-if="human_period != ''">{{ human_period }}</div>
                        </div>
                        <am-bar 
                            ref="gp_case" 
                            campo_categoria="_id" 
                            campo_valor="total:Registros" 
                            empty_category="(Vacío)" 
                            altura="400" 
                            multicolor 
                            redondeado
                            paleta="#0bb4ff,#50e991,#e6d800,#9b19f5,#ffa300,#dc0ab4,#b3d4ff,#00bfa0" 
                            etiquetas 
                            tooltip 
                            lanzarevento="bar-estado"
                            cursor>
                        </am-bar>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border" v-if="status_bar != 'ini'">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <h6 class="panel-title txt-dark">FACTURAS SELECCIONADAS</h6>
                        <div>
                            <div class="btn-group">
                                <button class="btn btn-default btn-outline" :disabled="pagina == 1" type="button" @click="loadSelectBar(barSelect, pagina - 1)"><i class="fa fa-chevron-left me-2"></i> Anterior</button>
                                <button class="btn btn-default btn-outline" :disabled="!hasNext" type="button" @click="loadSelectBar(barSelect, pagina + 1)">Siguiente <i class="fa fa-chevron-right ms-2"></i></button>
                            </div>
                        </div>
                        <!-- <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a> -->
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="d-flex align-items-center" v-if="status_bar == state.LOADING">
                            <i class="fa fa-spinner fa-spin fs-2 me-3"></i>
                            <span>Cargando facturas...</span>
                        </div>
                        <div v-if="status_bar == state.LOADED">
                            <table class="table mb-4">
                                <thead>
                                    <tr>
                                        <th class="colmin px-4">No.</th>
                                        <th class="text-center">Número de radicación</th>
                                        <th class="text-centerx">Razón social</th>
                                        <th class="text-center">Factura</th>
                                        <th class="colmin px-4">Fecha radicado</th>
                                        <th class="text-center">Tipo contrato</th>
                                        <th class="text-center">Departamento</th>
                                        <th class="text-center">Municipio</th>
                                        <th>Auditor</th>
                                        <th class="text-center">Estado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(elm, i) in slicebar" :key="i">
                                        <td class="text-center">{{ wpage(i) }}</td>
                                        <td class="text-center">{{ elm.numero_radicacion }}</td>
                                        <td class="text-centerx">{{ elm.razon_social }}</td>
                                        <td class="text-center">{{ elm.factura }}</td>
                                        <td class="text-center">{{ elm.fecha_radicado }}</td>
                                        <td class="text-center">{{ elm.tipo_contrato }}</td>
                                        <td class="text-center">{{ elm.departamento }}</td>
                                        <td class="text-center">{{ elm.municipio }}</td>
                                        <td class="text-center">{{ elm.usuario_auditoria_tecnica }}</td>
                                        <td class="text-center">{{ elm.estado_tecnica }}</td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="d-flex justify-content-end">
                                <div class="btn-group">
                                    <button class="btn btn-default btn-outline" :disabled="pagina == 1" type="button" @click="loadSelectBar(barSelect, pagina - 1)"><i class="fa fa-chevron-left me-2"></i> Anterior</button>
                                    <button class="btn btn-default btn-outline" :disabled="!hasNext" type="button" @click="loadSelectBar(barSelect, pagina + 1)">Siguiente <i class="fa fa-chevron-right ms-2"></i></button>
                                </div>
                            </div>
                        </div>
                    </div><!-- End panel-body -->
                </div><!-- End panel wrapper -->
            </div>
        </div><!-- End section CASE -->
        <div :class="section == 'conciliacion'? '': 'd-none'">
            <div :class="'panel panel-default card-view border ' + status">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="mb-4">
                            <h5 class="text-center text-uppercase">Facturación según estado de conciliación</h5>
                            <div class="text-center fs-6">{{ getTitleDepto() }}</div>
                            <div class="text-center fs-6" v-if="human_period != ''">{{ human_period }}</div>
                        </div>
                        <!-- <am-bar ref="gp_concilia" campo_categoria="_id" campo_valor="total" altura="400" sin_valores multicolor paleta="#0bb4ff,#50e991,#e6d800,#9b19f5,#ffa300,#dc0ab4,#b3d4ff,#00bfa0" redondeado etiquetas tooltip cursor lanzarevento="concilio"></am-bar> -->
                        <am-two 
                            ref="gp_two" 
                            campo_categoria="per" 
                            campo_valor="ready:Conciliado,pending:Pendiente por conciliar,glosado:Valor glosado" 
                            unidad="80" 
                            paleta="#17B978,#FF595E,#ffbf69,#00afb9,#ffca3a,#8ac926,#6a4c93" 
                            cursor
                            lanzarevento="concilio">
                        </am-two>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border" v-if="status_slice != 'ini'">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <h6 class="panel-title txt-dark">FACTURAS SELECCIONADAS</h6>
                        <div>
                            <div class="btn-group">
                                <button class="btn btn-default btn-outline" :disabled="pagina_alt == 1" type="button" @click="loadConcilioUnity(barSelect_alt, pagina_alt - 1)"><i class="fa fa-chevron-left me-2"></i> Anterior</button>
                                <button class="btn btn-default btn-outline" :disabled="!hasNext_alt" type="button" @click="loadConcilioUnity(barSelect_alt, pagina_alt + 1)">Siguiente <i class="fa fa-chevron-right ms-2"></i></button>
                            </div>
                        </div>
                        <!-- <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a> -->
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="d-flex align-items-center" v-if="status_slice == state.LOADING">
                            <i class="fa fa-spinner fa-spin fs-2 me-3"></i>
                            <span>Cargando facturas...</span>
                        </div>
                        <div v-if="status_slice == state.LOADED">
                            <table class="table mb-4">
                                <thead>
                                    <tr>
                                        <th class="colmin px-4">No.</th>
                                        <th class="text-center">No. radicación</th>
                                        <th class="colmin px-4">Fecha radicado</th>
                                        <th class="text-centerx">Razón social</th>
                                        <th class="text-center">Factura</th>
                                        <th class="text-center">Tipo contrato</th>
                                        <th>Auditor</th>
                                        <th class="text-center">Total glosa</th>
                                        <th class="text-center">Acepta EPS</th>
                                        <th class="text-center">Acepta IPS</th>
                                        <th class="text-center">Estado conciliación</th>
                                        <th class="text-center">Estado</th>
                                        <th class="text-center">Departamento</th>
                                        <th class="text-center">Municipio</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(elm, i) in slicecon" :key="i">
                                        <td class="text-center">{{ wpage_alt(i) }}</td>
                                        <td class="text-center">{{ elm.numero_radicacion }}</td>
                                        <td class="text-center">{{ elm.fecha_radicado }}</td>
                                        <td class="text-centerx">{{ elm.razon_social }}</td>
                                        <td class="text-center">{{ elm.factura }}</td>
                                        <td class="text-center">{{ elm.tipo_contrato }}</td>
                                        <td class="text-center">{{ elm.usuario_auditoria_tecnica }}</td>
                                        <td class="text-right">{{ formatMiles(elm.total_glosa) }}</td>
                                        <td class="text-right">{{ formatMiles(elm.valor_total_acepta_eps) }}</td>
                                        <td class="text-right">{{ formatMiles(elm.valor_total_acepta_ips) }}</td>
                                        <td class="text-cemter">{{ wconci(elm.formi) }}</td>
                                        <td class="text-center">{{ elm.estado_tecnica }}</td>
                                        <td class="text-center">{{ elm.departamento }}</td>
                                        <td class="text-center">{{ elm.municipio }}</td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="d-flex justify-content-end">
                                <div class="btn-group">
                                    <button class="btn btn-default btn-outline" :disabled="pagina_alt == 1" type="button" @click="loadConcilioUnity(barSelect_alt, pagina_alt - 1)"><i class="fa fa-chevron-left me-2"></i> Anterior</button>
                                    <button class="btn btn-default btn-outline" :disabled="!hasNext_alt" type="button" @click="loadConcilioUnity(barSelect_alt, pagina_alt + 1)">Siguiente <i class="fa fa-chevron-right ms-2"></i></button>
                                </div>
                            </div>
                        </div>
                    </div><!-- End panel-body -->
                </div><!-- End panel wrapper -->
            </div>


            <div :class="'d-none panel panel-default card-view border ' + status_slice">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="mb-4">
                            <h5 class="text-center text-uppercase">Facturas seleccionadas</h5>
                            <!-- <div class="text-center fs-6" v-if="human_period != ''">{{ human_period }}</div> -->
                        </div>
                        <table class="table display product-overview border-none" id="support_table">
                            <thead>
                                <tr>
                                    <th class="colminx">Tipo de glosa</th>
                                    <th class="text-center">Número de registros</th>
                                    <th class="text-center">Valor de glosa</th>
                                    <th class="text-center">% Representativo</th>
                                    <th class="colmin px-4">Ver detalles</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(glo, i) in datos" :key="i" :class="cssrow(glo.grupo)">
                                    <td class="colminx">{{ glo.concepto }}</td>
                                    <td class="text-center">{{ formatMiles(glo.total) }}</td>
                                    <td class="text-center">{{ formatMiles(glo.suma) }}</td>
                                    <td class="text-center">{{ glo.percent }}%</td>
                                    <td class="text-center">
                                        <i class="fa fa-circle fs-5 df-hand text-success" v-if="targetGrupo == glo.grupo"></i>
                                        <i :class="glo.grupo == '0'? 'fa fa-circle-o fs-5 df-hand xd-none': 'fa fa-circle-o fs-5 df-hand'" @click="setGrupo(glo.grupo)" v-else></i>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

        </div>
        <!-- <div class="table-wrap">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead>
                        <tr>
                            <th class="colmin">No.</th>
                            <th>Item</th>
                            <th class="colmin">Total</th>
                        </tr>
                    </thead>
                    <tbody v-if="targetItem == 'cifras'">
                        <tr v-for="(elm, i) in datos" :key="i">
                            <td class="py-2 text-center">{{ i + 1 }}</td>
                            <td class="py-2">{{ elm.prestador }}</td>
                            <td class="py-2 text-right">{{ formatMiles(elm.total) }}</td>
                        </tr>
                        <tr style="color:#000; font-weight:bold">
                            <td class="text-dark">Total:</td>
                            <td class="text-right" colspan="2">{{ formatMiles(datos.reduce((acum, elm) => acum + elm.total, 0)) }}</td>
                        </tr>
                    </tbody>
                    <tbody v-else>
                        <tr v-for="(elm, i) in datos" :key="i">
                            <td class="py-2 text-center">{{ i + 1 }}</td>
                            <td class="py-2">{{ elm._id }}</td>
                            <td class="py-2 text-center px-4">{{ elm.count }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div> -->
        <local-modal 
            coleccion="audit_facturas_0" 
            :altpath="pathcifras + '/conciliacion/slice'"
            cantidad="50"
            campos="numero_recepcion,numero_radicacion,valor_factura,numero_contrato,tipo_contrato,modalidad_contrato,estado_factura_conciliacion,nit,razon_social,factura,fecha_radicado,usuario_radica,usuario_auditoria_tecnica,pos,estado_tecnica,case,valor_total_acepta_eps,valor_total_acepta_ips,crx:Periodo">
        </local-modal>
    </div>
</template>
<script>
import Counter from './Contador_light.vue';
import PieChart from './amcharts/pie.vue';
import BarChart from './amcharts/bar.vue';
import VerticalChart from './amcharts/bar-vertical.vue';
import BarTwo from './amcharts/bar-two.vue';
import Modal from './modal_table_data.vue';
export default {
    components: {'local-counter': Counter, 'am-pie': PieChart, 'am-bar': BarChart, 'am-ver': VerticalChart, 'am-two': BarTwo, 'local-modal': Modal},
    props: {
        pathcifras: {type: String, default: ''}
    },
    data() {
        return {
            mss: ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            section: 'razon_social',
            kunas: {'ready': 'Conciliado', 'pending': 'Pendiente'},
            opciones: [
                {'status': 'ini', 'data': [], 'alt': [], 'depto': '', 'tcc': '', 'audit': '', 'nit': '', 'periodo': '', 'tx': '# de facturas radicadas', 'code': 'razon_social'}, 
                {'status': 'ini', 'data': [], 'alt': [], 'depto': '', 'tcc': '', 'audit': '', 'nit': '', 'periodo': '', 'tx': 'Cifras en pesos', 'code': 'cifras'}, 
                {'status': 'ini', 'data': [], 'alt': [], 'depto': '', 'tcc': '', 'audit': '', 'nit': '', 'periodo': '', 'tx': 'Tipo de contratación', 'code': 'tipo_regimen'}, 
                {'status': 'ini', 'data': [], 'alt': [], 'depto': '', 'tcc': '', 'audit': '', 'nit': '', 'periodo': '', 'tx': 'Estado de auditoría', 'code': 'case'},
                {'status': 'ini', 'data': [], 'alt': [], 'depto': '', 'tcc': '', 'audit': '', 'nit': '', 'periodo': '', 'tx': 'Conciliación', 'code': 'conciliacion'}
            ],
            deptos: [],
            tcc: [],
            ipss: [],
            times: [],
            auditores: [],
            txtool: `[bold]{categoryX}[/]
                Facturacion: {valueY}
                Glosas: {glosa}
                Total a pagar: {pago}
                # de facturas: {items}`,
            targetItem: '',
            targetChart: '',
            subitem: 'general',     // general | detail
            items: [
                {'item': 'razon_social', 'tx': 'Razón social', 'ope': 'count', 'chart': 'bar'}, 
                {'item': 'cifras', 'tx': 'Cifras', 'ope': 'count', 'chart': 'bar'}, 
                {'item': 'tipo_regimen', 'tx': 'Régimen', 'ope': 'count', 'chart': 'pie'},
                {'item': 'case', 'tx': 'Case', 'ope': 'count', 'chart': 'pie'},
                {'item': 'estado_factura_conciliacion', 'tx': 'Conciliación', 'ope': 'count', 'chart': 'pie'},
            ],
            datos: [],
            slicedata: [],
            f_nit: '',
            f_periodo: '',
            prestadortx: '',
            d_depto: '',
            d_tcc: '',
            d_audit: '',
            d_nipre: {'nit': '', 'prestador': ''},
            d_nit: '',
            d_periodo: '',
            pagina: 1,
            barSelect: '',
            hasNext: false,
            slicebar: [],
            pagina_alt: 1,
            barSelect_alt: '',
            periodo_alt: '',
            hasNext_alt: false,
            slicecon: [],
            status: 'ini',
            status_bar: 'ini',
            status_slice: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            lastcon: {'nit': '', 'periodo': '', 'prestador': '', 'status': 'ini'},
            evgroup: true,
            evsuma: true,
        }
    },
    watch: {
        d_nipre: function(val){
            this.d_nit = val.nit;
            this.prestadortx = val.prestador;
        }  
    },
    computed: {
        human_period: function(){
            let ym = this.d_periodo.toString();
            if(ym.length == 7){
                let anio = ym.slice(0, 4);
                let ms = parseInt(ym.slice(-2));
                return this.mss[ms] + ' de ' + anio;
            }
            return '';
        },
        period_modal: function(){
            let ym = this.d_periodo.toString();
            return (ym.length == 7)? ym.replace('-', ''): null;
        }
    },
    methods: {
        getTitleDepto: function(){
            let tm = this.opciones.find(op => op.code == this.section);
            if(!this.isEmpty(tm)){
                if(tm.status == this.state.LOADED && tm.depto != ""){
                    return "Departamento: " + tm.depto;
                }else{
                    return "";
                }
            }
            return "";
        },
        isEmpty: function(arg){
            return ['', undefined, null].includes(arg);
        },
        clearNumber: function(num){
            return (num % 1 == 0)? num: parseFloat(num).toFixed(2);
        },
        formatMiles: function(num){
            return this.isEmpty(num)? num: num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        setSection: function(arg){
            if(this.status != this.state.LOADING){
                this.section = arg;
                this.manager();
            }
        },
        customRounded: function(num){
            let n = parseFloat(num);
            let res = n % 1;
            if(res >= 0.5){
                return Math.ceil(n);
            }else{
                return num;
            }
        },
        setEvgroup: function(bool){
            this.evgroup = bool;
            let tm = this.opciones[2].data;
            let xim = {};
            if(this.evgroup){
                tm.forEach(elm => {
                    let key = /^(Evento|Sin)/i.test(elm._id)? 'Evento': elm._id;
                    if(xim[key] == undefined) xim[key] = {'_id': key, 'total': 0};
                    xim[key].total += this.evsuma? elm.factura: elm.total;
                });
            }else{
                tm.forEach(elm => {
                    if(xim[elm._id] == undefined) xim[elm._id] = {'_id': elm._id, 'total': 0};
                    xim[elm._id].total += this.evsuma? elm.factura: elm.total;
                });
            }
            this.$refs.gp_regimen.setDatos(Object.values(xim));
        },
        setEvsuma: function(bool){
            this.evsuma = bool;
            this.setEvgroup(this.evgroup);
        },
        wpage: function(it){
            return (50 * (this.pagina -1)) + (it + 1);
        },
        wpage_alt: function(it){
            return (50 * (this.pagina_alt -1)) + (it + 1);
        },
        wconci: function(formi){
            return this.kunas[formi];
        },
        loadGroup: function(){
            var pam = new FormData();
            pam.append('tema', 'audit_facturas_0');
            pam.append('action', 'count:' + this.targetItem);
            this.status = this.state.LOADING;
            axios.post(root_path + 'reservas/mng/group', pam).then(res => {
                this.datos = res.data;
                this.$refs.gp_1.setDatos(this.datos.map(elm => ({_id: elm._id.length > 45? elm._id.slice(0, 45) + '...': elm._id, 'count': elm.count})).sort((a, b) => a.count - b.count));
                this.status = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status = this.state.FAILED;
            });
        },
        loadSocial: function(){
            this.status = this.state.LOADING;
            this.setCampo('depto', this.d_depto);
            this.setCampo('tcc', this.d_tcc);
            this.setCampo('audit', this.d_audit);
            this.setCampo('nit', this.d_nit);
            this.setCampo('periodo', this.d_periodo);
            this.setCampo('status', this.state.LOADING);
            let pam = new FormData();
            pam.append('depto', this.d_depto);
            pam.append('tcc', this.d_tcc);
            pam.append('auditor', this.d_audit);
            pam.append('nit', this.d_nit);
            pam.append('periodo', this.d_periodo);
            axios.post(this.pathcifras + '/social', pam).then(res => {
                let dts = [];
                dts = res.data.map(elm => {
                    return {'_id': elm.prestador.length > 45? elm.prestador.slice(0, 45) + '...': elm.prestador, 'count': elm.count};
                }).slice(0, 20);
                this.setCampo('data', res.data);
                this.setCampo('alt', dts.sort((a, b) => a.count - b.count));
                // this.$refs.gp_1.setDatos(this.getCampo('razon_social', 'alt'));
                this.$refs.gp_social.setDatos(this.getCampo('razon_social', 'alt'));
                this.status = this.state.LOADED;
                this.setCampo('status', this.state.LOADED);
            }).catch(err => {
                console.log(err);
                this.status = this.state.FAILED;
                this.setCampo('status', this.state.FAILED);
            });
        },
        loadPeriodos: function(){
            axios.post(this.pathcifras + '/periodos').then(res => {
                let big_total = 0; //this.datos.reduce((acum, elm) => acum + elm.total, 0);
                let big_glosa = 0;
                let big_pagar = 0;
                let mnu = res.data.map(elm => {
                    big_total += elm.total;
                    big_glosa += elm.sum_glosas;
                    big_pagar += elm.sum_pagar;
                    return {_id: (elm._id == '')? '(vacío)': elm._id, 'count': elm.total, 'glosa': elm.sum_glosas, 'pago': elm.sum_pagar, 'items': elm.sum_fac};
                });
                this.$refs.gp_dual.setDatos(mnu);
                this.$refs.contador_1.setValor(big_total);
                this.$refs.contador_2.setValor(big_glosa);
                this.$refs.contador_3.setValor(big_pagar);
                this.$refs.por_1.setValor('100%');
                this.$refs.por_2.setValor(this.clearNumber((big_glosa / big_total) * 100) + '%')
                this.$refs.por_3.setValor(this.clearNumber((big_pagar / big_total) * 100) + '%')
            }).catch(err => {
                console.log(err);
            });
        },
        loadCifras: function(){
            let pam = new FormData();
            pam.append('depto', this.d_depto);
            pam.append('tcc', this.d_tcc);
            pam.append('auditor', this.d_audit);
            pam.append('nit', this.d_nit);
            pam.append('periodo', this.d_periodo);
            this.status = this.state.LOADING;
            this.setCampo('depto', this.d_depto);
            this.setCampo('tcc', this.d_tcc);
            this.setCampo('audit', this.d_audit);
            this.setCampo('nit', this.d_nit);
            this.setCampo('periodo', this.d_periodo);
            this.setCampo('status', this.state.LOADING);
            axios.post(this.pathcifras, pam).then(res => {
                let mnu = res.data[0].general.map(elm => {
                    return {_id: (elm._id == '')? '(vacío)': elm._id, 'count': elm.total, 'glosa': elm.sum_glosas, 'pago': elm.sum_pagar, 'items': elm.sum_fac};
                });
                this.$refs.gp_dual.setDatos(mnu);
                let repu = res.data[0].repu;
                // this.$refs.gp_1.setDatos(this.datos.map(elm => ({_id: elm.prestador.length > 45? elm.prestador.slice(0, 45) + '...': elm.prestador, 'count': elm.total})).sort((a, b) => a.total - b.total));
                // let dts = repu.map(elm => ({_id: elm.prestador.length > 45? elm.prestador.slice(0, 45) + '...': elm.prestador, 'count': elm.total})).sort((a, b) => a.count - b.count);
                let dts = repu.slice(0, 20).map(elm => {
                    return {_id: elm.prestador.length > 45? elm.prestador.slice(0, 45) + '...': elm.prestador, 'count': elm.total};
                }).sort((a, b) => a.count - b.count);
                this.$refs.gp_1.setDatos(dts);
                // this.$refs.gp_1.setDatos(repu.map(elm => ({_id: elm.prestador.length > 45? elm.prestador.slice(0, 45) + '...': elm.prestador, 'count': elm.total})).sort((a, b) => a.count - b.count));
                let big_total = 0; //this.datos.reduce((acum, elm) => acum + elm.total, 0);
                let big_glosa = 0;
                let big_pagar = 0;
                repu.forEach(elm => {
                    big_total += elm.total;
                    big_glosa += elm.sum_glosas;
                    big_pagar += elm.sum_pagar;
                });
                this.setCampo('data', repu);
                this.$refs.contador_1.setValor(this.clearNumber(big_total));
                this.$refs.contador_2.setValor(this.clearNumber(big_glosa));
                this.$refs.por_1.setValor('100%');
                this.$refs.por_2.setValor(this.customRounded(this.clearNumber((big_glosa / big_total) * 100)) + '%');
                let conci = res.data[0].concilia;
                if(conci.length > 0){
                    let xeps = this.clearNumber(conci[0].eps);
                    let xips = this.clearNumber(conci[0].ips);
                    this.$refs.contador_3.setValor(xeps);
                    this.$refs.contador_4.setValor(xips);
                    let aux = big_glosa - (conci[0].eps + conci[0].ips);
                    this.$refs.contador_5.setValor(this.clearNumber(aux));
                    this.$refs.por_3.setValor(this.customRounded(this.clearNumber((xeps / big_total) * 100)) + '%');
                    this.$refs.por_4.setValor(this.customRounded(this.clearNumber((xips / big_total) * 100)) + '%');
                    this.$refs.por_5.setValor(this.customRounded(this.clearNumber((aux / big_total) * 100)) + '%');
                    this.$refs.por_77.setValor(this.customRounded(this.clearNumber((xips / big_total) * 100)) + '%');
                }else{
                    this.$refs.contador_3.setValor("");
                    this.$refs.contador_4.setValor("");
                    this.$refs.contador_5.setValor("");
                    this.$refs.por_3.setValor("%");
                    this.$refs.por_4.setValor("%");
                    this.$refs.por_5.setValor("%");
                    this.$refs.por_77.setValor("%");
                }
                this.status = this.state.LOADED;
                this.setCampo('status', this.state.LOADED);
            }).catch(err => {
                console.log(err);
                this.status = this.state.FAILED;
                this.setCampo('status', this.state.FAILED);
            });
        },
        loadRegimen: function(){        // Now is event (tipo_contrato field)
            this.status = this.state.LOADING;
            this.setCampo('depto', this.d_depto);
            this.setCampo('tcc', this.d_tcc);
            this.setCampo('audit', this.d_audit);
            this.setCampo('nit', this.d_nit);
            this.setCampo('periodo', this.d_periodo);
            this.setCampo('status', this.state.LOADING);
            let pam = new FormData();
            pam.append('depto', this.d_depto);
            pam.append('tcc', this.d_tcc);
            pam.append('auditor', this.d_audit);
            pam.append('nit', this.d_nit);
            pam.append('periodo', this.d_periodo);
            axios.post(this.pathcifras + '/regimen', pam).then(res => {
                let rtn = res.data[0].repu;
                this.setCampo('data', rtn);
                this.setEvgroup(this.evgroup);
                this.setCampo('status', this.state.LOADED);
                this.status = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.setCampo('status', this.state.FAILED);
                this.status = this.state.FAILED;
            });
        },
        loadCase: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                this.pagina = 1;
                this.barSelect = '',
                this.hasNext = false;
                this.slicebar = [];
                this.status_bar = 'ini';
                this.setCampo('depto', this.d_depto);
                this.setCampo('tcc', this.d_tcc);
                this.setCampo('audit', this.d_audit);
                this.setCampo('nit', this.d_nit);
                this.setCampo('periodo', this.d_periodo);
                this.setCampo('status', this.state.LOADING);
                let pam = new FormData();
                pam.append('depto', this.d_depto);
                pam.append('tcc', this.d_tcc);
                pam.append('auditor', this.d_audit);
                pam.append('nit', this.d_nit);
                pam.append('periodo', this.d_periodo);
                axios.post(this.pathcifras + '/case', pam).then(res => {
                    let rtn = res.data[0].repu;
                    this.$refs.gp_case.setDatos(rtn);
                    this.setCampo('data', res.data);
                    this.setCampo('status', this.state.LOADED);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.setCampo('status', this.state.FAILED);
                    this.status = this.state.FAILED;
                });
            }
        },
        loadConciliacion: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                this.setCampo('depto', this.d_depto);
                this.setCampo('tcc', this.d_tcc);
                this.setCampo('audit', this.d_audit);
                this.setCampo('nit', this.d_nit);
                this.setCampo('periodo', this.d_periodo);
                this.setCampo('status', this.state.LOADING);
                let pam = new FormData();
                pam.append('depto', this.d_depto);
                pam.append('tcc', this.d_tcc);
                pam.append('auditor', this.d_audit);
                pam.append('nit', this.d_nit);
                pam.append('periodo', this.d_periodo);
                this.lastcon = {'nit': this.d_nit, 'periodo': this.d_periodo, 'prestador': this.d_nipre.prestador, 'status': this.state.LOADING};
                axios.post(this.pathcifras + '/conciliacion', pam).then(res => {
                    let rtn = res.data[0].repu;
                    let aux = {};
                    rtn.forEach(elm => {
                        if(aux[elm.prd] == undefined){
                            aux[elm.prd] = {'per': elm._id.per, 'ready': 0, 'pending': 0, 'glosado': 0};
                        }
                        if(elm._id.stt == 'Conciliado'){
                            aux[elm.prd].ready = elm.suma;
                        }else{
                            aux[elm.prd].pending = elm.suma;
                        }
                        aux[elm.prd].glosado += elm.suma;
                    });
                    console.log('voi aquí');
                    console.log(rtn);
                    // this.$refs.gp_concilia.setDatos(rtn);
                    if(this.lastcon.periodo == ''){
                        this.$refs.gp_two.setDatos(Object.values(aux));
                    }else{
                        this.$refs.gp_two.setDatos(Object.values(aux).sort((a, b) => b.pending - a.pending));
                    }
                    this.setCampo('data', res.data);
                    this.setCampo('status', this.state.LOADED);
                    this.status = this.state.LOADED;
                    this.lastcon.status = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.setCampo('status', this.state.FAILED);
                    this.status = this.state.FAILED;
                    this.lastcon.status = this.state.FAILED;
                });
            }
        },
        loadConcilioUnity: function(barra, page=1){
            if(this.status_slice != this.state.LOADING){
                this.status_slice = this.state.LOADING;
                let pam = new FormData();
                pam.append('depto', this.d_depto);
                pam.append('tcc', this.d_tcc);
                pam.append('pagina', page);
                pam.append('barra', barra);
                pam.append('auditor', this.d_audit);
                pam.append('nit', this.d_nit);
                pam.append('periodo', this.periodo_alt);
                this.pagina_alt = (page < 1)? 1: page;
                this.barSelect_alt = barra;
                axios.post(this.pathcifras + '/conciliacion/slice/bar', pam).then(res => {
                    this.slicecon = res.data[0].slice;
                    console.log('sheam');
                    console.log(this.slicecon);
                    this.hasNext_alt = this.slicecon.length > 50;
                    if(this.hasNext_alt) this.slicecon.pop();
                    this.status_slice = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status_slice = this.state.FAILED;
                });
            }
        },
        loadSliceBar: function(periodo, nit, barra){
            if(this.status_slice != this.state.LOADING){
                this.status_slice = this.state.LOADING;
                let pam = new FormData();
                pam.append('auditor', this.d_audit);
                pam.append('nit', nit);
                pam.append('periodo', periodo);
                let rbarra = (barra == 'ready')? 'Conciliado': 'Pendiente por conciliar';
                pam.append('barra', rbarra);
                // this.lastcon = {'nit': this.d_nit, 'periodo': this.d_periodo, 'prestador': this.d_nipre.prestador, 'status': this.state.LOADING};
                console.log('cargando slice!');
                axios.post(this.pathcifras + '/conciliacion/slice/bar', pam).then(res => {
                    this.slicedata = res.data[0].repu;
                    console.log('hakini');
                    console.log(this.slicedata);
                    // this.$refs.gp_two.setDatos(Object.values(aux));
                    this.status_slice = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status_slice = this.state.FAILED;
                });
            }
        },
        setItem: function(arg){
            if(this.status != this.state.LOADING){
                this.targetItem = arg;
                if(this.targetItem == 'cifras'){
                    if(this.subitem == 'general'){
                        // this.loadPeriodos();
                    }else{
                        // this.loadCifras();
                    }
                    this.loadCifras();
                }else{
                    if(this.targetItem == 'razon_social'){
                        this.loadSocial();
                    }else{
                        this.loadGroup();
                    }
                }
            }
        },
        setSubitem: function(arg){
            this.subitem = arg;
            // if(this.subitem == 'general'){
            //     this.loadPeriodos();
            // }else{
            //     this.loadCifras();
            // }
            this.loadCifras();
        },
        loadEntities: function(){
            // this.status = this.state.LOADING;
            this.ipss = [];
            this.tcc = [];
            axios.post(this.pathcifras + '/ipss').then(res => {
                this.tcc = res.data[0].tcc.map(elm => elm._id);
                this.deptos = res.data[0].deptos;
                res.data[0].ipss.forEach(elm => {
                    this.ipss.push({'nit': elm._id, 'prestador': elm.prestador});
                });
                res.data[0].auditores.forEach(elm => {
                    let aud = {'auditor': elm._id, 'valor': elm._id};
                    if(elm._id == ''){
                        aud = {'auditor': '(Sin auditor)', 'valor': '-void-'};
                    }
                    this.auditores.push(aud);
                });
                let tmp = {};
                res.data[0].times.forEach(elm => {
                    if(this.isEmpty(elm._id)){

                    }else{
                        let bi = elm._id.toString().split('-');
                        if(tmp[bi[0]] == undefined){
                            tmp[bi[0]] = {'anio': bi[0], 'meses': []};
                        }
                        tmp[bi[0]].meses.push({'tx': this.mss[parseInt(bi[1])], 'ym': elm._id, 'total': elm.total});
                    }
                });
                this.times = Object.values(tmp);
            }).catch(err => {console.log(err)});
        },
        isChange: function(){
            let pos = {'razon_social': 0, 'cifras': 1, 'tipo_regimen': 2, 'case': 3, 'conciliacion': 4};
            let tmp = this.opciones[pos[this.section]];
            if(this.d_depto == tmp.depto && this.d_tcc == tmp.tcc && this.d_nit == tmp.nit && this.d_periodo == tmp.periodo && this.d_audit == tmp.audit){
                return (tmp.status == this.state.LOADED)? false: true;
            }else{
                return true;
            }
        },
        setCampo: function(cmp, val){
            let pos = {'razon_social': 0, 'cifras': 1, 'tipo_regimen': 2, 'case': 3, 'conciliacion': 4};
            this.opciones[pos[this.section]][cmp] = val;
        },
        getCampo: function(sec, cmp){
            let pos = {'razon_social': 0, 'cifras': 1, 'tipo_regimen': 2, 'case': 3, 'conciliacion': 4};
            return this.opciones[pos[sec]][cmp];
        },
        manager: function(){
            if(this.status != this.state.LOADING){
                if(this.section == 'razon_social'){
                    if(this.isChange()){
                        this.loadSocial();
                    }
                }else if(this.section == 'cifras'){
                    if(this.isChange()){
                        this.loadCifras();
                    }
                }else if(this.section == 'tipo_regimen'){
                    if(this.isChange()){
                        this.loadRegimen();
                    }
                }else if(this.section == 'case'){
                    if(this.isChange()){
                        this.loadCase();
                    }
                }else if(this.section == 'conciliacion'){
                    if(this.isChange()){
                        this.loadConciliacion();
                    }
                }
            }
        },
        loadSelectBar: function(stt, page=1){
            if(this.status_bar != this.state.LOADING){
                this.status_bar = this.state.LOADING;
                let pam = new FormData();
                pam.append('depto', this.d_depto);
                pam.append('pagina', page);
                pam.append('tcc', this.d_tcc);
                pam.append('estado', stt);
                pam.append('auditor', this.d_audit);
                pam.append('nit', this.d_nit);
                pam.append('periodo', this.d_periodo);
                this.pagina = (page < 1)? 1: page;
                this.barSelect = stt;
                axios.post(this.pathcifras + '/case/select/bar', pam).then(res => {
                    this.slicebar = res.data[0].slice;
                    this.hasNext = this.slicebar.length > 50;
                    if(this.hasNext) this.slicebar.pop();
                    this.status_bar = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status_bar = this.state.FAILED;
                });
            }
        },
        listen: function(){
            this.$eventBus.$on('select-per', arg => {
                console.log(arg);
            });
            this.$eventBus.$on('bar-estado', evt => {
                this.loadSelectBar(evt._id, 1);
            });
            this.$eventBus.$on('concilio', arg => {
                console.log('Hello dispatcher');
                console.log(arg);
                this.periodo_alt = arg.per;
                this.loadConcilioUnity(arg.campo_valor, 1);
                // if(this.lastcon.status == this.state.LOADED){
                //     console.log('entró');
                //     this.loadSliceBar(arg.per, this.lastcon.nit, arg.campo_valor);
                // }
                // let prm = {'nit': this.d_nit, 'periodo': this.d_periodo, 'stt_fac': arg._id};
                // this.$eventBus.$emit('open-modal', {'titulo': 'ESTADO DE CONCILIACIÓN', 'periodo': null, 'params': prm, 'foco': 'estado_factura_conciliacion'});
            });
        }
    },
    mounted() {
        this.txtool = `
            [bold]{categoryX}[/]
            Facturacion: {valueY}
            Glosas: {glosa}
            Total a pagar: {pago}
            # de facturas: {items}`;
        this.$refs.gp_dual.lc_custom = this.txtool;
        // this.setItem('razon_social');
        this.listen();
        this.loadEntities();
        this.manager();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space:nowrap; text-align: center}
    .loading {opacity: .4}
    .bg-target.loading, .bg-custom.loading {cursor:wait !important}
    td.is-active {background: #2ECD99 !important; color: #FFF !important}
    .opaco {opacity: 0.4 !important}
    .df-hand {cursor: default; user-select: none}
    .df-muted {user-select: none !important; pointer-events: none !important; opacity: .3 !important}

    .bg-target {cursor:pointer; background:#F0C541; padding:14px 20px; color:#FFF !important}
    .bg-custom {cursor:pointer; background:#DEDEDE; padding:14px 20px}
    .bg-custom + .bg-custom {border-left:1px solid #FEFEFE}
    .bg-custom:hover {background: #DEDEDEAA}
    .lc-icon {display:inline-block; width:35px !important; height:35px !important; background:#FFF; color:#8F908F; border-radius:50% !important}
    .lc-icon > i {font-size:16px}
</style>
