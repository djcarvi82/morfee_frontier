<template>
    <div>
        <div class="panel panel-default card-view border" v-if="enable_controls">
            <div class="panel-wrapper collapse in">
                <div  class="panel-body">
                    <!-- ***************** -->
                    <!-- CONTROLES SECTION -->
                    <!-- ***************** -->
                    <div v-if="enable_controls && hot_status && 'CALOR' == getTriangleInfo('code')">
                        <!-- TABLA DE CONTROL OCULTA -->
                        <div class="table-responsive">
                            <table class="table table-bordered mt-4">
                                <thead>
                                    <tr>
                                        <th class="cel-hide py-2"></th>
                                        <th class="df-grey text-bold fs-5 py-2" v-for="(per, i) in periodos" :key="i">{{ i + 1 }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(elm, i) in pridata" :key="i">
                                        <td class="colmin df-grey py-2">{{ elm.tx }}</td>
                                        <td class="py-2" v-for="(rad, r) in periodos" :key="r">{{ clearNumber(getDataMM(rad.num, elm.src), 4) }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- End table-responsive -->
                        <!-- TABLA IBNR promedio -->
                        <div class="table-responsive mt-4">
                            <table class="table table-bordered">
                                <thead>
                                    <tr class="bg-primary"><th class="text-center text-bold fs-5 py-2" style="color:#FFF !important" colspan="6">IBNR PROMEDIO</th></tr>
                                    <tr class="df-grey">
                                        <th class="py-2">PERIODO DE PRESTACIÓN</th>
                                        <th class="py-2">PERIODO DE DESARROLLO</th>
                                        <th class="py-2">PRESTACIONES ACUMULADAS</th>
                                        <th class="py-2">FDA PROMEDIO</th>
                                        <th class="py-2">ÚLTIMA PRESTACIÓN ESPERADA</th>
                                        <th class="py-2">UPE-PA</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(per, i) in periodos" :key="i">
                                        <td class="py-1">{{ per.num }}</td>
                                        <td class="py-1 text-center">{{ 36 - i }}</td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- End table-responsive -->
                        <div class="table-responsive mt-4">
                            <table class="table table-bordered">
                                <thead>
                                    <tr class="bg-primary"><th class="text-center text-bold fs-5 py-2" style="color:#FFF !important" colspan="6">IBNR CHAIN LADDER</th></tr>
                                    <tr class="df-grey">
                                        <th class="py-2">PERIODO DE PRESTACIÓN</th>
                                        <th class="py-2">PERIODO DE DESARROLLO</th>
                                        <th class="py-2">PRESTACIONES ACUMULADAS</th>
                                        <th class="py-2">FDA CHAIN LADDER</th>
                                        <th class="py-2">ÚLTIMA PRESTACIÓN ESPERADA</th>
                                        <th class="py-2">UPE-PA</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(per, i) in periodos" :key="i">
                                        <td class="py-1">{{ per.num }}</td>
                                        <td class="py-1 text-center">{{ 36 - i }}</td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- End table-responsive -->
                        <div class="table-responsive mt-4">
                            <table class="table table-bordered">
                                <thead>
                                    <tr class="bg-primary"><th class="text-center text-bold fs-5 py-2" style="color:#FFF !important" colspan="6">IBNR MIN</th></tr>
                                    <tr class="df-grey">
                                        <th class="py-2">PERIODO DE PRESTACIÓN</th>
                                        <th class="py-2">PERIODO DE DESARROLLO</th>
                                        <th class="py-2">PRESTACIONES ACUMULADAS</th>
                                        <th class="py-2">FDA MIN</th>
                                        <th class="py-2">ÚLTIMA PRESTACIÓN ESPERADA</th>
                                        <th class="py-2">UPE-PA</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(per, i) in periodos" :key="i">
                                        <td class="py-1">{{ per.num }}</td>
                                        <td class="py-1 text-center">{{ 36 - i }}</td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- End table-responsive -->
                        <div class="table-responsive mt-4">
                            <table class="table table-bordered">
                                <thead>
                                    <tr class="bg-primary"><th class="text-center text-bold fs-5 py-2" style="color:#FFF !important" colspan="6">IBNR MAX</th></tr>
                                    <tr class="df-grey">
                                        <th class="py-2">PERIODO DE PRESTACIÓN</th>
                                        <th class="py-2">PERIODO DE DESARROLLO</th>
                                        <th class="py-2">PRESTACIONES ACUMULADAS</th>
                                        <th class="py-2">FDA MAX</th>
                                        <th class="py-2">ÚLTIMA PRESTACIÓN ESPERADA</th>
                                        <th class="py-2">UPE-PA</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(per, i) in periodos" :key="i">
                                        <td class="py-1">{{ per.num }}</td>
                                        <td class="py-1 text-center">{{ 36 - i }}</td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- End table-responsive -->
                        <div class="table-responsive mt-4">
                            <table class="table table-bordered">
                                <thead>
                                    <tr class="bg-primary"><th class="text-center text-bold fs-5 py-2" style="color:#FFF !important" colspan="6">IBNR PROM -MIN -MAX</th></tr>
                                    <tr class="df-grey">
                                        <th class="py-2">PERIODO DE PRESTACIÓN</th>
                                        <th class="py-2">PERIODO DE DESARROLLO</th>
                                        <th class="py-2">PRESTACIONES ACUMULADAS</th>
                                        <th class="py-2">FDA PROM -MIN -MAX</th>
                                        <th class="py-2">ÚLTIMA PRESTACIÓN ESPERADA</th>
                                        <th class="py-2">UPE-PA</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(per, i) in periodos" :key="i">
                                        <td class="py-1">{{ per.num }}</td>
                                        <td class="py-1 text-center">{{ 36 - i }}</td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                        <td class="py-1"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </div><!-- End table-responsive -->
                    </div><!-- End controles section -->
                </div>
            </div>
        </div>
        <div :class="enable_controls? 'd-none': 'row mb-4'">
            <div class="col-sm-6">
                <div :class="status + '-wait'">
                    <div class="form-group mb-0">
                        <div class="input-group">
                            <select class="form-control" v-model="targetPeriodoDB" :disabled="hasAnyData()">
                                <option :value="null">Seleccione el periodo de corte de la base de datos:</option>
                                <optgroup :label="elm.anio" v-for="(elm, i) in periodos_select" :key="i">
                                    <option :value="mes" v-for="(mes, k) in elm.meses" :key="k">{{ mes.tx }} de {{ elm.anio }}</option>
                                </optgroup>
                            </select>
                            <div class="input-group-btn">
                                <button class="btn btn-success" :disabled="!hasAnyData()" @click="preReset"><i class="fa fa-refresh"></i></button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <load-and-time ref="timer" :pathsearch="pathsearch"></load-and-time>
            </div>
        </div>
        <div :class="enable_controls? 'd-none': 'row'">
            <div class="col-lg-3 col-md-3 col-sm-3 col-xs-12">
                <div :class="getClassHeading('aut')">
                    <div class="panel-heading py-3">
                        <h6 class="panel-title txt-light">AUTORIZACIONES</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div :class="getClassGroupList('aut')">
                                <a href="javascript:void(0)" :class="elm.code == getTriangleInfo('code')? 'list-group-item focus-item': 'list-group-item'" v-for="(elm, i) in status_src.aut.list" :key="i" @click="setTriangle(elm)">
                                    <div class="d-flex align-items-center">
                                        <i :class="getIcon('aut')"></i>
                                        <div>
                                            {{ elm.title }}
                                            <span class="block txt-grey">Descripción</span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="d-flex align-items-center mx-3 mb-3" v-if="status_src.aut.status == state.LOADING">
                                <i class="fa fa-spinner fa-spin fs-3 me-2"></i>
                                <span>Cargando autorizaciones...</span>
                            </div>
                            <div class="my-3 mx-3 text-center" v-if="status_src.aut.load">
                                <button class="btn btn-primary" @click="loadBridge('aut', true)" :disabled="status_src.aut.status == state.LOADING">Recargar datos</button>
                            </div>
                            <div class="alert alert-warning mb-0" v-if="isEmptyDB('aut')">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-warning me-2"></i>
                                    <span>No hay registros en la base datos para el periodo seleccionado!</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!-- End card-view -->
            </div><!-- End col-sm-3 -->
            <div class="col-lg-3 col-md-3 col-sm-3 col-xs-12">
                <div :class="getClassHeading('fac')">
                    <div class="panel-heading py-3">
                        <h6 class="panel-title txt-light">FACTURAS</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div :class="getClassGroupList('fac')">
                                <a href="javascript:void(0)" :class="elm.code == getTriangleInfo('code')? 'list-group-item focus-item': 'list-group-item'" v-for="(elm, i) in status_src.fac.list" :key="i" @click="setTriangle(elm)">
                                    <div class="d-flex align-items-center">
                                        <i :class="getIcon('fac')"></i>
                                        <div>
                                            {{ elm.title }}
                                            <span class="block txt-grey">Descripción</span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="d-flex align-items-center mx-3 mb-3" v-if="status_src.fac.status == state.LOADING">
                                <i class="fa fa-spinner fa-spin fs-3 me-2"></i>
                                <span>Cargando facturas...</span>
                            </div>
                            <div class="my-3 mx-3 text-center" v-if="status_src.fac.load">
                                <button class="btn btn-primary" @click="loadBridge('fac', true)" :disabled="status_src.fac.status == state.LOADING">Recargar datos</button>
                            </div>
                            <div class="alert alert-warning mb-0" v-if="isEmptyDB('fac')">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-warning me-2"></i>
                                    <span>No hay registros en la base datos para el periodo seleccionado!</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!-- End card-view -->
            </div><!-- End col-sm-3 -->
            <div class="col-lg-3 col-md-3 col-sm-3 col-xs-12">
                <div :class="getClassHeading('pag')">
                    <div class="panel-heading py-3">
                        <h5 class="panel-title txt-light">PAGOS</h5>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div :class="getClassGroupList('pag')">
                                <a href="javascript:void(0)" :class="elm.code == getTriangleInfo('code')? 'list-group-item focus-item': 'list-group-item'" v-for="(elm, i) in status_src.pag.list" :key="i" @click="setTriangle(elm)">
                                    <div class="d-flex align-items-center">
                                        <i :class="getIcon('pag')"></i>
                                        <div>
                                            {{ elm.title }}
                                            <span class="block txt-grey">Descripción</span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                            <div class="d-flex align-items-center mx-3 mb-3" v-if="status_src.pag.status == state.LOADING">
                                <i class="fa fa-spinner fa-spin fs-3 me-2"></i>
                                <span>Cargando pagos...</span>
                            </div>
                            <div class="my-3 mx-3 text-center" v-if="status_src.pag.load">
                                <button class="btn btn-primary" @click="loadBridge('pag', true)" :disabled="status_src.pag.status == state.LOADING">Recargar datos</button>
                            </div>
                            <div class="alert alert-warning m-2" v-if="isEmptyDB('pag')">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-warning me-2"></i>
                                    <span>No hay registros en la base datos para el periodo seleccionado!</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!-- End card-view -->
            </div><!-- End col-sm-3 -->
            <div class="col-lg-3 col-md-3 col-sm-3 col-xs-12">
                <div :class="status_src.all.load? 'panel panel-success card-view': 'panel panel-inverse card-view loading-solid'">
                    <div class="panel-heading py-3">
                        <h5 class="panel-title txt-light">CONSOLIDADO</h5>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div :class="status_src.all.load? 'list-group mb-0': 'list-group mb-0 loading'">
                                <a href="javascript:void(0)" :class="elm.code == getTriangleInfo('code')? 'list-group-item focus-item': 'list-group-item'" v-for="(elm, i) in status_src.all.list" :key="i" @click="setTriangle(elm)">
                                    <div class="d-flex align-items-center">
                                        <i :class="getIcon('all')"></i>
                                        <div>
                                            {{ elm.title }}
                                            <span class="block txt-grey">Descripción</span>
                                        </div>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div><!-- End card-view -->
            </div><!-- End col-sm-3 -->
        </div><!-- End row -->

        <!-- ************** -->
        <!-- SECTION TABLES -->
        <!-- ************** -->
        <div class="panel panel-default card-view border" v-if="isLoadTriangle(getTriangleInfo('ori'))">
            <div class="panel-wrapper collapse in">
                <div  class="panel-body">
                    <div class="d-flex align-items-center">
                        <i class="fa fa-spinner fa-spin fs-3 me-2"></i>
                        <span>Cargando fuente de datos...</span>
                    </div>
                </div>
            </div>
        </div>
        <div :class="enable_controls? 'd-none': 'panel panel-default card-view border'" v-else-if="getTriangleInfo('ori') != ''">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <div>
                        <h5 class="panel-title txt-dark fs-4 mb-0">{{ getTriangleInfo('fulltitle') }}</h5>
                        <div>{{ str_periodo }}</div>
                    </div>
                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div  class="panel-body">
                    <div>
                        <div class="btn-group me-4">
                            <button :class="f_filtro == 'pbs'? 'btn btn-primary': 'btn btn-default'" @click="setFilter('pbs')">PBS</button>
                            <button :class="f_filtro == 'pm'? 'btn btn-primary': 'btn btn-default'" @click="setFilter('pm')">PM</button>
                            <button :class="f_filtro == 'pac'? 'btn btn-primary': 'btn btn-default'" @click="setFilter('pac')">PAC</button>
                            <button :class="f_filtro == 'all'? 'btn btn-primary': 'btn btn-default'" @click="setFilter('all')">TODAS</button>
                        </div>
                        <button :class="f_guia? 'btn btn-primary': 'btn btn-default'" :disabled="getTriangleInfo('code') == 'AUT_2'" type="button" @click="f_guia = !f_guia">GUÍA</button>
                    </div>
                    <div v-if="getTriangleInfo('code') == 'AUT_2'">
                        <table class="table table-min table-bordered mt-4">
                            <thead>
                                <tr>
                                    <th class="cel-hide" colspan="2"></th>
                                    <th class="df-grey text-bold">1</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(pre, i) in periodos" :key="i">
                                    <td class="colmin df-grey text-bold">{{ i + 1 }}</td>
                                    <td class="colmin df-grey text-bold">{{ pre.num }}</td>
                                    <td :class="getClass(pre.num, pre.num) + ' text-center colmin'" @click="openCell(pre.num, pre.num, i + 1, '', getTriangleInfo('ori'))">{{ getValor(pre.num, pre.num, getTriangleInfo('ori')) }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="mt-4" v-else>
                        <div class="table-responsive">
                            <table class="table table-bordered">
                                <thead v-if="getTriangleInfo('head') == 'num'">
                                    <tr>
                                        <th class="cel-hide py-2" colspan="2"></th>
                                        <th class="df-grey text-bold fs-5 py-2" v-for="(per, i) in periodos" :key="i">{{ i + 1 }}</th>
                                    </tr>
                                </thead>
                                <thead v-else>
                                    <tr>
                                        <th class="cel-hide" colspan="2"></th>
                                        <th class="df-grey text-bold" v-for="(per, i) in periodos" :key="i">{{ per.num }}</th>
                                    </tr>
                                </thead>
                                <tbody :class="f_guia? 'df-guia': ''" v-if="'DESARROLLO' == getTriangleInfo('code')">
                                    <tr :class="'triangle-' + getTriangleInfo('align')" v-for="(pre, i) in periodos" :key="i">
                                        <td class="colmin df-grey text-bold">{{ i + 1 }}</td>
                                        <td class="colmin df-grey text-bold">{{ pre.num }}</td>
                                        <td :class="getClass(pre.num, rad.num) + ' text-center df-rel'" @click="openCellAcum(pre.num, rad.num, i + 1, (k + 1) - i)" v-for="(rad, k) in periodos" :key="k">
                                            {{ clearNumber(getValorAcumHot(pre.num, rad.num)) }}
                                            <div class="info-left">{{ pre.num }}</div>
                                            <div class="info-top">{{ getTriangleInfo('head') == 'num'? (k + 1) - i: rad.num }}</div>
                                        </td>
                                    </tr>
                                </tbody>
                                <tbody :class="f_guia? 'df-guia': ''" v-else-if="'CALOR' == getTriangleInfo('code')">
                                    <tr :class="'triangle-' + getTriangleInfo('align')" v-for="(pre, i) in periodos" :key="i">
                                        <td class="colmin df-grey text-bold">{{ i + 1 }}</td>
                                        <td class="colmin df-grey text-bold">{{ pre.num }}</td>
                                        <td :class="getClass(pre.num, rad.num) + ' text-center df-rel'" :title="getValorAcumFac(pre.num, rad.num)" @click="openCellAcum(pre.num, rad.num, i + 1, (k + 1) - i)" v-for="(rad, k) in periodos" :key="k">
                                            {{ clearNumber(getValorAcumFac(pre.num, rad.num), 4) }}
                                            <div class="info-left">{{ pre.num }}</div>
                                            <div class="info-top">{{ getTriangleInfo('head') == 'num'? (k + 1) - i: rad.num }}</div>
                                        </td>
                                    </tr>
                                </tbody>
                                <tbody :class="f_guia? 'df-guia': ''" v-else>
                                    <tr :class="'triangle-' + getTriangleInfo('align')" v-for="(pre, i) in periodos" :key="i">
                                        <td class="colmin df-grey text-bold">{{ i + 1 }}</td>
                                        <td class="colmin df-grey text-bold">{{ pre.num }}</td>
                                        <td :class="getClass(pre.num, rad.num) + ' text-center df-rel'" @click="openCell(pre.num, rad.num, i + 1, (k + 1) - i, getTriangleInfo('ori'))" v-for="(rad, k) in periodos" :key="k">
                                            {{ getValor(pre.num, rad.num, getTriangleInfo('ori')) }}
                                            <div class="info-left">{{ pre.num }}</div>
                                            <div class="info-top">{{ getTriangleInfo('head') == 'num'? (k + 1) - i: rad.num }}</div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div><!-- End panel-body -->
            </div><!-- End panel-wrapper -->
        </div><!-- End card-view -->

        <!-- *********************** -->
        <!-- SECTION MODAL DATA CELL -->
        <!-- *********************** -->
        <div id="lc_modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" style="display: none;">
            <div :class="type_cell == 'acum'? 'modal-dialog modal-lg': 'modal-dialog modal-lgx'">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h5 class="modal-title" id="myLargeModalLabel">CONTENIDO DE LA CELDA</h5>
                    </div>
                    <div class="modal-body">
                        <div class="d-flex justify-content-center mt-4">
                            <table class="table table-minx table-bordered">
                                <thead v-if="!isEmpty(targetCellRef.col)">
                                    <tr>
                                        <th class="cel-hide" colspan="2"></th><th class="df-grey">{{ getTriangleInfo('head') == 'num'? targetCellRef.col: targetCellRef.rad }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td class="colmin df-grey">{{ targetCellRef.row }}</td>
                                        <td class="colmin df-grey">{{ targetCellRef.pre }}</td>
                                        <td :class="getClass(targetCellRef.pre, targetCellRef.rad) + ' text-center'" v-if="type_cell == 'acum'">{{ value_cell }}</td>
                                        <td :class="getClass(targetCellRef.pre, targetCellRef.rad) + ' text-center'" v-else>{{ getValor(targetCellRef.pre, targetCellRef.rad, targetCellRef.origen) }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-if="type_cell == 'normal'">
                            <div class="d-flex justify-content-between mt-4" v-if="targetCellRef.origen != 'all'">
                                <button :class="targetCellRef.origen == 'aut'? 'btn btn-primary flex-fill': 'btn btn-default flex-fill'" @click="targetCellRef.origen = 'aut'">Autorizaciones</button>
                                <button :class="targetCellRef.origen == 'fac'? 'btn btn-primary flex-fill': 'btn btn-default flex-fill'" @click="targetCellRef.origen = 'fac'">Facturas</button>
                                <button :class="targetCellRef.origen == 'pag'? 'btn btn-primary flex-fill': 'btn btn-default flex-fill'" @click="targetCellRef.origen = 'pag'">Pagos</button>
                            </div>
                            <div class="alert alert-danger mt-4" v-if="verifyLoad(targetCellRef.origen) == false">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-info-circle fs-3 me-2"></i>
                                    <span>No se ha cargado esta fuente de datos!</span>
                                </div>
                            </div>
                            <div class="alert alert-warning mt-4" v-else-if="targetCell.length == 0">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-info-circle fs-3 me-2"></i>
                                    <span>No hay datos en esta celda!</span>
                                </div>
                            </div>
                            <table class="table mt-4" v-else>
                                <thead>
                                    <tr class="text-bold"><th>Fuente</th><th>Tipo</th><th class="text-center">Valor</th></tr>
                                </thead>
                                <tbody v-if="targetCellRef.origen == 'all'">
                                    <tr v-for="(elm, i) in targetCell" :key="i">
                                        <td>{{ fuentes_tx[elm.origen] }}</td>
                                        <td>{{ elm.tipo }}</td>
                                        <td class="text-right">{{ clearNumber(elm.valor) }}</td>
                                    </tr>
                                    <tr class="text-bold" v-if="targetCell.length > 0">
                                        <td colspan="2">TOTAL</td>
                                        <td class="text-right">{{ clearNumber(targetCell.reduce((ac, elm) => ac + elm.valor, 0)) }}</td>
                                    </tr>
                                </tbody>
                                <tbody v-else>
                                    <tr :class="elm.origen == targetCellRef.origen? '': 'd-none'" v-for="(elm, i) in targetCell" :key="i">
                                        <td>{{ fuentes_tx[elm.origen] }}</td>
                                        <td>{{ elm.tipo }}</td>
                                        <td class="text-right">{{ clearNumber(elm.valor) }}</td>
                                    </tr>
                                    <tr class="text-bold" v-if="targetCell.length > 0">
                                        <td colspan="2">TOTAL</td>
                                        <td class="text-right">{{ clearNumber(targetCell.filter(elm => elm.origen == targetCellRef.origen).reduce((ac, elm) => ac + elm.valor, 0)) }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div v-if="type_cell == 'acum'">
                            <table class="table mt-4">
                                <thead>
                                    <tr>
                                        <th>Periodo</th>
                                        <th>FILTRO</th>
                                        <th class="text-center">Autorizaciones</th>
                                        <th class="text-center">Facturas</th>
                                        <th class="text-center">Pagos</th>
                                        <th class="text-center">TOTAL</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(elm, i) in targetCell" :key="i">
                                        <td class="text-center">{{ elm.i }}</td>
                                        <td>{{ filtro_tx[f_filtro] }}</td>
                                        <td class="text-center">{{ clearNumber(elm.aut) }}</td>
                                        <td class="text-center">{{ clearNumber(elm.fac) }}</td>
                                        <td class="text-center">{{ clearNumber(elm.pag) }}</td>
                                        <td class="text-center">{{ clearNumber(elm.aut + elm.fac + elm.pag) }}</td>
                                    </tr>
                                    <tr>
                                        <th class="text-bold" colspan="5">TOTAL:</th><th class="text-center text-bold">{{ value_cell }}</th>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div><!-- End modal-body -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger text-left" data-dismiss="modal">Cancelar</button>
                    </div>
                </div><!-- /.modal-content -->
            </div><!-- /.modal-dialog -->
        </div>        
        <!-- End modal -->        
    </div>
</template>
<script>
import axios from 'axios';

export default {
    props: {
        pathsearch: {type: String, default: ''},
        pathperiodos: {type: String, default: ''},
        pathfuente: {type: String, default: ''},
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''},
        cliente: {type: String, default: ''},
        clientetx: {type: String, default: ''}
    },
    data() {
        return {
            mss: ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            mssi: ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            col_asc: ["#F8696B","#F8766D","#F98370","#FA9072","#FA9D75","#FBAA77","#FCB77A","#FCC47C","#FDD17F","#FEDE81","#FFEB84","#F0E784","#E0E383","#D1DE82","#C1D981","#B1D580","#A2D07F","#92CC7E","#83C77D","#73C37C","#63BE7B"],
            col_desc: ["#63BE7B","#73C37C","#83C77D","#92CC7E","#A2D07F","#B1D580","#C1D981","#D1DE82","#E0E383","#F0E784","#FFEB84","#FEDE81","#FDD17F","#FCC47C","#FCB77A","#FBAA77","#FA9D75","#FA9072","#F98370","#F8766D","#F8696B"],
            pridata: [
                {'tx': 'FD PROMEDIO', 'src': 'calc_01'},
                {'tx': 'FDA PROM', 'src': 'calc_02'},
                {'tx': 'MIN', 'src': 'min'},
                {'tx': 'FDA MIN', 'src': ''},
                {'tx': 'MAX', 'src': 'max'},
                {'tx': 'FDA MAX', 'src': ''},
                {'tx': 'CHAIN LADDER', 'src': ''},
                {'tx': 'FDA CH.LADDER', 'src': ''},
                {'tx': 'PROM SIN MIN SIN MAX', 'src': ''},
                {'tx': 'FDA PROM - MIN - MAX', 'src': ''},
                {'tx': 'PROM ÚLTIMO AÑO', 'src': ''},
                {'tx': 'PROM ÚLTIMS DOS AÑOS', 'src': ''},
            ],
            fun_dymclass: () => true,
            fuente: (this.cliente == '0')? 'retec_facturas_0': this.cliente + '_retec_facturas',
            fuentes: {
                'aut': this.cliente + '_retec_autorizacion', 
                'fac': this.cliente + '_retec_facturas', 
                'pag': this.cliente + '_retec_pagos'
            },
            fuentes_tx: {'aut': 'Autorizaciones', 'fac': 'Facturas', 'pag': 'Pagos'},
            from: '',
            to: '',
            periodos: [],   // {num: 202303, anio: 2023, mes: 03, tx: 'Marzo'}
            periodos_db: [],    // {num: 202303, anio: 2023, mes: 03, tx: 'Marzo', match: {aut: false, fac: false, pag: false}}
            periodos_select: [],
            per_first: 0,
            per_last: 0,
            targetPeriodoDB: null,
            targetFuente: '',
            targetTriangle: null,
            f_guia: true,
            f_filtro: 'all',    // pbs | pm | pac | all
            filtro_tx: {'all': 'TODAS', 'pbs': 'PBS', 'pm': 'PM', 'pac': 'PAC'},
            fun_filter: (tipo) => true,

            // Modal
            type_cell: 'normal',    // normal | acum
            value_cell: 0,
            targetCellRef: {'pre': '', 'rad': '', 'row': '', 'col': '', 'origen': 'all'},
            targetCell: [],
            warnings: {'aut': [], 'fac': [], 'pag': []},

            anio: '',
            mes: '',
            show_head: true,
            f_periodo: '',
            f_cross: 'bg-cruce',
            f_in: 'bg-in',
            f_out: 'bg-danger',
            f_left: '',
			datos: [],
            hash: {},
            rcol: [],
            akey: [],
            head: [],
            sumcol: {},
            hot_acum: {},
            hot_fac: {},
            hot_mm: {},
            hot_status: false,
            enable_controls: false,
            status: 'ini',
            status_per: 'ini',
            status_src: {
                'aut': {'info': false, 'load': false, 'status': 'ini', 'list': [
                    {'fulltitle': 'AUTORIZACIONES - TRIÁNGULO INCREMENTAL', 'title': 'TRIÁNGULO INCREMENTAL', 'code': 'AUT_1', 'align': 'normal', 'ori': 'aut', 'head': 'code'},
                    {'fulltitle': 'AUTORIZACIONES - TRIÁNGULO DE DESARROLLO', 'title': 'TRIÁNGULO DE DESARROLLO', 'code': 'AUT_2', 'align': 'unique', 'ori': 'aut', 'head': 'num'},
                ]},
                'fac': {'info': false, 'load': false, 'status': 'ini', 'list': [
                    {'fulltitle': 'FACTURAS - TRIÁNGULO INCREMENTAL', 'title': 'TRIÁNGULO INCREMENTAL', 'code': 'FAC_1', 'align': 'normal', 'ori': 'fac', 'head': 'code'},
                    {'fulltitle': 'FACTURAS - TRIÁNGULO DE DESARROLLO', 'title': 'TRIÁNGULO DE DESARROLLO', 'code': 'FAC_2', 'align': 'left', 'ori': 'fac', 'head': 'num'},
                ]},
                'pag': {'info': false, 'load': false, 'status': 'ini', 'list': [
                    {'fulltitle': 'PAGOS - TRIÁNGULO INCREMENTAL', 'title': 'TRIÁNGULO INCREMENTAL', 'code': 'PAG_1', 'align': 'normal', 'ori': 'pag', 'head': 'code'},
                    {'fulltitle': 'PAGOS - TRIÁNGULO DE DESARROLLO', 'title': 'TRIÁNGULO DE DESARROLLO', 'code': 'PAG_2', 'align': 'left', 'ori': 'pag', 'head': 'num'},
                ]},
                'all': {'info': false, 'load': false, 'status': 'ini', 'list': [
                    {'fulltitle': 'TRIÁNGULO DE DESARROLLO ACUMULADO', 'title': 'TRIÁNGULO DE DESARROLLO ACUMULADO', 'code': 'DESARROLLO', 'align': 'left', 'ori': 'all', 'head': 'num'}, 
                    {'fulltitle': 'TRIÁNGULO DE FACTORES DE DESARROLLO', 'title': 'TRIÁNGULO DE FACTORES DE DESARROLLO', 'code': 'CALOR', 'align': 'left', 'ori': 'all', 'head': 'num'}
                ]},
                'crx': null
            },
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    watch: {
        targetPeriodoDB: function(val){
            this.targetFuente = '';
        }
    },
    computed: {
        str_periodo: function(){
            if(this.isEmpty(this.status_src.crx)){
                return '';
            }
            let y = String(this.status_src.crx).slice(0, 4);
            let m = String(this.status_src.crx).slice(-2);
            return this.mssi[parseInt(m)] + ' de ' + y;
        }
    },
    methods: {
        getDataMM: function(ym, atr){
            if(atr == '' || [undefined, null].includes(this.hot_mm[ym])){
                return '';
            }
            if(atr == 'calc_01'){
                // SUMA(C5:C39)/(35-C4+1)
                return this.hot_mm[ym].suma / (35 - this.hot_mm[ym].periodo);
            }
            return this.hot_mm[ym][atr];
        },
        switchControl: function(){
            window.addEventListener('keydown', e => {
                if(e.key === 'F4'){
                    if(this.hot_status && 'CALOR' == this.getTriangleInfo('code')){
                        this.enable_controls = !this.enable_controls;
                    }else{
                        this.enable_controls = false;
                    }
                }
            });
        },
        isEmpty: function(arg){
            return ['', undefined, null].includes(arg);
        },
        hasAnyData: function(){
            let rs = false;
            if(this.status_src.crx != null){
                ['aut', 'fac', 'pag'].forEach(elm => {
                    if(rs == false){
                        if(this.status_src[elm].load){
                            rs = true;
                        }
                    }
                });
            }
            return rs;
        },
        getClassBtn: function(arg){
            if(this.targetPeriodoDB == null){
                return 'btn btn-default';
            }
            return this.targetPeriodoDB.match[arg]? 'btn btn-success': 'btn btn-danger';
        },
        getClassHeading: function(arg){
            if(this.targetPeriodoDB == null){
                return 'panel panel-inverse card-view';
            }
            return this.targetPeriodoDB.match[arg]? 'panel panel-success card-view': 'panel panel-danger card-view loading-solid';
        },
        isEmptyDB: function(arg){
            if(this.targetPeriodoDB == null){
                return false;
            }
            return this.targetPeriodoDB.match[arg]? false: true;
        },
        getClassGroupList: function(arg){
            if(this.targetPeriodoDB == null){
                return 'list-group mb-0 loading';
            }
            if(this.targetPeriodoDB.match[arg]){
                if(this.status == this.state.LOADING && this.status_src[arg].load == false){
                    return 'list-group mb-0 loading';
                }
                return 'list-group mb-0';
            }else{
                return 'list-group mb-0 loading';
            }
        },
        isDisabledFuente: function(arg){
            if(this.targetPeriodoDB == null){
                return true;
            }else{
                return this.targetPeriodoDB.match[arg]? false: true;
            }
        },
        getClass: function(r, c){
            // if(r == c){
            //     return this.f_cross;
            // }
            // return (c < r)? this.f_out + this.f_left: this.f_in;
            return this.fun_dymclass(r, c);
        },
        getColorCell: function(r, c){
            // let azar = parseInt(Math.random() * 21);
            let tm = this.hot_col[`${r}_${c}`];
            return tm;
            // return 'bg-' + azar;
        },
        getIcon: function(src){
            if(this.status_src[src].load){
                return 'fa fa-check me-2 fs-5 txt-success';
            }else{
                return 'fa fa-download me-2 fs-5';
                // return 'fa fa-circle me-2 fs-5';
            }
        },
        getColor: function(per, sentido=true){
            let num = Math.round(per * 20);
            if(num > 20) num = 20;
            if(num < 0) num = 0;
            return sentido? this.col_asc[num]: this.col_desc[num];
        },
        verifyLoad: function(arg){
            if(['aut', 'fac', 'pag', 'all'].includes(arg)){
                return this.status_src[arg].load;
            }
            return false;
        },
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        getSumColumn: function(col, tipo){
            if(this.sumcol[col] == undefined){
                this.sumcol[col] = {'pac': 0, 'pbs': 0, 'pm': 0, 'all': 0};
                this.periodos.forEach(elm => {
                    let ref = elm.num + '_' + col;
                    this.hash[ref].forEach(arg => {
                        this.sumcol[col][arg.tipo] += arg.valor;
                        this.sumcol[col].all += arg.valor;
                    });
                });
            }
            return this.sumcol[col][tipo];
        },
        clearNumber: function(num, len=2){
            if(num % 1 == 0){
                return this.formatMiles(num);
            }else{
                return this.formatMiles(parseFloat(num).toFixed(len));
            }
        },
        getMes: function(ym){
            let m = parseInt(ym.toString().slice(-2));
            return this.mss[m];
        },
        resetHotData: function(){
            this.hot_status = false;
            this.hot_acum = {};
            this.hot_fac = {};
            this.hot_mm = {};
            this.hot_col = {};
            let back = 0;
            let per01 = this.periodos[0].num;
            this.periodos.forEach(pre => {
                this.periodos.forEach(rad => {
                    this.hot_acum[`${pre.num}_${rad.num}`] = this.getValorAcum(pre.num, rad.num).valor;
                });
            });
            this.periodos.forEach((pre, pi) => {
                this.periodos.slice(pi).forEach((rad, ri) => {
                    let ranum = this.periodos[ri].num;
                    let tm1 = `${pre.num}_${rad.num}`;
                    if(ri == 0){
                        this.hot_fac[tm1] = '';
                    }else{
                        back = this.periodos[(ri - 1) + pi].num
                        let tm0 = `${pre.num}_${back}`;
                        if(this.hot_acum[tm1] >= this.hot_acum[tm0]){
                            let fac = (this.hot_acum[tm0] > 0)? this.hot_acum[tm1] / this.hot_acum[tm0]: 1;
                            this.hot_fac[tm1] = fac;
                            if(this.hot_mm[ranum] == undefined){
                                this.hot_mm[ranum] = {'min': fac, 'max': fac, 'periodo': ri + 1, 'data': [], 'suma': 0};
                            }
                            this.hot_mm[ranum].min = Math.min(this.hot_mm[ranum].min, fac);
                            this.hot_mm[ranum].max = Math.max(this.hot_mm[ranum].max, fac);
                            this.hot_mm[ranum].data.push(fac);
                            this.hot_mm[ranum].suma += fac;
                        }else{
                            // console.log('El actual debería ser mayor que el anterior.');
                            // console.log();
                        }
                    }
                });
            });
            console.log('roneke');
            console.log(this.hot_mm);
            this.periodos.forEach((pre, pi) => {
                this.periodos.slice(pi).forEach((rad, ri) => {
                    let refmm = this.periodos[ri].num;
                    let namei = `${pre.num}_${rad.num}`;
                    if(ri == 0){
                        this.hot_col[namei] = 'd-nonex';
                    }else{
                        if(!this.isEmpty(this.hot_mm[refmm]) && !this.isEmpty(this.hot_fac[namei])){
                            let rango = this.hot_mm[refmm].max - this.hot_mm[refmm].min;
                            if(rango == 0){
                                this.hot_col[namei] = 'bg-0';
                            }else{
                                let num = (this.hot_fac[namei] - this.hot_mm[refmm].min) / rango;
                                this.hot_col[namei] = 'bg-' + Math.round(num * 20);
                            }
                        }
                    }
                });
            });
            this.hot_status = true;
        },
        setTriangle: function(elm){
            this.enable_controls = false;
            this.targetTriangle = elm;
            this.setDymclass(elm.code);
            if(['CALOR', 'DESARROLLO'].includes(elm.code)){
                this.resetHotData();
            }
            if(elm.ori != 'all' && this.status_src[elm.ori].load == false){
                this.loadBridge(elm.ori);
                // this.loadFuente(elm.ori);
            }
        },
        setDymclass: function(code){
            if(code == 'CALOR'){
                this.fun_dymclass = (r, c) => {
                    let cs = (c < r)? this.f_out + ' ': '';
                    return cs + this.getColorCell(r, c);
                }
            }else{
                this.fun_dymclass = (r, c) => {
                    if(r == c){
                        return this.f_cross;
                    }
                    return (c < r)? this.f_out + this.f_left: this.f_in;
                }
            }
        },
        getTriangleInfo: function(arg){
            if(this.targetTriangle == null){
                return '';
            }
            return this.targetTriangle[arg];
        },
        getFuenteInfo: function(ori, arg){
            if(this.isEmpty(ori) || this.isEmpty(arg)){
                return '';
            }
            return this.status_src[ori][arg];
        },
        isLoadTriangle: function(ori){
            if(['aut', 'fac', 'pag'].includes(ori)){
                return this.status_src[ori].status == this.state.LOADING;
            }
            return false;
        },
        makePyramid: function(y, m){
            this.periodos = [];     // {num: 202303, anio: 2023, mes: 03, tx: 'Marzo'}
            for(let i = 1; i < 37; i++){
                if(m == 0){
                    m = 12;
                    y--;
                }
                let per = parseInt(y + m.toString().padStart(2, '0'));
                this.periodos.unshift({
                    'num': per,
                    'anio': y,
                    'mes': m,
                    'tx': this.mss[m]
                });
                m--;
            }
            this.per_first = this.periodos[0].num;
            this.per_last = this.periodos.at(-1).num;
        },
        setFilter: function(arg){
            this.f_filtro = arg;
            if(arg == 'all'){
                this.fun_filter = (tipo) => true;
            }else{
                this.fun_filter = (tipo) => tipo == this.f_filtro;
            }
        },
        setValor: function(row, col, val){
            if(this.akey.includes(row) && this.akey.includes(col)){
                this.hash[row][col].valor = val;
                this.hash[row][col].stt = 'on';
            }else{
                // console.log('Not include!');
                // console.log(row, col);
            }
        },
        getValor: function(row, col, origen){
            let ref = row + '_' + col;
            if(this.hash[ref] == undefined || this.hash[ref].length == 0){
                return '';
            }
            let num = 0;
            if(origen == 'all'){
                num = this.hash[ref].reduce((ac, elm) => {
                    return this.fun_filter(elm.tipo)? ac + elm.valor: ac;
                }, 0);
            }else{
                num = this.hash[ref].reduce((ac, elm) => {
                    return (this.fun_filter(elm.tipo) && elm.origen == origen)? ac + elm.valor: ac;
                }, 0);
            }
            return this.clearNumber(num);
        },
        getValorAcum: function(row, col){
            let nrow = parseInt(row);
            let ncol = parseInt(col);
            let aux = {};
            let pers = this.periodos.filter(elm => elm.num >= nrow && elm.num <= ncol).map((elm, i) => {
                aux[`${nrow}_${elm.num}`] = {'r': nrow, 'c': elm.num, 'i': i + 1, 'aut': 0, 'fac': 0, 'pag': 0};
                return elm.num;
            });
            let rs = 0;
            if(this.f_filtro == 'all'){
                pers.forEach(elm => {
                    let ref = row + '_' + elm;
                    if(this.hash[ref] == undefined || this.hash[ref].length == 0){
                        // return '';
                    }else{
                        this.hash[ref].forEach(ele => {
                            aux[ref][ele.origen] += ele.valor;
                            rs += ele.valor;
                        });
                    }
                });
            }else{
                pers.forEach(elm => {
                    let ref = row + '_' + elm;
                    if(this.hash[ref] == undefined || this.hash[ref].length == 0){
                        // return '';
                    }else{
                        this.hash[ref].forEach(ele => {
                            if(this.f_filtro == ele.tipo){
                                aux[ref][ele.origen] += ele.valor;
                                rs += ele.valor;
                            }
                        });
                    }
                });
            }
            let data = Object.values(aux);
            return {'valor': rs, 'data': data};
        },
        getValorAcumHot: function(row, col){
            return this.hot_acum[`${row}_${col}`];
        },
        getValorAcumFac: function(row, col){
            return this.hot_fac[`${row}_${col}`];
        },
        makeParams: function(arg){
            if(this.status != this.state.LOADING){
                if(this.status_src[arg].load === false){
                    this.status_src[arg].status = this.state.LOADING;
                    this.status = this.state.LOADING;
                    let crx = this.targetPeriodoDB.num;
                    let yyyy = parseInt(String(crx).slice(0, 4));
                    let mm = parseInt(String(crx).slice(-2));
                    if(this.status_src.crx != crx){
                        ['aut', 'fac', 'pag'].forEach(elm => this.status_src[elm].load = false);
                        this.status_src.crx = crx;
                        this.targetTriangle = null;
                        this.makePyramid(yyyy, mm);
                    }
                    let desde = this.periodos[0].num;
                    let hasta = this.periodos[35].num;
                    let pam = {'fuente': arg, 'tema': this.fuentes[arg], 'desde': desde, 'hasta': hasta, 'crx': crx};
                    return pam;
                }
            }
        },
        loadBridge: function(arg, force=false){
            console.log('Click load bridge...');
            if(this.status != this.state.LOADING){
                if(force){
                   this.status_src[arg].load = false;
                }
                if(this.status_src[arg].load === false){
                    console.log('Run loadBridge...');
                    this.status_src[arg].status = this.state.LOADING;
                    this.status = this.state.LOADING;
                    let crx = this.targetPeriodoDB.num;
                    let yyyy = parseInt(String(crx).slice(0, 4));
                    let mm = parseInt(String(crx).slice(-2));
                    if(this.status_src.crx != crx){
                        ['aut', 'fac', 'pag'].forEach(elm => this.status_src[elm].load = false);
                        this.status_src.crx = crx;
                        this.targetTriangle = null;
                        this.makePyramid(yyyy, mm);
                    }
                    let desde = this.periodos[0].num;
                    let hasta = this.periodos[35].num;
                    let pam = {'fuente': arg, 'tema': this.fuentes[arg], 'desde': desde, 'hasta': hasta, 'crx': crx};
                    let origen = arg;
                    let tname = this.cliente + '_try_' + arg + '_' + crx;
                    console.log('Empezando a cargar...');
                    this.$refs.timer.loadData(tname, arg, this.pathfuente, pam, force);
                }
            }
        },
        loadFuente: function(arg){
            if(this.status != this.state.LOADING){
                if(this.status_src[arg].load === false){
                    this.status_src[arg].status = this.state.LOADING;
                    this.status = this.state.LOADING;
                    let crx = this.targetPeriodoDB.num;
                    let yyyy = parseInt(String(crx).slice(0, 4));
                    let mm = parseInt(String(crx).slice(-2));
                    if(this.status_src.crx != crx){
                        ['aut', 'fac', 'pag'].forEach(elm => this.status_src[elm].load = false);
                        this.status_src.crx = crx;
                        this.targetTriangle = null;
                        this.makePyramid(yyyy, mm);
                    }
                    let desde = this.periodos[0].num;
                    let hasta = this.periodos[35].num;
                    let pam = new FormData();
                    pam.append('fuente', arg);
                    pam.append('tema', this.fuentes[arg]);
                    pam.append('desde', desde);
                    pam.append('hasta', hasta);
                    pam.append('crx', crx);
                    let origen = arg;
                    console.log('Empezando a cargar...');
                    axios.post(this.pathfuente, pam).then(res => {
                        if(Array.isArray(res.data)){
                            res.data[0].datos.forEach(elm => {
                                this.pushValue(elm, origen);
                            });
                            if(this.targetTriangle == null){
                                this.setTriangle(this.status_src[origen].list[0]);
                            }
                            this.status_src[arg].load = true;
                            this.status_src[arg].status = this.state.LOADED;
                            this.status = this.state.LOADED;
                            if(this.status_src.aut.load && this.status_src.fac.load && this.status_src.pag.load){
                                this.status_src.all.load = true;
                            }
                        }else{
                            this.status_src[arg].status = this.state.FAILED;
                            this.status = this.state.FAILED;
                        }
                    }).catch(err => {
                        console.log(err);
                        this.status = this.state.FAILED;
                    });
                }
            }
        },
        pushValue: function(doc, origen){
            if(/^\d{6}$/.test(doc._id.f_pre) == false || /^\d{6}$/.test(doc._id.f_rad) == false){
                this.warnings[origen].push({
                    'pre': doc._id.f_pre,
                    'rad': doc._id.f_rad
                });
            }else{
                let ref = doc._id.f_pre + '_' + doc._id.f_rad;
                if(this.hash[ref] == undefined){
                    this.hash[ref] = [];
                }
                this.hash[ref].push({'valor': doc.total_pac, 'tipo': 'pac', 'origen': origen});
                this.hash[ref].push({'valor': doc.total_pbs, 'tipo': 'pbs', 'origen': origen});
                this.hash[ref].push({'valor': doc.total_pm, 'tipo': 'pm', 'origen': origen});
            }
        },
        fillPeriodos: function(arr, src){
            // periodos_db: [],    
            // {num: 202303, anio: 2023, mes: 03, tx: 'Marzo', match: {aut: false, fac: false, pag: false}}
            arr.forEach(elm => {
                let aux = this.periodos_db.find(per => per.num == elm);
                if(this.isEmpty(aux)){
                    this.periodos_db.push({
                        'num': elm, 
                        'anio': String(elm).slice(0, 4), 
                        'mes': String(elm).slice(-2), 
                        'tx': this.mss[parseInt(String(elm).slice(-2))], 
                        'match': {'aut': src == 'aut', 'fac': src == 'fac', 'pag': src == 'pag'}
                    });
                }else{
                    aux.match[src] = true;
                }

            });
        },
        loadPeriodos: function(){
            let aut = [202206, 202212, 202306];
            let fac = [202212, 202305, 202306];
            let pag = [202212, 202306];
            if([7, '7'].includes(this.cliente)){
                aut = [202206, 202212, 202301, 202302, 202303, 202304, 202306];
                fac = [202206, 202212, 202301, 202302, 202303, 202304, 202306];
                pag = [202301, 202302, 202303, 202306];
            }
            if([3, '3'].includes(this.cliente)){
                aut = [202306];
                fac = [202306];
                pag = [202306];
            }
            this.periodos_db = [];
            this.fillPeriodos(aut, 'aut');
            this.fillPeriodos(fac, 'fac');
            this.fillPeriodos(pag, 'pag');
            let tm = {};
            this.periodos_db.forEach(elm => {
                if(tm[elm.anio] == undefined){
                    tm[elm.anio] = {'anio': elm.anio, 'meses': []};
                }
                tm[elm.anio]['meses'].push({'num': elm.num, 'tx': elm.tx, 'match': elm.match});
            });
            this.periodos_select = Object.values(tm);
            // if(this.status_per != this.state.LOADING){
            //     console.log('cargando periodos');
            //     let pam = new FormData();
            //     pam.append('tema', '6_retec_facturas_view');//'this.fuente);
            //     pam.append('campo', 'crx');
            //     this.status_per = this.state.LOADING;
            //     axios.post(this.pathperiodos, pam).then(res => {
            //         this.periodos_db = res.data;
            //         this.status_per = this.state.LOADED;
            //     }).catch(err => {
            //         this.status_per = this.state.FAILED;
            //         console.log(err);
            //     });
            // }
        },
        openCell: function(pre, rad, r, c, ori){
            this.type_cell = 'normal';
            this.targetCellRef = {'pre': pre, 'rad': rad, 'row': r, 'col': c, 'origen': ori};
            let ref = pre + '_' + rad;
            if(Array.isArray(this.hash[ref])){
                this.targetCell = this.hash[ref];
            }else{
                this.targetCell = [];
            }
            $('#lc_modal').modal('show');
        },
        openCellAcum: function(pre, rad, r, c){
            this.type_cell = 'acum';
            this.targetCellRef = {'pre': pre, 'rad': rad, 'row': r, 'col': c, 'origen': 'all'};
            console.log('Ñoki');
            let rs = this.getValorAcum(pre, rad);
            this.value_cell = rs.valor;
            this.targetCell = rs.data;
            $('#lc_modal').modal('show');
        },
        preReset: function(){
            swal({
                title: "¿Está seguro?",
                text: "Si cambia el corte de periodo de la base de datos, se reiniciarán las fuentes que hayan sido cargadas previamente.",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#f0c541",
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar",
                closeOnConfirm: true
            }, () => this.resetear());
        },
        resetear: function(){
            ['aut', 'fac', 'pag', 'all'].forEach(elm => {
                this.status_src[elm].load = false;
                this.status_src[elm].status = 'ini';
            });
            this.enable_controls = false;
            this.status_src.crx = null;
            this.status = this.state.INI;
            this.hash = {};
            this.sumcol = {};
            this.targetPeriodoDB = null;
            this.targetTriangle = null;
            this.warnings = {'aut': [], 'fac': [], 'pag': []};
        },
        listen: function(){
            this.$eventBus.$on('end-load', arg => {
                let origen = arg.origen;
                let contenido = arg.contenido;
                console.log('Resultado en end-load');
                console.log(arg);
                if(Array.isArray(contenido)){
                    contenido[0].datos.forEach(elm => {
                        this.pushValue(elm, origen);
                    });
                    if(this.targetTriangle == null){
                        this.setTriangle(this.status_src[origen].list[0]);
                    }
                    this.status_src[origen].load = true;
                    this.status_src[origen].status = this.state.LOADED;
                    this.status = this.state.LOADED;
                    if(this.status_src.aut.load && this.status_src.fac.load && this.status_src.pag.load){
                        this.status_src.all.load = true;
                    }
                }else{
                    this.status_src[origen].status = this.state.FAILED;
                    this.status = this.state.FAILED;
                }
            });
        },
        calc_01: function(){    //

        }
    },
    mounted() {
        this.switchControl();
        this.listen();
        this.setDymclass('self');
        let ki = new Date();
        this.anio = ki.getFullYear();
        this.mes = ki.getMonth() + 1;
        this.f_periodo = this.anio + this.mes.toString().padStart(2, '0');
        this.loadPeriodos();
    }
}
</script>
<style scoped>
.colmin {width: 1%; white-space:nowrap; text-align:center}
.opaco {opacity: 0.5 !important; user-select: none}
.control-label {text-transform: none !important}
.loading {opacity:0.45 !important; pointer-events: none !important; user-select: none !important}
.loading-solid {pointer-events: none !important; user-select: none !important}
.loading-wait {cursor:wait !important}
.loading-wait * {pointer-events: none !important; user-select: none !important}
.literal {text-transform: none !important}
.list-group-item {border-left: none !important; border-top: none !important; border-right: none !important; margin-top:1px}

.table.table-min {width: min-content !important}
.table.table-min th, .table.table-min td {padding-left: 24px !important; padding-right: 24px !important}
.table.table-bordered {border:none}
.table.table-bordered th, .table.table-bordered td {padding-left:6px; padding-right:6px; text-align:center; border:1px solid #999 !important; color:#000 !important; font-family: Arial; cursor:default !important}
.table.table-pyramid th, .table.table-pyramid td {padding:.5rem .4rem; color:#000; font-family: Arial}
.table-bordered.table-pyramid th, .table-bordered.table-pyramid td {border:1px solid #000 !important; color:#000}
.table-bordered.table-pyramid td {text-align: right}
.table-bordered.table-pyramid thead tr.tr-title th {font-size:1.2rem; font-weight: bold; text-align: center !important}
.table-bordered.table-pyramid thead tr.tr-sub th {font-size:.7rem; font-weight: bold; text-align: center !important}
tr.triangle-left td.bg-danger {display: none !important}

/* .table td:hover {background:#FFE699}
.table td:hover ~ td {background:#EBFFFC} */
.bg-gray {background:#E1E1E1}

.df-grey {background:#EAEAEA !important}
.bg-cruce {background: #FFE699}
.bg-in {background:#E2EFDA}
.df-out {display: none}

.table.table-bordered  th.cel-hide {border:none !important;}
.form-control option[disabled] {color:#F00 !important}
.text-micro {font-family: Arial !important; font-size: .8rem; letter-spacing: 2px !important}
.btn.btn-block {border-radius:none !important}
.df-btn {cursor: pointer; background:#DEDEDE; padding: .5rem 0; text-align: center}
tbody.df-guia td {position: relative}
.info-left, .info-top {position: absolute; display: none; background: #000; color:#FFF; text-align: center; padding:4px .75rem}
.info-left {right:100%; top:0; bottom:0}
.info-top {bottom:100%; left:0; right:0}

.list-group-item.focus-item {background:#FFF2CC !important; color:#000}

tbody.df-guia td:hover {background:#92D050}
tbody.df-guia td:hover > .info-left {display: block; pointer-events:none !important}
tbody.df-guia td:hover > .info-top {display: block; pointer-events:none !important}

.table.table-bordered td.bg-20 {background-color: #F8696B !important; border-color:#FFF !important}
.table.table-bordered td.bg-19 {background-color: #F8766D !important; border-color:#FFF !important}
.table.table-bordered td.bg-18 {background-color: #F98370 !important; border-color:#FFF !important}
.table.table-bordered td.bg-17 {background-color: #FA9072 !important; border-color:#FFF !important}
.table.table-bordered td.bg-16 {background-color: #FA9D75 !important; border-color:#FFF !important}
.table.table-bordered td.bg-15 {background-color: #FBAA77 !important; border-color:#FFF !important}
.table.table-bordered td.bg-14 {background-color: #FCB77A !important; border-color:#FFF !important}
.table.table-bordered td.bg-13 {background-color: #FCC47C !important; border-color:#FFF !important}
.table.table-bordered td.bg-12 {background-color: #FDD17F !important; border-color:#FFF !important}
.table.table-bordered td.bg-11 {background-color: #FEDE81 !important; border-color:#FFF !important}
.table.table-bordered td.bg-10 {background-color: #FFEB84 !important; border-color:#FFF !important}
.table.table-bordered td.bg-9 {background-color: #F0E784 !important; border-color:#FFF !important}
.table.table-bordered td.bg-8 {background-color: #E0E383 !important; border-color:#FFF !important}
.table.table-bordered td.bg-7 {background-color: #D1DE82 !important; border-color:#FFF !important}
.table.table-bordered td.bg-6 {background-color: #C1D981 !important; border-color:#FFF !important}
.table.table-bordered td.bg-5 {background-color: #B1D580 !important; border-color:#FFF !important}
.table.table-bordered td.bg-4 {background-color: #A2D07F !important; border-color:#FFF !important}
.table.table-bordered td.bg-3 {background-color: #92CC7E !important; border-color:#FFF !important}
.table.table-bordered td.bg-2 {background-color: #83C77D !important; border-color:#FFF !important}
.table.table-bordered td.bg-1 {background-color: #73C37C !important; border-color:#FFF !important}
.table.table-bordered td.bg-0 {background-color: #63BE7B !important; border-color:#FFF !important}
</style>
