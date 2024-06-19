<template>
    <div :class="'component-' + status">
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">{{ clientetx }} - <strong>FACTURAS</strong><br></h5>
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
        <div :class="section == 'basic'? '': 'd-none'">
            <div class="row">
                <div class="col-sm-3">
                    <local-counter ref="cnt_all" class="border" texto="REGISTROS" valor="0" loading duracion="1" miles></local-counter>
                    <local-counter ref="cnt_vbs" class="border" texto="Total VLRRESERVAPBS" valor="0" loading duracion="1" miles pretag="$ "></local-counter>
                    <local-counter ref="cnt_vac" class="border" texto="Total VLRRESERVAPAC" valor="0" loading duracion="1" miles pretag="$ "></local-counter>
                    <local-counter ref="cnt_vpm" class="border" texto="Total VLRRESERVAPM" valor="0" loading duracion="1" miles pretag="$ "></local-counter>
                    <local-counter ref="cnt_vdo" class="border" texto="Total VLRFACTURADO" valor="0" loading duracion="1" miles pretag="$ "></local-counter>
                    <local-counter ref="cnt_vgl" class="border" texto="Total VLRGLOSADO" valor="0" loading duracion="1" miles pretag="$ "></local-counter>
                    <local-counter ref="cnt_gde" class="border" texto="Total GLOSADEFINITIVA" valor="0" loading duracion="1" miles pretag="$ "></local-counter>
                </div>
                <div class="col-sm-3">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPOS DE DOCUMENTOS<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_0.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-ver ref="gp_0" grilla="0" multicolor campo_categoria="_id" campo_valor="total" tooltip cursor etiquetas sin_valores altura_minima="100" unidad="30" lanzarevento="select-tus" empty_category="(Vacío)"></am-ver>
                            </div>
                        </div>
                    </div>
                    <!-- NUEVO GRÁFICO MEC. PAGO -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">MECANISMO PAGO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-ver ref="gp_ext_mec" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores paleta="#EA595A,#EFC41E,#48AD68,#2B8CB9,#905A9F" multicolor grilla="0" cursor lanzarevento="select-pla" empty_category="(Vacío)"></am-ver>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-3">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPO DE CONTRATO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_2.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_2" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores multicolor grilla="0" cursor lanzarevento="select-tra" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">PLAN SALUD<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_1" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores paleta="#EA595A,#EFC41E,#48AD68,#2B8CB9,#905A9F" multicolor grilla="0" cursor lanzarevento="select-pla" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>
                    <!-- NUEVO GRÁFICO TIPO DE OBLIGACIÓN -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPO OBLIGACIÓN<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_ext_01" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores paleta="#EA595A,#EFC41E,#48AD68,#2B8CB9,#905A9F" multicolor grilla="0" cursor lanzarevento="select-pla" empty_category="(Vacío)"></am-bar>
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
                                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_pmx" altura="180" redondeado grilla="0" multicolor campo_categoria="_id" campo_valor="total" tooltip cursor etiquetas sin_valores lanzarevento="select-pmx" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>                
                </div>
                <div class="col-sm-3">
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ÁMBITO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_3.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_3" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores paleta="#1d4e89,#00b2ca,#7dcfb6,#fbd1a2,#f79256" multicolor grilla="0" cursor lanzarevento="select-amb" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ESTADO GLOSA<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_4.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_4" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores multicolor grilla="0" cursor lanzarevento="select-tpo" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>
                    <!-- NUEVO GRÁFICO TIPO ID PRESTADOR -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPO ID PRESTADOR<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_ext_02" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores paleta="#EA595A,#EFC41E,#48AD68,#2B8CB9,#905A9F" multicolor grilla="0" cursor lanzarevento="select-pla" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>                    
                    <!-- NUEVO GRÁFICO COVID -->
                    <div class="panel panel-default card-view border">
                        <div class="panel-heading">
                            <div class="d-flex justify-content-between">
                                <div>
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">COVID<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                                    <span class="txt-dark">{{ human_period }}</span>
                                </div>
                                <div>
                                    <a href="javascript:void(0)" class="me-2" @click="$refs.gp_1.exportar()"><i class="zmdi zmdi-download"></i></a>
                                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                        </div>
                        <div class="panel-wrapper collapse in">
                            <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                                <am-bar ref="gp_ext_03" altura="180" campo_categoria="_id" campo_valor="total:Recuento" redondeado tooltip etiquetas sin_valores paleta="#EA595A,#EFC41E,#48AD68,#2B8CB9,#905A9F" multicolor grilla="0" cursor lanzarevento="select-pla" empty_category="(Vacío)"></am-bar>
                            </div>
                        </div>
                    </div>


                    <!-- <table-data :class="altCss(display == 'table')" ref="tb_0_S" cols="_id:PRESTADOR,valor:TOTAL" compact counter lastright sumar="valor"></table-data>
                    <am-ver :class="altCss(display == 'chart')" ref="gp_0_S" grilla="0" multicolor campo_categoria="_id" campo_valor="valor" etiquetas tooltip sin_valores altura_minima="100" unidad="30"></am-ver> -->
                </div>
            </div>
        </div>
        <div :class="section == 'data-indigena'? '': 'd-none'">
            <div class="row">
                <div class="col-sm-4">
                    <div class="border py-5 text-center" style="background:#FFF" v-if="rawIndi != null">
                        <h5 class="txt-dark mb-0">VALOR RESERVA AUTORIZACIONES<br></h5>
                        <div class="fs-3 txt-dark">{{ numformat(clearNumber(rawIndi.s_vdo)) }}</div>
                        <div style="letter-spacing:3px; color:#555; font:12px Arial">{{ human_period }}</div>
                        <div><i class="fa fa-dollar fs-1 text-success my-4"></i></div>
                    </div>
                </div>
                <div class="col-sm-4">
                    <div class="border py-5 text-center" style="background:#FFF" v-if="rawIndi != null">
                        <h5 class="txt-dark mb-0">VALOR RESERVA FACTURAS<br></h5>
                        <div class="fs-3 txt-dark">{{ numformat(clearNumber(rawIndi.s_vpbs)) }}</div>
                        <div style="letter-spacing:3px; color:#555; font:12px Arial">{{ human_period }}</div>
                        <div><i class="fa fa-dollar fs-1 text-success my-4"></i></div>
                    </div>
                </div>
                <div class="col-sm-4">
                    <div class="border py-5 text-center" style="background:#FFF" v-if="rawIndi != null">
                        <h5 class="txt-dark mb-0">TOTAL RESERVAS TÉCNICAS<br></h5>
                        <div class="fs-3 txt-dark">{{ numformat(clearNumber(rawIndi.s_vdo + rawIndi.s_vpbs)) }}</div>
                        <div style="letter-spacing:3px; color:#555; font:12px Arial">{{ human_period }}</div>
                        <div><i class="fa fa-dollar fs-1 text-success my-4"></i></div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border d-none">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">EPS INDÍGENA<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
                            <span class="txt-dark">{{ human_period }}</span>
                        </div>
                        <div>
                            <!-- <a href="javascript:void(0)" class="me-2" @click="$refs.gp_0_S.exportar()" v-if="display == 'chart'"><i class="zmdi zmdi-download"></i></a> -->
                            <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div :class="status == state.LOADING? 'panel-body opaco': 'panel-body'">
                        <am-bar muestra></am-bar>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'data-1'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE FACTURAS PBS - RÉGIMEN SUBSIDIADO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
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
                        <table-data :class="altCss(display == 'table')" ref="tb_0_S" cols="_id:PRESTADOR,suma:TOTAL:$ " compact counter lastright sumar="suma"></table-data>
                        <am-ver :class="altCss(display == 'chart')" 
                            ref="gp_0_S" 
                            pretag="$ " 
                            grilla="0" 
                            multicolor 
                            campo_categoria="_id" 
                            campo_valor="suma" 
                            etiquetas 
                            tooltip 
                            sin_valores 
                            altura_minima="100" 
                            unidad="30" 
                            empty_data="No hay datos para graficar." 
                            custom="{valueX} ({total} registros)"></am-ver>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE FACTURAS PRESUPUESTOS MÁXIMOS - RÉGIMEN SUBSIDIADO <i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
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
                        <table-data :class="altCss(display == 'table')" ref="tb_1_S" cols="_id:PRESTADOR,suma:TOTAL:$ " compact counter lastright sumar="suma"></table-data>
                        <am-ver :class="altCss(display == 'chart')" ref="gp_1_S" pretag="$ " grilla="0" multicolor campo_categoria="_id" campo_valor="suma" etiquetas tooltip sin_valores altura_minima="100" unidad="30" empty_data="No hay datos para graficar." custom="{valueX} ({total} registros)"></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'data-2'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE FACTURAS PBS - MOVILIDAD CONTRIBUTIVO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
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
                        <table-data :class="altCss(display == 'table')" ref="tb_0_V" cols="_id:PRESTADOR,suma:TOTAL:$ " compact counter lastright sumar="suma"></table-data>
                        <am-ver :class="altCss(display == 'chart')" ref="gp_0_V" pretag="$ " grilla="0" multicolor campo_categoria="_id" campo_valor="suma" etiquetas tooltip sin_valores altura_minima="100" unidad="30" empty_data="No hay datos para graficar." custom="{valueX} ({total} registros)"></am-ver>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <div>
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">RANKING DE FACTURAS PRESUPUESTOS MÁXIMOS - MOVILIDAD CONTRIBUTIVO<i class="fa fa-spin fa-spinner ms-2" v-if="status == state.LOADING"></i></h6>
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
                        <table-data :class="altCss(display == 'table')" ref="tb_1_V" cols="_id:PRESTADOR,suma:TOTAL:$ " compact counter lastright sumar="suma"></table-data>
                        <am-ver :class="altCss(display == 'chart')" ref="gp_1_V" pretag="$ " grilla="0" multicolor campo_categoria="_id" campo_valor="suma" etiquetas tooltip sin_valores altura_minima="100" unidad="30" empty_data="No hay datos para graficar." custom="{valueX} ({total} registros)"></am-ver>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'controls'? '': 'd-none'">
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr class="tr-center">
                                        <th>VLR FACTURADO</th>
                                        <th>PAGADO PBS</th>
                                        <th>PAGADO PM</th>
                                        <th>GLOSADO</th>
                                        <th>GLOSA DEF</th>
                                        <th>REGISTROS</th>
                                        <th>RESERVA PBS</th>
                                        <th>RESERVA PM</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td>{{ numformat(clearNumber(rawCtr[0].s_vdo)) }}</td>
                                        <td>{{ numformat(clearNumber(rawCtr[0].s_vpbs)) }}</td>
                                        <td>{{ numformat(clearNumber(rawCtr[0].s_vppm)) }}</td>
                                        <td>{{ numformat(clearNumber(rawCtr[0].s_vgl)) }}</td>
                                        <td>{{ numformat(clearNumber(rawCtr[0].s_gld)) }}</td>
                                        <td>{{ numformat(clearNumber(rawCtr[0].total)) }}</td>
                                        <td>{{ numformat(clearNumber(rawCtr[0].s_vrpbs)) }}</td>
                                        <td>{{ numformat(clearNumber(rawCtr[0].s_vrpm)) }}</td>
                                    </tr>
                                    <tr class="dk-row" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td colspan="5"></td>
                                        <td>CONTROLES</td>
                                        <td>
                                            {{ numformat(clearNumber(rawCtr[0].s_vrpbs_0 + rawCtr[0].s_vrpbs_2 + rawCtr[0].s_vrpbs_1)) }}
                                                 <!-- {{ numformat(clearNumber(calcResta([rawCtr[0].s_vdo, rawCtr[0].s_vpbs]) + calcResta([rawCtr[0].s_vdo, rawCtr[0].s_vpbs, rawCtr[0].s_vgl]) + calcResta([rawCtr[0].s_vdo, rawCtr[0].s_vpbs, rawCtr[0].s_gld]) )) }} -->
                                            <!-- {{ numformat(clearNumber(calcResta([rawCtr[0].s_vdo, rawCtr[0].s_vpbs]) + calcResta([rawCtr[0].s_vdo, rawCtr[0].s_vpbs, rawCtr[0].s_vgl]) + calcResta([rawCtr[0].s_vdo, rawCtr[0].s_vpbs, rawCtr[0].s_gld]) )) }} -->
                                        </td>
                                        <td>
                                            {{ numformat(clearNumber(rawCtr[0].s_vrpm_0 + rawCtr[0].s_vrpm_1 + rawCtr[0].s_vrpm_2)) }}
                                            <!-- <hr>
                                            {{ numformat(clearNumber(calcResta([rawCtr[0].s_vdo_0_pm, rawCtr[0].s_vppm_0]) + calcResta([rawCtr[0].s_vdo_2_pm, rawCtr[0].s_vgl_2_pm, rawCtr[0].s_vppm_2]) + calcResta([rawCtr[0].s_vdo_1_pm, rawCtr[0].s_gld_1_pm]))) }} -->
                                        </td>
                                    </tr>
                                    <tr class="dk-row" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td colspan="5"></td>
                                        <td>DIFERENCIA</td>
                                        <td :class="df_pbs == 0? 'dk-success': 'text-danger'">
                                            {{ df_pbs }}
                                        </td>
                                        <td :class="df_pm == 0? 'dk-success': 'text-danger'">
                                            {{ df_pm }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="8">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="4" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            FACTURA PBS SIN GLOSA
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td>
                                            <div class="text-bold">FACTURADO</div>
                                            {{ printed('s_vdo_0_pbs') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PBS</div>
                                            {{ printed('s_vpbs_0') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">RESERVA PBS</div>
                                            {{ printed('s_vrpbs_0') }}
                                        </td>
                                        <td :class="df_pbs_glo == 0? 'dk-success td-20': 'txt-danger td-20'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ df_pbs_glo }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="4">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="4" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            FACTURA PM SIN GLOSA
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td>
                                            <div class="text-bold">FACTURADO</div>
                                            {{ printed('s_vdo_0_pm') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PM</div>
                                            {{ printed('s_vppm_0') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">RESERVA PM</div>
                                            {{ printed('s_vrpm_0') }}
                                        </td>
                                        <td :class="df_pm_glo == 0? 'dk-success td-20': 'txt-danger td-20'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ df_pm_glo }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="4">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="5" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            FACTURA PBS CON GLOSA PENDIENTE DE CONCILIAR
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row tr-20" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td>
                                            <div class="text-bold">FACTURADO</div>{{ printed('s_vdo_2_pbs') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PBS</div>{{ printed('s_vpbs_2') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">GLOSADO</div>{{ printed('s_vgl_2_pbs') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">RESERVA PBS</div>{{ printed('s_vrpbs_2') }}
                                        </td>
                                        <td :class="df_pbs_pen == 0? 'dk-success': 'txt-danger'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ df_pbs_pen }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="5">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="5" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            FACTURA PM CON GLOSA PENDIENTE DE CONCILIAR
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row tr-20" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td>
                                            <div class="text-bold">FACTURADO</div>{{ printed('s_vdo_2_pm') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PM</div>{{ printed('s_vppm_2') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">GLOSADO</div>{{ printed('s_vgl_2_pm') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">RESERVA PM</div>{{ printed('s_vrpm_2') }}
                                        </td>
                                        <td :class="df_pm_pen == 0? 'dk-success': 'txt-danger'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ df_pm_pen }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="5">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="5" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            FACTURA PM CON GLOSA CONCILIADA
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row tr-20" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td>
                                            <div class="text-bold">FACTURADO</div>{{ printed('s_vdo_1_pm') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PM</div>{{ printed('s_vppm_1') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">GLOSA DEFINITIVA</div>{{ printed('s_gld_1_pm') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">RESERVA PM</div>{{ printed('s_vrpm_1') }}
                                        </td>
                                        <td :class="df_pm_con == 0? 'dk-success': 'txt-danger'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ df_pm_con }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="5">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border pt-3 pb-2">
                <div class="panel-wrapper collapse in pa-0x">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table mb-0">
                                <thead>
                                    <tr>
                                        <th colspan="5" class="pt-0 pb-2" style="letter-spacing:1px; font-family:Arial">
                                            FACTURA PBS CON GLOSA CONCILIADA
                                            <div>{{ human_period }}</div>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="dk-row tr-20" v-if="rawCtr != null && rawCtr.length > 0">
                                        <td>
                                            <div class="text-bold">FACTURADO</div>{{ printed('s_vdo_1_pbs') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">PAGADO PBS</div>{{ printed('s_vpbs_1') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">GLOSA DEFINITIVA</div>{{ printed('s_gld_1_pbs') }}
                                        </td>
                                        <td>
                                            <div class="text-bold">RESERVA PBS</div>{{ printed('s_vrpbs_1') }}
                                        </td>
                                        <td :class="df_pbs_con == 0? 'dk-success': 'txt-danger'">
                                            <div class="text-bold">DIFERENCIA</div>
                                            {{ df_pbs_con }}
                                        </td>
                                    </tr>
                                    <tr v-if="status == state.LOADING">
                                        <td colspan="5">
                                            <div class="d-flex align-items-center">
                                                <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                                                <span>Cargando...</span>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
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
                                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">ESTRUCTURA DE LA BASE DE DATOS DE FACTURAS</h6>
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
                subtitulo="RESERVAS TÉCNICAS - FACTURAS" 
                separador="|" 
                sindiccionario
                head="file_parse"
                fields="tpo:tipoObligacion|ifa:idFactura|tpp:tipoIdPrestador|idp:idPrestador|nmp:nombrePrestador|pla:planSalud|tra:TContra|idc:idContrato|tus:tipoIdUsuario|ius:idUsuario|iav:idAvisado|fav:FAvis|amb:Ambito|ids:idServicio|ser:DesServicio|dia:DiagPpal|can:Cant|fp:FPres|fr:FRad|vdo:VlrFacturado|vpbs:VlrPagadoPBS|vpac:VlrPagadoPAC|vppm:VlrPagadoPM|fpa:FPago|mpa:MecPago|egl:EstGlosa|vgl:VlrGlosado|gld:glosaDefinitiva|vrpbs:VlrReservaPBS|vrpac:VlrReservaPAC|vrpm:VlrReservaPM|pmx:pres_Max|pac:PAct|ume:UMed|ffa:FFarma|cov:Covid"
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
                        <import-list :coleccion="fuente" titulo="BASE DE DATOS DE FACTURAS"></import-list>
                    </div>
                </div>
            </div>
        </div>
        <local-modal 
            :coleccion="fuente" 
            cantidad="50"
            campos="tpo:tipoObligacion,ifa:idFactura,tpp:tipoIdPrestador,idp:idPrestador,nmp:nombrePrestador,pla:planSalud,tra:TContra,idc:idContrato,tus:tipoIdUsuario,ius:idUsuario,iav:idAvisado,fav:FAvis,amb:Ambito,ids:idServicio,ser:DesServicio,dia:DiagPpal,can:Cant,fp:FPres,fr:FRad,vdo:VlrFacturado,vpbs:VlrPagadoPBS,vpac:VlrPagadoPAC,vppm:VlrPagadoPM,fpa:FPago,mpa:MecPago,egl:EstGlosa,vgl:VlrGlosado,gld:glosaDefinitiva,vrpbs:VlrReservaPBS,vrpac:VlrReservaPAC,vrpm:VlrReservaPM,pmx:pres_Max,pac:PAct,ume:UMed,ffa:FFarma,cov:Covid,crx:Periodo">
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
// import { MongoClient } from 'mongodb';

// let deno = require('mongodb');

export default {
    components: {'local-counter': Counter, 'am-pie': PieChart, 'am-bar': BarChart, 'am-ver': VBarChart, 'select-periodo': Ztime, 'local-modal': Modal},
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''},
        cliente: {type: String, default: ''},
        clientetx: {type: String, default: ''},
        indigena: {type: String, default: ''},
        urol: {type: String, default: ''},
    },
    data() {
        return {
            mocli: null,
            tokens: {},
            keycode: '',
            pathsearch: this.pathdata.replace(/dash.*$/i, 'dash/consulta/auto'),
            fuente: (this.cliente == '0')? 'retec_facturas_0': this.cliente + '_retec_facturas',
            // fuente: '6_retec_facturas',
            krache: 'dash_factu_' + this.cliente,
            krache_ctr: 'dash_factu_ctr_' + this.cliente,
            krache_indi: 'dash_factu_indi_' + this.cliente,
            krache_time: 'time_factu_' + this.cliente,
            section: 'basic',
            display: 'chart',       // table | chart
            opt: [
                {'tx': 'General', 'code': 'basic'}, 
                {'tx': 'Ranking facturas RS', 'code': 'data-1'}, 
                {'tx': 'Ranking facturas RC', 'code': 'data-2'}, 
                {'tx': 'Reservas', 'code': 'controls'}, 
                {'tx': 'Estructura', 'code': 'schema'}, 
                {'tx': 'Importar', 'code': 'import'}
            ],
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            campos: ['tpo', 'ifa', 'tpp', 'idp', 'nmp', 'pla', 'tra', 'idc', 'tus', 'ius', 'iav', 'fav', 'amb', 'ids', 'ser', 'dia', 'can', 'fp', 'fr', 'vdo', 'vpbs', 'vpac', 'vppm', 'fpa', 'mpa', 'egl', 'vgl', 'gld', 'vrpbs', 'vrpac', 'vrpm', 'pmx', 'pac', 'ume', 'ffa', 'cov'],
            pairs: {_id:'Total Registros', tpo:'tipoObligacion', ifa:'idFactura', tpp:'tipoIdPrestador', idp:'idPrestador', nmp:'nombrePrestador', pla:'planSalud', tra:'TContra', idc:'idContrato', tus:'tipoIdUsuario', ius:'idUsuario', iav:'idAvisado', fav:'FAvis', amb:'Ambito', ids:'idServicio', ser:'DesServicio', dia:'DiagPpal', can:'Cant', fp:'FPres', fr:'FRad', vdo:'VlrFacturado', vpbs:'VlrPagadoPBS', vpac:'VlrPagadoPAC', vppm:'VlrPagadoPM', fpa:'FPago', mpa:'MecPago', egl:'EstGlosa', vgl:'VlrGlosado', gld:'glosaDefinitiva', vrpbs:'VlrReservaPBS', vrpac:'VlrReservaPAC', vrpm:'VlrReservaPM', pmx:'pres_Max', pac:'PAct', ume:'UMed', ffa:'FFarma', cov:'Covid'},
            bisch: [{'fx': 'tpo', 'tx': 'tipoObligacion'}, {'fx': 'ifa', 'tx': 'idFactura'}, {'fx': 'tpp', 'tx': 'tipoIdPrestador'}, {'fx': 'idp', 'tx': 'idPrestador'}, {'fx': 'nmp', 'tx': 'nombrePrestador'}, {'fx': 'pla', 'tx': 'planSalud'}, {'fx': 'tra', 'tx': 'TContra'}, {'fx': 'idc', 'tx': 'idContrato'}, {'fx': 'tus', 'tx': 'tipoIdUsuario'}, {'fx': 'ius', 'tx': 'idUsuario'}, {'fx': 'iav', 'tx': 'idAvisado'}, {'fx': 'fav', 'tx': 'FAvis'}, {'fx': 'amb', 'tx': 'Ambito'}, {'fx': 'ids', 'tx': 'idServicio'}, {'fx': 'ser', 'tx': 'DesServicio'}, {'fx': 'dia', 'tx': 'DiagPpal'}, {'fx': 'can', 'tx': 'Cant'}, {'fx': 'fp', 'tx': 'FPres'}, {'fx': 'fr', 'tx': 'FRad'}, {'fx': 'vdo', 'tx': 'VlrFacturado'}, {'fx': 'vpbs', 'tx': 'VlrPagadoPBS'}, {'fx': 'vpac', 'tx': 'VlrPagadoPAC'}, {'fx': 'vppm', 'tx': 'VlrPagadoPM'}, {'fx': 'fpa', 'tx': 'FPago'}, {'fx': 'mpa', 'tx': 'MecPago'}, {'fx': 'egl', 'tx': 'EstGlosa'}, {'fx': 'vgl', 'tx': 'VlrGlosado'}, {'fx': 'gld', 'tx': 'glosaDefinitiva'}, {'fx': 'vrpbs', 'tx': 'VlrReservaPBS'}, {'fx': 'vrpac', 'tx': 'VlrReservaPAC'}, {'fx': 'vrpm', 'tx': 'VlrReservaPM'}, {'fx': 'pmx', 'tx': 'pres_Max'}, {'fx': 'pac', 'tx': 'PAct'}, {'fx': 'ume', 'tx': 'UMed'}, {'fx': 'ffa', 'tx': 'FFarma'}, {'fx': 'cov', 'tx': 'Covid'}],            
            rawData: null,
            rawCtr: null,
            rawIndi: null,
            rawSchema: [],
            periodo: 202106,
			datos: [],
            num_registros: -1,
            status: 'ini',
            status_sch: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            pinload: 0,
            porcion: [{'a': 0, 'b': 5, 'per': '0'}, {'a': 5, 'b': 10, 'per': '33%'}, {'a': 10, 'b': 15, 'per': '67%'}, {'per': '100%'}],
            df_pbs: 0,
            df_pm: 0,

            df_pbs_glo: 0,
            df_pm_glo: 0,
            df_pbs_pen: 0,
            df_pm_pen: 0,
            df_pbs_con: 0,
            df_pm_con: 0,
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
        getTimestamp: function(){
            return (new Date()).toString().slice(11, 24);
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
        clearNumber: function(num, flag='default'){
            return (num % 1 == 0)? num: parseFloat(num).toFixed(2);
        },
        numformat: function(snum){
            var tm = new String(snum);
            return tm.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        printed: function(campo){
            if(this.rawCtr[0][campo] != undefined){
                return this.numformat(this.clearNumber(this.rawCtr[0][campo]));
            }
            return "";
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
        calcResta: function(arr){
            return arr.reduce((ac, elm, i) => i == 0? elm: ac - elm, 0);
        },
        baseResta: function(base, arr, flag=''){
            return base - this.calcResta(arr);
        },
        setSection: function(arg){
            if(this.status != this.state.LOADING && this.status_sch != this.state.LOADING){
                this.section = arg;
                this.manager();
            }
        },
        loadData: function(arg){
            if(this.status != this.state.LOADING){
                this.keycode = generatorKey();
                let pam = new FormData();
                pam.append('tema', this.fuente);
                pam.append('periodo', arg);
                pam.append('clave', this.keycode);
                // pam.append('tema', '6_retec_facturas');
                // pam.append('periodo', '202206');
                console.log('Iniciando: ' + this.getTimestamp());
                this.status = this.state.LOADING;
                this.clock_up();
                // axios.post(this.pathdata + '/data', pam).then(res => {
                customPost(this.pathdata + '/data', pam).then(res => {
                    console.log('Terminado: ' + this.getTimestamp());
                    console.log(res);
                    this.rawData = (res.length > 0)?  res[0]: {'rs_0': [], 'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'cores': [], 's0': [], 'v0': [], 's1': [], 'v1': [], 'pmx': [], 'gp_ext_01': [], 'gp_ext_02': [], 'gp_ext_03': [], 'gp_ext_mec': []};
                    console.log('Raw data');
                    console.log(this.rawData);
                    registerJSON(this.krache, this.rawData, 'per_' + arg);
                    registerJSON(this.krache, arg, 'lastper');
                    this.writeCards();
                    this.status = this.state.LOADED;
                    this.clock_down();
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log('Terminado con error: ' + this.getTimestamp());
                    this.clock_down();
                    console.log(err);
                });
            }
        },
        loadIndigena: function(arg){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('tema', this.fuente);
                pam.append('periodo', arg);
                this.status = this.state.LOADING;
                axios.post(this.pathdata + '/indigena', pam).then(res => {
                    this.rawIndi = (res.data.length > 0)? res.data[0]: {'s_vdo': '', 's_vpbs': '', 'total': ''};
                    registerJSON(this.krache_indi, this.rawIndi, 'per_' + arg);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                })
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
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },        
        writeCards: function(){
            // rs_1: Plan salud
            // rs_2: Tcontra
            // rs_3: Ámbito
            // rs_4: Est Glosa
            if(this.rawData != null){
                this.$refs.gp_0.setDatos(this.rawData['rs_0']);
                this.$refs.gp_1.setDatos(this.rawData['rs_1']);
                this.$refs.gp_2.setDatos(this.rawData['rs_2']);
                this.$refs.gp_3.setDatos(this.rawData['rs_3']);
                this.$refs.gp_4.setDatos(this.rawData['rs_4']);
                this.$refs.gp_ext_01.setDatos(this.rawData['gp_ext_01']);
                this.$refs.gp_ext_02.setDatos(this.rawData['gp_ext_02']);
                this.$refs.gp_ext_03.setDatos(this.rawData['gp_ext_03']);
                this.$refs.gp_ext_mec.setDatos(this.rawData['gp_ext_mec']);

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
                console.log('Data est. glosa ▼');
                console.log(this.rawData['rs_4']);
                let cores = (this.rawData['cores'].length > 0)? this.rawData['cores'][0]: null;
                if(cores != null){
                    this.$refs.cnt_all.setValor(cores.total);
                    this.$refs.cnt_vbs.setValor(this.clearNumber(cores.sum_vbs));
                    this.$refs.cnt_vac.setValor(this.clearNumber(cores.sum_vac));
                    this.$refs.cnt_vpm.setValor(this.clearNumber(cores.sum_vpm));
                    this.$refs.cnt_vdo.setValor(this.clearNumber(cores.sum_vdo));
                    this.$refs.cnt_vgl.setValor(this.clearNumber(cores.sum_vgl));
                    this.$refs.cnt_gde.setValor(this.clearNumber(cores.sum_gde));
                }else{
                    this.$refs.cnt_all.setValor('');
                    this.$refs.cnt_vbs.setValor('');
                    this.$refs.cnt_vac.setValor('');
                    this.$refs.cnt_vpm.setValor('');
                    this.$refs.cnt_vdo.setValor('');
                    this.$refs.cnt_vgl.setValor('');
                    this.$refs.cnt_gde.setValor('');
                }
                this.$refs.tb_0_S.setDatos(this.rawData['s0']);
                this.$refs.gp_0_S.setDatos(this.rawData['s0'].slice(0, 30).sort((a, b) => a.suma - b.suma));
                this.$refs.tb_0_V.setDatos(this.rawData['v0']);
                this.$refs.gp_0_V.setDatos(this.rawData['v0'].slice(0, 30).sort((a, b) => a.suma - b.suma));
                this.$refs.tb_1_S.setDatos(this.rawData['s1']);
                this.$refs.gp_1_S.setDatos(this.rawData['s1'].slice(0, 30).sort((a, b) => a.suma - b.suma));
                this.$refs.tb_1_V.setDatos(this.rawData['v1']);
                this.$refs.gp_1_V.setDatos(this.rawData['v1'].slice(0, 30).sort((a, b) => a.suma - b.suma));
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
            // let tmp = getRegisterJSON(this.krache, 'sch_' + this.periodo);
            // let tmp = localStorage.getItem('sch_' + this.key_history);
            this.status_sch = this.state.LOADING;
            this.asyncRequest(
                'schema_factura' + this.periodo,
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
            if(force){
                // this.loadSchemaParts();
                // this.loadSchemaTry();
            }else{
                // this.rawSchema = tmp;
                // let num = this.rawSchema.find(elm => elm.field == '_id');
                // let num = this.rawSchema.total;
                // this.num_registros = (num == undefined)? -1: num;
                // this.status_sch = this.state.LOADED;
            }
        },
        loadSchemaTry: function(){
            var pam = new FormData();
            pam.append('tema', this.fuente);
            pam.append('periodo', this.periodo);
            // pam.append('tema', '6_retec_facturas');
            // pam.append('periodo', '202206');
            this.status_sch = this.state.LOADING;
            this.clock_up();
            console.log('Iniciando: ' + this.getTimestamp());
            // axios.post(this.pathdata + '/schema', pam).then(res => {
            customPost(this.pathdata + '/schema', pam).then(res => {
                console.log('Terminando: ' + this.getTimestamp());
                console.log(res);
                if(res.length > 0){
                    let rs = res[0];
                    registerJSON(this.krache, rs, 'sch_' + this.periodo);
                    this.rawSchema = rs;
                    this.num_registros = rs.total;
                    this.status_sch = this.state.LOADED;
                }else{
                    this.status_sch = this.state.FAILED;
                }
                this.clock_down();
            }).catch(err => {
                console.log(err);
                this.status_sch = this.state.FAILED;
                this.clock_down();
                console.log('Terminando con error: ' + this.getTimestamp());
            })
        },
        personal: function(){
            this.asyncRequest(
                'try_one_'+ this.periodo,
                res => {

                },
                this.pathdata + '/controls/1',
                {'tema': this.fuente, 'periodo': this.periodo},
                true,   // first param
                '',     // kcode param
                force   // force param

            );
        },
        manager: function(force=false){
            if('schema' == this.section){
                this.getSchema(force);
            }else if('controls' == this.section){
                console.log('In controls section!' + this.fuente);
                this.asyncRequest(
                    'raw_fac_ctr' + this.periodo,
                    res => {
                        if(!this.isEmpty(res)){
                            this.rawCtr = (res.length > 0)?  res: null;
                            // this.df_pbs = this.numformat(this.clearNumber(this.calcResta([this.rawCtr[0].s_vrpbs, this.calcResta([this.rawCtr[0].s_vdo, this.rawCtr[0].s_vpbs]) + this.calcResta([this.rawCtr[0].s_vdo, this.rawCtr[0].s_vpbs, this.rawCtr[0].s_vgl]) + this.calcResta([this.rawCtr[0].s_vdo, this.rawCtr[0].s_vpbs, this.rawCtr[0].s_gld])]) ));
                            // this.df_pm = this.numformat(this.clearNumber(this.calcResta([this.rawCtr[0].s_vrpm, this.calcResta([this.rawCtr[0].s_vdo, this.rawCtr[0].s_vppm]) + this.calcResta([this.rawCtr[0].s_vdo, this.rawCtr[0].s_vgl, this.rawCtr[0].s_vppm]) + this.calcResta([this.rawCtr[0].s_vdo, this.rawCtr[0].s_gld])]) ));
                            this.df_pbs_glo = this.numformat(this.clearNumber(this.baseResta(this.rawCtr[0].s_vrpbs_0, [this.rawCtr[0].s_vdo_0_pbs, this.rawCtr[0].s_vpbs_0])));
                            this.df_pm_glo = this.numformat(this.clearNumber(this.baseResta(this.rawCtr[0].s_vrpm_0, [this.rawCtr[0].s_vdo_0_pm, this.rawCtr[0].s_vppm_0])));
                            this.df_pbs_pen = this.numformat(this.clearNumber(this.baseResta(this.rawCtr[0].s_vrpbs_2, [this.rawCtr[0].s_vdo_2_pbs, this.rawCtr[0].s_vpbs_2])));  // s_vgl_2_pbs
                            this.df_pm_pen = this.numformat(this.clearNumber(this.baseResta(this.rawCtr[0].s_vrpm_2, [this.rawCtr[0].s_vdo_2_pm, this.rawCtr[0].s_vppm_2])));  // s_vgl_2_pm
                            this.df_pbs_con = this.numformat(this.clearNumber(this.baseResta(this.rawCtr[0].s_vrpbs_1, [this.rawCtr[0].s_vdo_1_pbs, this.rawCtr[0].s_vpbs_1, this.rawCtr[0].s_gld_1_pbs])));

                            
                                                                                                        // FACTURADO  s_vdo_1_pm
                                                                                                        // PAGADO PM	s_vppm_1
                                                                                                        // GLOSA DEFINITIVA	s_gld_1_pm
                                                                                                        // RESERVA PM			s_vrpm_1
                            this.df_pm_con = this.numformat(this.clearNumber(this.rawCtr[0].s_vdo_1_pm - (this.rawCtr[0].s_vppm_1 + this.rawCtr[0].s_gld_1_pm + this.rawCtr[0].s_vrpm_1)));
                            // this.df_pm_con = this.numformat(this.clearNumber(this.baseResta(this.rawCtr[0].s_vrpm_1, [this.rawCtr[0].s_vdo_1_pm, this.rawCtr[0].s_gld_1_pm])));
                            this.df_pbs = this.rawCtr[0].s_vrpbs - (this.rawCtr[0].s_vrpbs_0 + this.rawCtr[0].s_vrpbs_2 + this.rawCtr[0].s_vrpbs_1);
                            this.df_pm = this.rawCtr[0].s_vrpm - (this.rawCtr[0].s_vrpm_0 + this.rawCtr[0].s_vrpm_1 + this.rawCtr[0].s_vrpm_2);
                        }else{
                            console.log('Contenido vacío!');
                        }
                    },
                    this.pathdata + '/controls',
                    {'tema': this.fuente, 'periodo': this.periodo},
                    true,   // first param
                    '',     // kcode param
                    force   // force param
                );
            }else if('data-indigena' == this.section){
                this.rawIndi = getRegisterJSON(this.krache_indi, 'per_' + this.periodo);
                if(this.isEmpty(this.rawIndi)){
                    this.loadIndigena(this.periodo);
                }else{
                    console.log('Cargado en memoria!');
                }
            }else{
                // this.rawData = getRegisterJSON(this.krache, 'per_' + this.periodo);
                this.asyncRequest(
                    'raw_facet_fac' + this.periodo,
                    res => {
                        this.rawData = (res.length > 0)?  res[0]: {'rs_0': [], 'rs_1': [], 'rs_2': [], 'rs_3': [], 'rs_4': [], 'cores': [], 's0': [], 'v0': [], 's1': [], 'v1': [], 'pmx': []};
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
            console.log('Writepath ' + writepath);
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
                    console.log('async request in else block!');
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
            this.$eventBus.$on('select-tus', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'TIPO DE DOCUMENTO', 'periodo': this.periodo, 'filtros': 'tus:' + arg._id, 'foco': 'tus'});
            });
            this.$eventBus.$on('select-pla', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'PLAN SALUD', 'periodo': this.periodo, 'filtros': 'pla:' + arg._id, 'foco': 'pla'});
            });
            this.$eventBus.$on('select-tra', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'TIPO DE CONTRATO', 'periodo': this.periodo, 'filtros': 'tra:' + arg._id, 'foco': 'tra'});
            });
            this.$eventBus.$on('select-amb', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'ÁMBITO', 'periodo': this.periodo, 'filtros': 'amb:' + arg._id, 'foco': 'amb'});
            });
            this.$eventBus.$on('select-tpo', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'EST. GLOSA', 'periodo': this.periodo, 'filtros': 'tpo:' + arg._id, 'foco': 'tpo'});
            });
            this.$eventBus.$on('select-pmx', arg => {
                this.$eventBus.$emit('open-modal', {'titulo': 'PRESUPUESTOS MÁXIMOS', 'periodo': this.periodo, 'filtros': 'pmx:' + arg._id, 'foco': 'pmx'});
            });
            this.$eventBus.$on('time-select', obj => {
                console.log('time-select dispatch!');
                this.periodo = obj.periodo;
                this.manager();
            });
            this.$eventBus.$on('time-refresh', bool => {
                console.log('time refresh dispath!');
                unregisterJSON(this.krache);
                unregisterJSON(this.krache_ctr);
                unregisterJSON(this.krache_indi);
                this.rawData = null;
                this.manager(true);
            });
        }
    },
    mounted() {
        this.listen();
        if(this.urol == 'Consultor'){
            this.opt.pop();
        }
        if(this.indigena == 'on'){
            this.opt.splice(1, 0, {'tx': 'Indígena', 'code': 'data-indigena'});
        }
    }
}
</script>
<style>
.text-upper {text-transform: uppercase !important}
.dk-hand {cursor: pointer !important; user-select: none}
.text-bold {font-weight: bold !important}
.dk-success {color:#29B672 !important}
.dk-disabled, .dk-load {opacity: .5 !important; user-select: none !important; pointer-events: none !important}
.dk-row {color:#000; font-family: Arial}
.dk-row td, .tr-center th {text-align: center !important}
.tr-center th {font-weight: bold}
.tr-20 > td, .td-20 {width: 20%}
.td-30 {width: 33%}
.component-loading .card-view > div {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .panel-body.vega {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
.component-loading .df-options > a {opacity: .35 !important; pointer-events: none !important; cursor:wait !important}
</style>
