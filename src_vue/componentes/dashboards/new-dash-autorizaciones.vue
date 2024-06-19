<template>
    <div :class="'component-' + status">
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">{{ clientetx }} - <strong>AUTORIZACIONES</strong><br></h5>
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
                <div :class="section == 'basic'? 'btn-group dk-disabled': 'btn-group'">
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
        <div :class="section == 'controls'? 'd-none': 'row'">
            <div class="col-sm-3">
                <local-counter ref="cnt_1" class="border" texto="SERVICIOS" valor="0" duracion="1" miles></local-counter>
            </div>
            <div class="col-sm-3">
                <local-counter ref="cnt_vbs" class="border" texto="TOTAL RESERVA PBS" valor="0" duracion="1" miles pretag="$ "></local-counter>
            </div>
            <div class="col-sm-3">
                <local-counter ref="cnt_vac" class="border" texto="TOTAL RESERVA PAC" valor="0" duracion="1" miles pretag="$ "></local-counter>
            </div>
            <div class="col-sm-3">
                <local-counter ref="cnt_vpm" class="border" texto="TOTAL RESERVA PM" valor="0" duracion="1" miles pretag="$ "></local-counter>
            </div>
        </div>
        <div :class="section == 'basic'? '': 'd-none'">
            <div class="row">
                <div class="col-sm-5">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">% ESTIMACIÓN TARIFA<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-pie 
                                    ref="gp_esti" 
                                    altura="290" 
                                    etiquetas 
                                    radio="60" 
                                    campo_categoria="_id" 
                                    campo_valor="total" 
                                    leyenda="bottom" 
                                    paleta="#0081a7,#00afb9,#fdfcdc,#fed9b7,#f07167"></am-pie>
                            </div>
                        </div>
                    </div>
                </div><!-- End col-sm-5 -->
                <div class="col-sm-7">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">% ESTADO AUTORIZACIÓN<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-pie 
                                    ref="gp_stt" 
                                    altura="290" 
                                    etiquetas 
                                    radio="60" 
                                    campo_categoria="_id" 
                                    campo_valor="total" 
                                    empty_category="(Vacío)"
                                    leyenda="bottom" 
                                    paleta="#0081a7,#00afb9,#fdfcdc,#fed9b7,#f07167"></am-pie>
                            </div>
                        </div>
                    </div>
                </div><!-- End col-sm-7 -->
            </div>
            <div class="row">
                <div class="col-sm-5">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">% DE AUTORIZACIONES SEGÚN PLAN DE SALUD<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-pie 
                                    ref="one" 
                                    altura="290" 
                                    etiquetas 
                                    radio="60" 
                                    campo_categoria="_id" 
                                    campo_valor="count" 
                                    leyenda="bottom" 
                                    paleta="#0081a7,#00afb9,#fdfcdc,#fed9b7,#f07167"></am-pie>
                            </div>
                        </div>
                    </div>
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">PRESUPUESTOS MÁXIMOS<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_pmx.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_pmx" 
                                    altura="140" 
                                    campo_categoria="_id" 
                                    campo_valor="total:Recuento" 
                                    empty_category="(Vacío)"
                                    redondeado
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    paleta="#1d4e89,#00b2ca,#7dcfb6,#fbd1a2,#f79256" 
                                    multicolor 
                                    grilla="0" 
                                    cursor 
                                    lanzarevento="select-pmx">
                                </am-bar>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-7">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPOS DE DOCUMENTOS<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_doc.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar 
                                    ref="gp_doc" 
                                    altura="213" 
                                    campo_categoria="_id" 
                                    campo_valor="count:Recuento" 
                                    redondeado
                                    tooltip 
                                    etiquetas 
                                    sin_valores 
                                    paleta="#1d4e89,#00b2ca,#7dcfb6,#fbd1a2,#f79256" 
                                    multicolor 
                                    grilla="0" 
                                    cursor 
                                    lanzarevento="select-tipodoc">
                                </am-bar>
                            </div>
                        </div>
                    </div>
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ÁMBITO DE AUTORIZACIONES<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.two.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="two" altura="213" campo_categoria="_id" campo_valor="count:Recuento" redondeado tooltip etiquetas sin_valores paleta="#118ab2,#06d6a0,#ffd166,#ef476f,#073b4c" multicolor grilla="0" cursor lanzarevento="select-ambito"></am-bar>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :class="['data-1', 'data-2'].includes(section)? 'd-none': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="btn-group">
                            <button :class="taritem == 'suma'? 'btn btn-success': 'btn btn-default'" @click="setTaritem('suma')"><i class="fa fa-dollar me-2"></i> Ranking financiero</button>
                            <button :class="taritem == 'total'? 'btn btn-success': 'btn btn-default'" @click="setTaritem('total')"><i class="fa fa-list-ol me-2"></i> Ranking registros</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'data-1'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE AUTORIZACIONES PBS - RÉGIMEN SUBSIDIADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.gp_0_S.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_0_S" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" custom="Valor: {valueX}, Registros: {total}" custom_label="{category}: {valueX} ({total} registros)" ref="gp_0_S" pretag="$ " grilla="0" multicolor campo_categoria="_id" campo_valor="valor" etiquetas tooltip sin_valores altura_minima="100" unidad="30" empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE AUTORIZACIONES PRESUPUESTOS MÁXIMOS - RÉGIMEN SUBSIDIADO <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1_S.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_1_S" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="gp_1_S" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{category}: {valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'data-2'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE AUTORIZACIONES PBS - MOVILIDAD CONTRIBUTIVO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.gp_0_V.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_0_V" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="gp_0_V" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{category}: {valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE AUTORIZACIONES PRESUPUESTOS MÁXIMOS - MOVILIDAD CONTRIBUTIVO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1_V.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a>
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <table-data :class="altCss(display == 'table')" ref="tb_1_V" cols="_id:PRESTADOR,valor:TOTAL:$ " compact counter lastright sumar="valor"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="gp_1_V" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="valor" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            custom="Valor: {valueX}, Registros: {total}" 
                            custom_label="{category}: {valueX} ({total} registros)" 
                            empty_data="No hay datos para graficar."></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'controls'? '': 'd-none'">
            <h5 class="txt-dark">Controles PBS</h5>
            <div class="row mb-4">
                <div class="col-sm-4">
                    <local-counter ref="a_1" pretag="$ " class="border" texto="RESERVA CALCULADA" valor="0" duracion="1" miles></local-counter>
                </div>
                <div class="col-sm-4">
                    <local-counter ref="a_2" pretag="$ " class="border" texto="RESERVA REPORTADA" valor="0" duracion="1" miles></local-counter>
                </div>
                <div class="col-sm-4">
                    <local-counter ref="a_3" pretag="$ " class="border" texto="DIFERENCIA" valor="0" duracion="1" miles warning></local-counter>
                </div>
            </div>
            <h5 class="txt-dark">Controles Presupuestos Máximos</h5>
            <div class="row">
                <div class="col-sm-4">
                    <local-counter ref="b_1" pretag="$ " class="border" texto="RESERVA CALCULADA" valor="0" duracion="1" miles></local-counter>
                </div>
                <div class="col-sm-4">
                    <local-counter ref="b_2" pretag="$ " class="border" texto="RESERVA REPORTADA" valor="0" duracion="1" miles></local-counter>
                </div>
                <div class="col-sm-4">
                    <local-counter ref="b_3" pretag="$ " class="border" texto="DIFERENCIA" valor="0" duracion="1" miles warning></local-counter>
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
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">PROPORCIÓN DE TARIFAS <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <table-data :class="altCss(display == 'table')" ref="table_suma" cols="_id:TARIFA,valor:TOTAL" compact lastright sumar="valor"></table-data>
                                <am-pie :class="altCss(display == 'chart')" ref="sumas" campo_categoria="_id" altura="480" tooltip etiquetas></am-pie>
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
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <table-data :class="altCss(display == 'table')" ref="table_3" cols="_id:ESTADO,suma:VALOR,total:REGISTROS" compact lastright sumar="total"></table-data>
                                <am-bar :class="altCss(display == 'chart')" ref="gp_3" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor tooltip cursor lanzarevento="select-estado"></am-bar>
                            </div>
                        </div>
                    </div>
                    <!-- END MICRO TABLE -->
                    <div class="row">
                        <div class="col-sm-6">
                            <div class="panel panel-default card-view border">
                                <div class="panel-heading border-bottomx">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">Plan salud <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                            <span class="txt-dark">{{ human_period }}</span>
                                        </div>
                                        <div>
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_1" cols="_id:PLAN,suma:VALOR,total:REGISTROS" compact lastright sumar="total"></table-data>
                                        <am-bar :class="altCss(display == 'chart')" ref="gp_1" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor tooltip cursor lanzarevento="select-plan"></am-bar>
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
                                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                        </div>
                                    </div>
                                </div>
                                <div class="panel-wrapper collapse in">
                                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                        <table-data :class="altCss(display == 'table')" ref="table_2" cols="_id:TIPO DOC,suma:VALOR,total:REGISTROS" compact lastright sumar="total"></table-data>
                                        <am-bar :class="altCss(display == 'chart')" ref="gp_2" campo_categoria="_id" campo_valor="total" etiquetas sin_valores grilla="0" altura="180" multicolor tooltip cursor lanzarevento="select-tipo"></am-bar>
                                    </div>
                                </div>
                            </div>
                            <!-- END MICRO TABLE -->
                        </div>
                    </div>
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
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ESTRUCTURA DE LA BASE DE DATOS DE AUTORIZACIONES</h6>
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
                                            <!-- <th>Nombre corto</th> -->
                                            <th class="colmin text-center">Apariciones del campo</th>
                                            <th class="colmin text-center">Estado</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(elm, i) in campos" :key="i">
                                            <td class="text-center">{{ i + 1 }}</td>
                                            <td>{{ pairs[elm] }}</td>
                                            <!-- <td>{{ elm }}</td> -->
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
                subtitulo="RESERVAS TÉCNICAS - AUTORIZACIONES" 
                separador="|" 
                sindiccionario
                head="file_parse"
                fields="stt:Estado|tpp:tipoIdPrestador|idp:idPrestador|nmp:nombrePrestador|pla:planSalud|idc:idContrato|tus:tipoIdUsuario|ius:idUsuario|iav:idAvisado|fav:FAvis|amb:Ambito|ids:idServicio|ser:DesServicio|dia:DiagPpal|can:Cant|est:Est|vun:VrUnidad|vbs:VlrReservaPBS|vac:VlrReservaPAC|vpm:VlrReservaPM|pmx:pres_Max|pac:PAct|ume:UMed|ffa:FFarma|cov:Covid"
                rules=""
                codec_mode="show"
                error="ignore"
                error_mode="show"
                info
                extra
                realtime
                withperiodo
                :clientetx="clientetx">
            </import-basic>
            <div class="my-4"></div>
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <import-list :coleccion="fuente" titulo="BASE DE DATOS DE AUTORIZACIONES"></import-list>
                    </div>
                </div>
            </div>
        </div>
        <local-modal 
            :coleccion="fuente" 
            cantidad="50"
            campos="stt:Estado,tpp:tipoIdPrestador,idp:idPrestador,nmp:nombrePrestador,pla:planSalud,idc:idContrato,tus:tipoIdUsuario,ius:idUsuario,iav:idAvisado,fav:FAvis,amb:Ambito,ids:idServicio,ser:DesServicio,dia:DiagPpal,can:Cant,est:Est,vun:VrUnidad,vbs:VlrReservaPBS,vac:VlrReservaPAC,vpm:VlrReservaPM,pmx:pres_Max,pac:Pact,ume:Umed,ffa:Ffarma,cov:Covid,crx:Periodo">
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
            fuente: (this.cliente == '0')? 'retec_autorizacion_0': this.cliente + '_retec_autorizacion',
            // fuente: '7_retec_autorizacion',
            krache: 'dash_auto_' + this.cliente,
            krache_ctr: 'dash_auto_ctr_' + this.cliente,
            krache_time: 'time_autorizacion_' + this.cliente,
            section: 'basic',
            display: 'chart',       // table | chart
            taritem: 'suma',        // suma | total
            opt: [
                {'tx': 'General', 'code': 'basic'}, 
                {'tx': 'Ranking Servicios RS', 'code': 'data-1'}, 
                {'tx': 'Ranking Servicios RC', 'code': 'data-2'}, 
                {'tx': 'Reservas', 'code': 'controls'}, 
                {'tx': 'Estructura', 'code': 'schema'}, 
                {'tx': 'Importar', 'code': 'import'}
            ],
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            campos: ['stt', 'tpp', 'idp', 'nmp', 'pla', 'idc', 'tus', 'ius', 'iav', 'fav', 'amb', 'ids', 'ser', 'dia', 'can', 'est', 'vun', 'vbs', 'vac', 'vpm', 'pmx', 'pac', 'ume', 'ffa', 'cov'],
            pairs: {_id:'Total registros', stt:'Estado', tpp:'tipoIdPrestador', idp:'idPrestador', nmp:'nombrePrestador', pla:'planSalud', idc:'idContrato', tus:'tipoIdUsuario', ius:'idUsuario', iav:'idAvisado', fav:'FAvis', amb:'Ambito', ids:'idServicio', ser:'DesServicio', dia:'DiagPpal', can:'Cant', est:'Est', vun:'VrUnidad', vbs:'VlrReservaPBS', vac:'VlrReservaPAC', vpm:'VlrReservaPM', pmx:'pres_Max', pac:'Pact', ume:'Umed', ffa:'Ffarma', cov:'Covid'},
            rawData: null,
            rawCtr: null,
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
        clearNumber: function(num){
            return (num % 1 == 0)? num: parseFloat(num).toFixed(2);
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
        setTaritem: function(arg){
            if(['suma', 'total'].includes(arg)){
                this.taritem = arg;
                this.writeItems();
            }
        },
        loadData: function(arg){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('tema', this.fuente);
                pam.append('periodo', arg);
                this.status = this.state.LOADING;
                axios.post(this.pathdata + '/data', pam).then(res => {
                    this.rawData = (res.data.length > 0)?  res.data[0]: {'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'facet_pla': [], 'facet_amb': [], 'facet_total': [], 'facet_vbs': [], 'facet_vac': [], 'facet_vpm': [], 'facet_pmx': [], 'facet_doc': [], 'gp_esti': [], 'gp_stt': []};
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
        loadControls: function(arg){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('tema', this.fuente);
                pam.append('periodo', arg);
                this.status = this.state.LOADING;
                axios.post(this.pathdata + '/controls', pam).then(res => {
                    this.rawCtr = res.data;
                    registerJSON(this.krache_ctr, this.rawCtr, 'per_' + arg);
                    registerJSON(this.krache_ctr, arg, 'lastper');
                    this.rawCtr.forEach(elm => {
                        if(elm._id == '0'){
                            this.$refs.a_1.setValor(this.clearNumber(elm.sum_fac));
                            this.$refs.a_2.setValor(this.clearNumber(elm.sum_vbs));
                            this.$refs.a_3.setValor(this.clearNumber(elm.sum_fac - elm.sum_vbs));
                        }else if(elm._id == '1'){
                            this.$refs.b_1.setValor(this.clearNumber(elm.sum_fac));
                            this.$refs.b_2.setValor(this.clearNumber(elm.sum_vpm));
                            this.$refs.b_3.setValor(this.clearNumber(elm.sum_fac - elm.sum_vpm));
                        }
                    })
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
            if(this.rawData != null){
                this.rawData['facet_total'].length > 0? this.$refs.cnt_1.setValor(this.rawData['facet_total'][0].n): this.$refs.cnt_1.setValor('');
                this.rawData['facet_vbs'].length > 0? this.$refs.cnt_vbs.setValor(this.rawData['facet_vbs'][0].n): this.$refs.cnt_vbs.setValor('');
                this.rawData['facet_vac'].length > 0? this.$refs.cnt_vac.setValor(this.rawData['facet_vac'][0].n): this.$refs.cnt_vac.setValor('');
                this.rawData['facet_vpm'].length > 0? this.$refs.cnt_vpm.setValor(this.rawData['facet_vpm'][0].n): this.$refs.cnt_vpm.setValor('');
                this.$refs.gp_doc.setDatos(this.rawData['facet_doc']);
                if(Array.isArray(this.rawData['pmx'])){
                    let aux = {};
                    this.rawData['pmx'].forEach(elm => {
                        let kd = String(elm._id);
                        if(aux[kd] == undefined){
                            aux[kd] = {'_id': kd, 'total': 0};
                        }
                        aux[kd].total += elm.total;
                    });
                    this.$refs.gp_pmx.setDatos(Object.values(aux));
                }
                this.$refs.gp_esti.setDatos(this.rawData['gp_esti']);
                this.$refs.gp_stt.setDatos(this.rawData['gp_stt']);
                this.$refs.one.setDatos(this.rawData['facet_pla']);
                this.$refs.two.setDatos(this.rawData['facet_amb']);
                this.writeItems();
                // this.$refs.tb_0_S.setDatos(this.rawData['rs_1']);
                // this.$refs.gp_0_S.setDatos(this.rawData['rs_1'].slice(0, 30).sort((a, b) => a.valor - b.valor));
                // this.$refs.tb_0_V.setDatos(this.rawData['rs_2']);
                // this.$refs.gp_0_V.setDatos(this.rawData['rs_2'].slice(0, 30).sort((a, b) => a.valor - b.valor));
                // this.$refs.tb_1_S.setDatos(this.rawData['rs_3']);
                // this.$refs.gp_1_S.setDatos(this.rawData['rs_3'].slice(0, 30).sort((a, b) => a.valor - b.valor));
                // this.$refs.tb_1_V.setDatos(this.rawData['rs_4']);
                // this.$refs.gp_1_V.setDatos(this.rawData['rs_4'].slice(0, 30).sort((a, b) => a.valor - b.valor));
            }
            // facet_vbs  facet_vac   facet_vpm
        },
        writeItems: function(){
            if(this.rawData != null){
                if(this.taritem == 'suma'){
                    this.$refs.tb_0_S.setDatos(this.rawData['rs_1'], '$ ');
                    this.$refs.gp_0_S.setDatos(this.rawData['rs_1'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ ');
                    this.$refs.tb_0_V.setDatos(this.rawData['rs_2'], '$ ');
                    this.$refs.gp_0_V.setDatos(this.rawData['rs_2'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ ');
                    this.$refs.tb_1_S.setDatos(this.rawData['rs_3'], '$ ');
                    this.$refs.gp_1_S.setDatos(this.rawData['rs_3'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ ');
                    this.$refs.tb_1_V.setDatos(this.rawData['rs_4'], '$ ');
                    this.$refs.gp_1_V.setDatos(this.rawData['rs_4'].slice(0, 30).sort((a, b) => a.valor - b.valor), '$ ');
                }else{
                    this.$refs.tb_0_S.setDatos(this.rawData['rs_1'].map(elm => this.makeItem(elm)), '');
                    this.$refs.gp_0_S.setDatos(this.rawData['rs_1'].map(elm => this.makeItem(elm)).sort((a, b) => b.valor - a.valor).slice(0, 30).sort((a, b) => a.valor - b.valor), '');
                    this.$refs.tb_0_V.setDatos(this.rawData['rs_2'].map(elm => this.makeItem(elm)), '');
                    this.$refs.gp_0_V.setDatos(this.rawData['rs_2'].map(elm => this.makeItem(elm)).sort((a, b) => b.valor - a.valor).slice(0, 30).sort((a, b) => a.valor - b.valor), '');
                    this.$refs.tb_1_S.setDatos(this.rawData['rs_3'].map(elm => this.makeItem(elm)), '');
                    this.$refs.gp_1_S.setDatos(this.rawData['rs_3'].map(elm => this.makeItem(elm)).sort((a, b) => b.valor - a.valor).slice(0, 30).sort((a, b) => a.valor - b.valor), '');
                    this.$refs.tb_1_V.setDatos(this.rawData['rs_4'].map(elm => this.makeItem(elm)), '');
                    this.$refs.gp_1_V.setDatos(this.rawData['rs_4'].map(elm => this.makeItem(elm)).sort((a, b) => b.valor - a.valor).slice(0, 30).sort((a, b) => a.valor - b.valor), '');
                }
            }
        },
        makeItem: function(elm){
            return {'_id': elm._id, 'valor': elm.total};
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
                'schema_auto' + this.periodo,
                res => {
                    this.rawSchema = res[0];
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
            }else if('controls' == this.section){
                this.asyncRequest(
                    'raw_aut_ctr' + this.periodo,
                    res => {
                        this.rawCtr = (res.length > 0)? res: [];
                        this.rawCtr.forEach(elm => {
                            if(elm._id == '0'){
                                this.$refs.a_1.setValor(this.clearNumber(elm.sum_fac));
                                this.$refs.a_2.setValor(this.clearNumber(elm.sum_vbs));
                                this.$refs.a_3.setValor(this.clearNumber(elm.sum_fac - elm.sum_vbs));
                            }else if(elm._id == '1'){
                                this.$refs.b_1.setValor(this.clearNumber(elm.sum_fac));
                                this.$refs.b_2.setValor(this.clearNumber(elm.sum_vpm));
                                this.$refs.b_3.setValor(this.clearNumber(elm.sum_fac - elm.sum_vpm));
                            }
                        });
                    },
                    this.pathdata + '/controls',
                    {'tema': this.fuente, 'periodo': this.periodo},
                    true,   // first param
                    '',     // kcode param
                    force   // force param
                );
            }else{
                this.asyncRequest(
                    'raw_aut_dat' + this.periodo,
                    res => {
                        console.log('kokin');
                        console.log(res);
                        this.rawData = (res.length > 0)?  res[0]: {'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'facet_pla': [], 'facet_amb': [], 'facet_total': [], 'facet_vbs': [], 'facet_vac': [], 'facet_vpm': [], 'facet_pmx': [], 'facet_doc': [], 'pmx': []};
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
            this.$eventBus.$on('select-tipodoc', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'TIPO DE DOCUMENTO', 'periodo': this.periodo, 'filtros': 'tus:' + arg._id, 'foco': 'tus'});
            });
            this.$eventBus.$on('select-ambito', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'ÁMBITO', 'periodo': this.periodo, 'filtros': 'amb:' + arg._id, 'foco': 'amb'});
            });
            this.$eventBus.$on('select-tipo', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'TIPO DE PRESTADOR', 'periodo': this.periodo, 'filtros': 'tpp:' + arg._id, 'foco': 'tpp'});
            });
            this.$eventBus.$on('select-pmx', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'PRESUPUESTOS MÁXIMOS', 'periodo': this.periodo, 'filtros': 'pmx:' + arg._id, 'foco': 'pmx'});
            });
            this.$eventBus.$on('time-select', obj => {
                this.periodo = obj.periodo;
                this.manager();
            });
            this.$eventBus.$on('time-refresh', bool => {
                unregisterJSON(this.krache);
                unregisterJSON(this.krache_ctr);
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
.dk-disabled {opacity: .5 !important; user-select: none !important; pointer-events: none !important}
.component-loading .card-view > div {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .panel-body.vega {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .df-options > a {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
</style>