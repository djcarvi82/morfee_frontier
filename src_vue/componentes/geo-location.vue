<template>
    <div>
        <div class="row">
            <div class="col-sm-2">
                <div class="tab-struct custom-tab-2" style="margin-left:-5px; margin-right:-5px">
                    <ul class="nav nav-tabs">
                        <li :class="modo_search == 'filtro'? 'active': ''"><a href="javascript:void(0)" v-on:click="setSearchMode('filtro')">Filtros</a></li>
                        <li :class="modo_search == 'near'? 'active': ''"><a href="javascript:void(0)" v-on:click="setSearchMode('near')">Proximidad</a></li>
                    </ul>
                </div>
                <div class="panel panel-default card-view border">
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body" v-if="modo_search == 'filtro'">
                            <div class="btn-group btn-group-justified mb-4">
                                <div :class="modo == 'mapa'? 'btn btn-xs btn-primary': 'btn btn-xs btn-default'" v-on:click="setModo('mapa')">Mapa</div>
                                <div :class="modo == 'tabla'? 'btn btn-xs btn-primary': 'btn btn-xs btn-default'" v-on:click="setModo('tabla')">Tabla</div>
                            </div>
                            <div class="btn-group btn-group-justified mb-4">
                                <div :class="(style == 1)? 'btn btn-xs btn-font px-1 btn-primary': 'btn btn-xs btn-font px-1 btn-default'" :disabled="modo != 'mapa'" v-on:click="changeMap(1)">Estilo 1</div>
                                <div :class="(style == 2)? 'btn btn-xs btn-font px-1 btn-primary': 'btn btn-xs btn-font px-1 btn-default'" :disabled="modo != 'mapa'" v-on:click="changeMap(2)">Estilo 2</div>
                                <div :class="(style == 3)? 'btn btn-xs btn-font px-1 btn-primary': 'btn btn-xs btn-font px-1 btn-default'" :disabled="modo != 'mapa'" v-on:click="changeMap(3)">Estilo 3</div>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Departamento:</label>
                                <select class="form-control" v-model="f_depto">
                                    <option value=""></option>
                                    <option :value="dep.depto" v-for="(dep, i) in deptos" :key="i">{{ dep.depto }}</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Municipio:</label>
                                <select class="form-control" v-model="f_mcpio">
                                    <option value=""></option>
                                    <option :value="mun.mcpio" v-for="(mun, i) in mcpios" :key="i">{{ mun.mcpio }}</option>
                                </select>
                                <select class="form-control select2 select2-multiple d-none" multiple>
                                    <option value=""></option>
                                    <option :value="mun.mcpio" v-for="(mun, i) in mcpios" :key="i">{{ mun.mcpio }}</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Prestador:</label>
                                <input type="text" class="form-control" v-model="f_nombre">
                            </div>
                            <div class="form-group">
                                <label class="control-label">Naturaleza:</label>
                                <select class="form-control" v-model="f_natu">
                                    <option value=""></option>
                                    <option value="Pública">Pública</option>
                                    <option value="Privada">Privada</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Servicio:</label>
                                <select class="form-control" v-model="f_servi">
                                    <option value=""></option>
                                    <optgroup :label="item.grupo" v-for="item in datagroup" :key="item.gru">
                                        <option :value="ss.cod" v-for="(ss, s) in item.servicios" :key="s">{{ ss.cod + ' - ' + ss.ser }}</option>
                                    </optgroup>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Código CUP:</label>
                                <input type="text" class="form-control" v-model="f_cup">
                            </div>
                            <div class="form-group mt-4 mb-0">
                                <button type="button" class="btn btn-success btn-anim btn-block" v-on:click="loadData" :disabled="status == 'loading'">
                                    <i class="fa fa-search"></i>
                                    <span class="btn-text">Buscar</span>
                                </button>
                                <div class="text-center mt-3" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner fs-5 me-2"></i> Cargando</div>
                            </div>
                        </div>
                        <div class="panel-body" v-else>
                            <div class="alert alert-warning py-2 px-2" v-if="coords == null">
                                De click en el mapa para fijar un punto de referencia.
                            </div>
                            <div v-else>
                                <span class="border border-primary bg-primary px-2" style="background:#0D6EFD">REFERENCIA</span>
                                <div class="border border-primary py-2 px-2 mb-4" style="background:#F7FAFB">
                                    <div class="form-group">
                                        <label class="control-label">Latitud:</label>
                                        <input type="text" class="form-control" :value="coords.lat" readonly>
                                    </div>
                                    <div class="form-group">
                                        <label class="control-label">Longitud:</label>
                                        <input type="text" class="form-control" :value="coords.lng" readonly>
                                    </div>
                                    <button class="btn btn-primary btn-xs btn-block mb-0" type="button" v-on:click="setSearchMode('near')" v-if="coords.fixed">Limpiar</button>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Límite</label>
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <div class="radio radio-success">
                                            <input id="r1" type="radio" v-model="limite" value="5"><label for="r1">5</label>
                                        </div>
                                    </div>
                                    <div>
                                        <div class="radio radio-success">
                                            <input id="r2" type="radio" v-model="limite" value="10"><label for="r2">10</label>
                                        </div>
                                    </div>
                                    <div>
                                        <div class="radio radio-success">
                                            <input id="r3" type="radio" v-model="limite" value="0"><label for="r3">Todos</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Naturaleza:</label>
                                <select class="form-control" v-model="f_natu">
                                    <option value=""></option>
                                    <option value="Pública">Pública</option>
                                    <option value="Privada">Privada</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Servicio:</label>
                                <select class="form-control" v-model="f_servi">
                                    <option value=""></option>
                                    <optgroup :label="item.grupo" v-for="item in datagroup" :key="item.gru">
                                        <option :value="ss.cod" v-for="(ss, s) in item.servicios" :key="s">{{ ss.cod + ' - ' + ss.ser }}</option>
                                    </optgroup>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Código CUP:</label>
                                <input type="text" class="form-control" v-model="f_cup">
                            </div>
                            <div class="form-group mt-4 mb-0">
                                <button type="button" class="btn btn-success btn-anim btn-block" v-on:click="loadProximity" :disabled="status == 'loading' || coords == null">
                                    <i class="fa fa-search"></i>
                                    <span class="btn-text">Buscar</span>
                                </button>
                                <div class="text-center mt-3" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner fs-5 me-2"></i> Cargando</div>
                            </div>
                        </div>
                    </div>
                </div><!-- END PANEL -->
                <div :class="status == state.LOADED? '': 'd-none'">
                    <local-counter ref="counter" class="border" texto="Resultados" valor="0" loading duracion="1" miles></local-counter>
                </div>
            </div>
            <div class="col-sm-10">
                <div :class="modo == 'mapa'? '': 'd-none'">
                    <local-map ref="mapa" :class="style==1? 'border border-primary': ''" altura="82" unidad="vh" localcenter autocentrar zoom="8"></local-map>
                </div>
                <div class="panel panel-default card-view border" v-if="modo == 'tabla'">
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div v-if="status == state.INI" class="alert alert-warning mb-0">
                                <div class="d-flex align-items-center">
                                    <i class="zmdi zmdi-alert-circle-o me-2"></i>
                                    <p>Utilice los filtros del panel izquierdo para visualizar resultados de búsqueda!</p>
                                </div>
                            </div>
                            <div class="table-wrap" v-else>
                                <div class="table-responsive">
                                    <table class="table table-striped">
                                        <thead>
                                            <tr>
                                                <th class="colmin">No.</th>
                                                <th>Prestador</th>
                                                <th>Departamento</th>
                                                <th>Municipio</th>
                                                <th>Dirección</th>
                                                <th>Naturaleza</th>
                                                <th class="colmin px-4">Acción</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(item, i) in rawdata" :key="i" :class="indice >= 0 && indice != i? 'biometal': ''">
                                                <td class="master border border-info" colspan="7" v-if="indice == i && prestador != null">
                                                    <div class="row">
                                                        <div class="col-sm-6">
                                                            <h6 class="txt-dark bolder border-bottom pb-2 mb-4">DATOS DEL PRESTADOR</h6>
                                                            <div class="d-flex justify-content-between mb-3">
                                                                <div>Prestador</div><div>{{ prestador.nom }}</div>
                                                            </div>
                                                            <div class="d-flex justify-content-between mb-3">
                                                                <div>Departamento</div><div>{{ prestador.dep }}</div>
                                                            </div>
                                                            <div class="d-flex justify-content-between mb-3">
                                                                <div>Municipio</div><div>{{ prestador.mcp }}</div>
                                                            </div>
                                                            <div class="d-flex justify-content-between mb-3">
                                                                <div>Dirección</div><div>{{ prestador.dir }}</div>
                                                            </div>
                                                            <div class="d-flex justify-content-between mb-3">
                                                                <div>Naturaleza</div><div>{{ prestador.nat }}</div>
                                                            </div>
                                                            <div class="btn btn-success btn-block" v-on:click="setIndice(-1)">Cerrar detalles</div>
                                                        </div>
                                                        <div class="col-sm-6">
                                                            <h6 class="txt-dark bolder border-bottom pb-2 mb-4">SERVICIOS HABILITADOS</h6>
                                                            <table class="table my-0">
                                                                <thead>
                                                                    <tr>
                                                                        <th class="colmin px-5 pt-0">Código</th>
                                                                        <th class="pt-0">Servicio</th>
                                                                    </tr>
                                                                </thead>
                                                                <tbody>
                                                                    <tr v-for="(pre, p) in prestador.servicios" :key="p" :class="f_servi == pre.cod? 'bg-light-success txt-dark': ''">
                                                                        <td class="text-center py-1">{{ pre.cod }}</td>
                                                                        <td class="py-1">{{ pre.ser }}</td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                </td>
                                                <td class="text-center">{{ i + 1 }}</td>
                                                <td>{{ item.nom }}</td>
                                                <td>{{ item.dep }}</td>
                                                <td>{{ item.mcp }}</td>
                                                <td>{{ item.dir }}</td>
                                                <td>{{ item.nat }}</td>
                                                <td class="text-center">
                                                    <a href="javascript:void(0)" title="Detalles" class="txt-dark hov-success" v-on:click="setIndice(i)"><i class="fa fa-list-alt"></i></a>
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
        </div>
        <!-- END ROW -->
        <!-- *************************  BEGIN MODAL SECTION  ************************* -->
        <div id="modalMap" class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5 class="modal-title" id="myLargeModalLabel">DATOS DEL PRESTADOR</h5>
                            <i class="fa fa-times close fs-5" data-dismiss="modal" aria-hidden="true"></i>
                        </div>
                    </div>
                    <div class="modal-body rowx">
                        <div v-if="prestador != null">
                            <div class="d-flex justify-content-between py-2">
                                <div>Prestador:</div>
                                <div class="txt-dark text-bold">{{ prestador.nom }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-2">
                                <div>NIT:</div>
                                <div class="txt-dark">{{ prestador.nit }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-2">
                                <div>Dirección:</div>
                                <div class="txt-dark">{{ prestador.dir }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-2">
                                <div>Correo:</div>
                                <div class="txt-dark">{{ prestador.ema }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-2">
                                <div>Naturaleza:</div>
                                <div class="txt-dark">{{ prestador.nat }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-2">
                                <div>Departamento:</div>
                                <div class="txt-dark">{{ prestador.dep }}</div>
                            </div>
                            <div class="d-flex justify-content-between py-2">
                                <div>Municipio:</div>
                                <div class="txt-dark">{{ prestador.mcp }}</div>
                            </div>
                            <div class="tab-struct custom-tab-1 d-none">
                                <ul class="nav nav-tabs my-4" role="tablist">
                                    <li :class="(focusMode == 'ser')? 'active': 'text-muted'" v-on:click="focusMode = 'ser'"><a href="javascript:void(0)">SERVICIOS</a></li>
                                    <li :class="(focusMode == 'cup')? 'active': 'text-muted'" v-on:click="focusMode = 'cup'"><a href="javascript:void(0)">CUPS</a></li>
                                </ul>
                            </div>
                            <div class="mt-4 mb-2">
                                <button type="button" :class="(focusMode == 'ser')? focus_css: focus_css + ' btn-outline'" v-on:click="focusMode = 'ser'">SERVICIOS</button>
                                <button type="button" :class="(focusMode == 'cup')? focus_css: focus_css + ' btn-outline'" v-on:click="focusMode = 'cup'">CUPS</button>
                            </div>
                            <div v-if="status_one == state.LOADED">
                                <div v-if="focusMode == 'ser'">
                                    <table class="table table-bordered table-striped my-0" v-if="dataFocus.servicios.length > 0">
                                        <thead class="d-nonex">
                                            <tr>
                                                <th class="text-bold py-1">No.</th><th class="text-bold py-1">Código y servicio</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(elm, i) in dataFocus.servicios" :key="i" :class="elm.foc? 'bg-focus': ''">
                                                <td class="colmin py-1">{{ i + 1 }}</td>
                                                <td class="py-1">{{ elm.cod + ' - ' + elm.ser }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <div class="alert alert-warning mt-3" v-else>
                                        <div class="d-flex align-items-center">
                                            <i class="zmdi zmdi-alert-circle-o me-2"></i>
                                            <p>No se encontraron servicios registrados para este prestador.</p>
                                        </div>
                                    </div>
                                </div>
                                <div v-if="focusMode == 'cup'">
                                    <table class="table table-bordered table-striped my-0" v-if="dataFocus.cups.length > 0">
                                        <thead>
                                            <tr><th class="text-bold py-1">No.</th><th class="text-bold py-1">Código y descripción CUP</th></tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(elm, i) in dataFocus.cups" :key="i" :class="elm.foc? 'bg-focus': ''">
                                                <td class="colmin py-1">{{ i + 1 }}</td><td class="py-1">{{ elm.CODIGO + ' - ' + elm.DESCRIPCION }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <div class="alert alert-warning mt-3" v-else>
                                        <div class="d-flex align-items-center">
                                            <i class="zmdi zmdi-alert-circle-o me-2"></i>
                                            <p>No se encontraron CUPS registrados para este prestador.</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div v-if="status_one == state.LOADING" class="d-flex align-items-center mt-4">
                                <i class="fa fa-spin fa-spinner fs-4 me-3"></i>
                                <p>Cargando servicios y CUPS.</p>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger text-left" data-dismiss="modal">Cerrar</button>
                    </div>
                </div><!-- /.modal-content -->
            </div><!-- /.modal-dialog -->
        </div><!-- /.modal -->
    </div>
</template>
<script>
import Mapa from './mapas/simple-map.vue';
import Counter from './Contador_light.vue';
export default {
    components: {'local-map': Mapa, 'local-counter': Counter},
    data() {
        return {
            modo: 'mapa',
            modo_search: 'filtro',  // filtro | near
            coords: null, // Ref coords of proximity.
            maquetado: false,
            rawdata: [],
            datos: [],
            deptos: [],
            mcpios: [],
            prestador: null,
            dataFocus: null,
            focusMode: 'ser',      // ser || cup
            focus_css: 'btn btn-success btn-xs fixed-btn',
            style: 1,
            f_depto: '',
            f_mcpio: '',
            f_nombre: '',
            f_natu: '',
            f_servi: '',
            f_cup: '',
            d_aux: '',
            limite: 5,
            cups: [],
            status: 'ini',
            status_one: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            indice: -1,
            datagroup: [{"gru":1,"grupo":"Internación","servicios":[{"cod":"101","ser":"GENERAL ADULTOS"},{"cod":"102","ser":"GENERAL PEDIÁTRICA"},{"cod":"103","ser":"PSIQUIATRÍA O UNIDAD DE SALUD MENTAL"},{"cod":"105","ser":"CUIDADO INTERMEDIO NEONATAL"},{"cod":"106","ser":"CUIDADO INTERMEDIO PEDIÁTRICO"},{"cod":"107","ser":"CUIDADO INTERMEDIO ADULTOS"},{"cod":"108","ser":"CUIDADO INTENSIVO NEONATAL"},{"cod":"109","ser":"CUIDADO INTENSIVO PEDIÁTRICO"},{"cod":"110","ser":"CUIDADO INTENSIVO ADULTOS"},{"cod":"111","ser":"UNIDAD DE QUEMADOS ADULTOS"},{"cod":"112","ser":"OBSTETRICIA"},{"cod":"117","ser":"CUIDADO AGUDO EN SALUD MENTAL O PSIQUIATRÍA"},{"cod":"118","ser":"CUIDADO INTERMEDIO EN SALUD MENTAL O PSIQUIATRÍA"},{"cod":"120","ser":"CUIDADO BÁSICO NEONATAL"},{"cod":"121","ser":"ATENCIÓN INSTITUCIONAL DE PACIENTE CRÓNICO"},{"cod":"123","ser":"ATENCIÓN A CONSUMIDOR DE SUSTANCIAS PSICOACTIVAS PACIENTE AGUDO"},{"cod":"124","ser":"INTERNACIÓN PARCIAL EN HOSPITAL"},{"cod":"126","ser":"HOSPITALIZACIÓN EN UNIDAD DE SALUD MENTAL"},{"cod":"127","ser":"INTERNACIÓN HOSPITALARIA CONSUMIDOR DE SUSTANCIAS PSICOACTIVAS"},{"cod":"128","ser":"INTERNACIÓN PARCIAL CONSUMIDOR DE SUSTANCIAS PSICOACTIVAS"},{"cod":"129","ser":"HOSPITALIZACIÓN ADULTOS"},{"cod":"130","ser":"HOSPITALIZACIÓN PEDIÁTRICA"},{"cod":"131","ser":"HOSPITALIZACIÓN EN SALUD MENTAL"},{"cod":"132","ser":"HOSPITALIZACIÓN PARCIAL"},{"cod":"133","ser":"HOSPITALIZACIÓN PACIENTE CRÓNICO CON VENTILADOR"},{"cod":"134","ser":"HOSPITALIZACIÓN PACIENTE CRÓNICO SIN VENTILADOR"},{"cod":"135","ser":"HOSPITALIZACIÓN EN CONSUMO DE SUSTANCIAS PSICOACTIVAS"},{"cod":"138","ser":"CUIDADO BÁSICO DEL CONSUMO DE SUSTANCIAS PSICOACTIVAS"}]},{"gru":2,"grupo":"Quirúrgicos","servicios":[{"cod":"201","ser":"CIRUGÍA DE CABEZA Y CUELLO"},{"cod":"202","ser":"CIRUGÍA CARDIOVASCULAR"},{"cod":"203","ser":"CIRUGÍA GENERAL"},{"cod":"204","ser":"CIRUGÍA GINECOLÓGICA"},{"cod":"205","ser":"CIRUGÍA MAXILOFACIAL"},{"cod":"206","ser":"CIRUGÍA NEUROLÓGICA"},{"cod":"207","ser":"CIRUGÍA ORTOPÉDICA"},{"cod":"208","ser":"CIRUGÍA OFTALMOLÓGICA"},{"cod":"209","ser":"CIRUGÍA OTORRINOLARINGOLOGÍA"},{"cod":"210","ser":"CIRUGÍA ONCOLÓGICA"},{"cod":"211","ser":"CIRUGÍA ORAL"},{"cod":"212","ser":"CIRUGÍA PEDIÁTRICA"},{"cod":"213","ser":"CIRUGÍA PLÁSTICA Y ESTÉTICA"},{"cod":"214","ser":"CIRUGÍA VASCULAR Y ANGIOLÓGICA"},{"cod":"215","ser":"CIRUGÍA UROLÓGICA"},{"cod":"217","ser":"OTRAS CIRUGÍAS"},{"cod":"218","ser":"CIRUGÍA ENDOVASCULAR NEUROLÓGICA"},{"cod":"219","ser":"TRASPLANTE RENAL"},{"cod":"220","ser":"TRASPLANTE DE CORAZÓN"},{"cod":"221","ser":"TRASPLANTE DE HÍGADO"},{"cod":"222","ser":"TRASPLANTE DE PULMÓN"},{"cod":"223","ser":"TRASPLANTE DE RIÑÓN PÁNCREAS"},{"cod":"227","ser":"CIRUGÍA ONCOLÓGICA PEDIÁTRICA"},{"cod":"231","ser":"CIRUGÍA DE LA MANO"},{"cod":"232","ser":"CIRUGÍA DE MAMA Y TUMORES TEJIDOS BLANDOS"},{"cod":"233","ser":"CIRUGÍA DERMATOLÓGICA"},{"cod":"234","ser":"CIRUGÍA DE TÓRAX"},{"cod":"235","ser":"CIRUGÍA GASTROINTESTINAL"},{"cod":"237","ser":"CIRUGÍA PLÁSTICA ONCOLÓGICA"},{"cod":"238","ser":"TRASPLANTE DE INSTESTINO"},{"cod":"239","ser":"TRASPLANTE MULTIVISCERAL"},{"cod":"240","ser":"TRASPLANTE TEJIDOS OCULARES"},{"cod":"241","ser":"TRASPLANTE DE TEJIDO OSTEOMUSCULAR"},{"cod":"242","ser":"TRASPLANTE DE PROGENITORES HEMATOPOYÉTICOS"},{"cod":"243","ser":"TRASPLANTE DE PIEL Y COMPONENTES DE LA PIEL"},{"cod":"244","ser":"TRASPLANTE DE TEJIDOS CARDIOVASCULARES"},{"cod":"245","ser":"NEUROCIRUGÍA"}]},{"gru":3,"grupo":"Consulta Externa","servicios":[{"cod":"301","ser":"ANESTESIA"},{"cod":"302","ser":"CARDIOLOGÍA"},{"cod":"303","ser":"CIRUGÍA CARDIOVASCULAR"},{"cod":"304","ser":"CIRUGÍA GENERAL"},{"cod":"305","ser":"CIRUGÍA NEUROLÓGICA"},{"cod":"306","ser":"CIRUGÍA PEDIÁTRICA"},{"cod":"308","ser":"DERMATOLOGÍA"},{"cod":"309","ser":"DOLOR Y CUIDADOS PALIATIVOS"},{"cod":"310","ser":"ENDOCRINOLOGÍA"},{"cod":"311","ser":"ENDODONCIA"},{"cod":"312","ser":"ENFERMERÍA"},{"cod":"313","ser":"ESTOMATOLOGÍA"},{"cod":"316","ser":"GASTROENTEROLOGÍA"},{"cod":"317","ser":"GENÉTICA"},{"cod":"318","ser":"GERIATRÍA"},{"cod":"320","ser":"GINECOBSTETRICIA"},{"cod":"321","ser":"HEMATOLOGÍA"},{"cod":"323","ser":"INFECTOLOGÍA"},{"cod":"324","ser":"INMUNOLOGÍA"},{"cod":"325","ser":"MEDICINA FAMILIAR"},{"cod":"326","ser":"MEDICINA FÍSICA Y DEL DEPORTE"},{"cod":"327","ser":"MEDICINA FÍSICA Y REHABILITACIÓN"},{"cod":"328","ser":"MEDICINA GENERAL"},{"cod":"329","ser":"MEDICINA INTERNA"},{"cod":"330","ser":"NEFROLOGÍA"},{"cod":"331","ser":"NEUMOLOGÍA"},{"cod":"332","ser":"NEUROLOGÍA"},{"cod":"333","ser":"NUTRICIÓN Y DIETÉTICA"},{"cod":"334","ser":"ODONTOLOGÍA GENERAL"},{"cod":"335","ser":"OFTALMOLOGÍA"},{"cod":"336","ser":"ONCOLOGÍA CLÍNICA"},{"cod":"337","ser":"OPTOMETRÍA"},{"cod":"338","ser":"ORTODONCIA"},{"cod":"339","ser":"ORTOPEDIA Y/O TRAUMATOLOGÍA"},{"cod":"340","ser":"OTORRINOLARINGOLOGÍA"},{"cod":"342","ser":"PEDIATRÍA"},{"cod":"343","ser":"PERIODONCIA"},{"cod":"344","ser":"PSICOLOGÍA"},{"cod":"345","ser":"PSIQUIATRÍA"},{"cod":"346","ser":"REHABILITACIÓN ONCOLÓGICA"},{"cod":"347","ser":"REHABILITACIÓN ORAL"},{"cod":"348","ser":"REUMATOLOGÍA"},{"cod":"354","ser":"TOXICOLOGÍA"},{"cod":"355","ser":"UROLOGÍA"},{"cod":"356","ser":"OTRAS CONSULTAS DE ESPECIALIDAD"},{"cod":"359","ser":"CONSULTA PRIORITARIA"},{"cod":"361","ser":"CARDIOLOGÍA PEDIÁTRICA"},{"cod":"362","ser":"CIRUGÍA DE CABEZA Y CUELLO"},{"cod":"363","ser":"CIRUGÍA DE MANO"},{"cod":"364","ser":"CIRUGÍA DE MAMA Y TUMORES TEJIDOS BLANDOS"},{"cod":"365","ser":"CIRUGÍA DERMATOLÓGICA"},{"cod":"366","ser":"CIRUGÍA DE TÓRAX"},{"cod":"367","ser":"CIRUGÍA GASTROINTESTINAL"},{"cod":"368","ser":"CIRUGÍA GINECOLÓGICA LAPAROSCÓPICA"},{"cod":"369","ser":"CIRUGÍA PLÁSTICA Y ESTÉTICA"},{"cod":"370","ser":"CIRUGÍA PLÁSTICA ONCOLÓGICA"},{"cod":"371","ser":"OTRAS CONSULTAS GENERALES"},{"cod":"372","ser":"CIRUGÍA VASCULAR"},{"cod":"373","ser":"CIRUGÍA ONCOLÓGICA"},{"cod":"374","ser":"CIRUGÍA ONCOLÓGICA PEDIÁTRICA"},{"cod":"375","ser":"DERMATOLOGÍA ONCOLÓGICA"},{"cod":"377","ser":"COLOPROCTOLOGÍA"},{"cod":"379","ser":"GINECOLOGÍA ONCOLÓGICA"},{"cod":"383","ser":"MEDICINA NUCLEAR"},{"cod":"384","ser":"NEFROLOGÍA PEDIÁTRICA"},{"cod":"385","ser":"NEONATOLOGÍA"},{"cod":"386","ser":"NEUMOLOGÍA PEDIÁTRICA"},{"cod":"387","ser":"NEUROCIRUGÍA"},{"cod":"388","ser":"NEUROPEDIATRÍA"},{"cod":"390","ser":"OFTALMOLOGÍA ONCOLÓGICA"},{"cod":"391","ser":"ONCOLOGÍA Y HEMATOLOGÍA PEDIÁTRICA"},{"cod":"393","ser":"ORTOPEDIA ONCOLÓGICA"},{"cod":"395","ser":"UROLOGÍA ONCOLÓGICA"},{"cod":"396","ser":"ODONTOPEDIATRÍA"},{"cod":"397","ser":"MEDICINA ESTÉTICA"},{"cod":"398","ser":"MEDICINAS ALTERNATIVAS - HOMEOPATÍA"},{"cod":"399","ser":"MEDICINAS ALTERNATIVAS - AYURVEDA"},{"cod":"400","ser":"MEDICINAS ALTERNATIVAS - MEDICINA TRADICIONAL CHINA"},{"cod":"404","ser":"MEDICINAS ALTERNATIVAS - NATUROPATÍA"},{"cod":"405","ser":"MEDICINAS ALTERNATIVAS - NEURALTERAPIA"},{"cod":"406","ser":"HEMATOLOGÍA ONCOLÓGICA"},{"cod":"407","ser":"MEDICINA DEL TRABAJO Y MEDICINA LABORAL"},{"cod":"408","ser":"RADIOTERAPIA"},{"cod":"409","ser":"ORTOPEDIA PEDIÁTRICA"},{"cod":"410","ser":"CIRUGÍA ORAL"},{"cod":"411","ser":"CIRUGÍA MAXILOFACIAL"},{"cod":"412","ser":"MEDICINA ALTERNATIVA Y COMPLEMENTARIA - HOMEOPÁTICA"},{"cod":"413","ser":"MEDICINA ALTERNATIVA Y COMPLEMENTARIA - AYURVÉDICA"},{"cod":"414","ser":"MEDICINA ALTERNATIVA Y COMPLEMENTARIA - TRADICIONAL CHINA"},{"cod":"415","ser":"MEDICINA ALTERNATIVA Y COMPLEMENTARIA - NATUROPÁTICA"},{"cod":"416","ser":"MEDICINA ALTERNATIVA Y COMPLEMENTARIA - NEURALTERAPÉUTICA"},{"cod":"417","ser":"TERAPIAS ALTERNATIVAS Y COMPLEMENTARIAS - BIOENERGÉTICA"},{"cod":"418","ser":"TERAPIAS ALTERNATIVAS Y COMPLEMENTARIAS - TERAPIA CON FILTROS"},{"cod":"419","ser":"TERAPIAS ALTERNATIVAS Y COMPLEMENTARIAS - TERAPIAS MANUALES"},{"cod":"420","ser":"VACUNACIÓN"},{"cod":"421","ser":"PATOLOGÍA"},{"cod":"422","ser":"MEDICINA ALTERNATIVA Y COMPLEMENTARIA - OSTEOPÁTICA"},{"cod":"423","ser":"SEGURIDAD Y SALUD EN EL TRABAJO"}]},{"gru":4,"grupo":"Urgencias","servicios":[{"cod":"501","ser":"SERVICIO DE URGENCIAS"}]},{"gru":5,"grupo":"Transporte Asistencial","servicios":[{"cod":"601","ser":"TRANSPORTE ASISTENCIAL BÁSICO"},{"cod":"602","ser":"TRANSPORTE ASISTENCIAL MEDICALIZADO"}]},{"gru":6,"grupo":"Apoyo Diagnóstico y Complementación Terapéutica","servicios":[{"cod":"701","ser":"DIAGNÓSTICO CARDIOVASCULAR"},{"cod":"703","ser":"ENDOSCOPIA DIGESTIVA"},{"cod":"704","ser":"NEUMOLOGÍA - FIBROBRONCOSCOPIA"},{"cod":"705","ser":"HEMODINAMÍA"},{"cod":"706","ser":"LABORATORIO CLÍNICO"},{"cod":"708","ser":"UROLOGÍA - LITOTRIPSIA UROLÓGICA"},{"cod":"709","ser":"QUIMIOTERAPIA"},{"cod":"710","ser":"RADIOLOGÍA E IMÁGENES DIAGNOSTICAS"},{"cod":"711","ser":"RADIOTERAPIA"},{"cod":"712","ser":"TOMA DE MUESTRAS DE LABORATORIO CLÍNICO"},{"cod":"713","ser":"TRANSFUSIÓN SANGUÍNEA"},{"cod":"714","ser":"SERVICIO FARMACÉUTICO"},{"cod":"715","ser":"MEDICINA NUCLEAR"},{"cod":"717","ser":"LABORATORIO CITOLOGÍAS CERVICO-UTERINAS"},{"cod":"718","ser":"LABORATORIO DE PATOLOGÍA"},{"cod":"719","ser":"ULTRASONIDO"},{"cod":"724","ser":"TOMA E INTERPRETACIÓN DE RADIOGRAFÍAS ODONTOLÓGICAS"},{"cod":"725","ser":"ELECTRODIAGNÓSTICO"},{"cod":"728","ser":"TERAPIA OCUPACIONAL"},{"cod":"729","ser":"TERAPIA RESPIRATORIA"},{"cod":"730","ser":"NEUMOLOGÍA LABORATORIO FUNCIÓN PULMONAR"},{"cod":"731","ser":"LABORATORIO DE HISTOTECNOLOGÍA"},{"cod":"732","ser":"ECOCARDIOGRAFÍA"},{"cod":"733","ser":"HEMODIÁLISIS"},{"cod":"734","ser":"DIÁLISIS PERITONEAL"},{"cod":"735","ser":"TERAPIA ALTERNATIVA BIOENERGÉTICA"},{"cod":"736","ser":"TERAPIA ALTERNATIVA CON FILTROS"},{"cod":"737","ser":"TERAPIA ALTERNATIVA MANUAL"},{"cod":"738","ser":"ELECTROFISIOLOGÍA MARCAPASOS Y ARRITMIAS CARDÍACAS"},{"cod":"739","ser":"FISIOTERAPIA"},{"cod":"740","ser":"FONOAUDIOLOGÍA Y/O TERAPIA DEL LENGUAJE"},{"cod":"741","ser":"TAMIZACIÓN DE CÁNCER DE CUELLO UTERINO"},{"cod":"742","ser":"DIAGNÓSTICO VASCULAR"},{"cod":"743","ser":"HEMODINAMIA E INTERVENCIONISMO"},{"cod":"744","ser":"IMÁGENES DIAGNOSTICAS - IONIZANTES"},{"cod":"745","ser":"IMÁGENES DIAGNOSTICAS - NO IONIZANTES"},{"cod":"746","ser":"GESTION PRE-TRANSFUSIONAL"},{"cod":"747","ser":"PATOLOGÍA"},{"cod":"748","ser":"RADIOLOGÍA ODONTOLÓGICA"},{"cod":"749","ser":"TOMA DE MUESTRAS DE CUELLO UTERINO Y GINECOLÓGICAS"}]},{"gru":7,"grupo":"Otros Servicios","servicios":[{"cod":"815","ser":"ATENCIÓN DOMICILIARIA DE PACIENTE CRÓNICO CON VENTILADOR"},{"cod":"816","ser":"ATENCIÓN DOMICILIARIA DE PACIENTE CRÓNICO SIN VENTILADOR"},{"cod":"817","ser":"ATENCIÓN DOMICILIARIA DE PACIENTE AGUDO"},{"cod":"818","ser":"ATENCIÓN PREHOSPITALARIA"},{"cod":"819","ser":"ATENCIÓN A CONSUMIDOR DE SUSTANCIAS PSICOACTIVAS"},{"cod":"820","ser":"ATENCIÓN INSTITUCIONAL NO HOSPITALARIA AL CONSUMIDOR DE SUSTANCIAS PSICOACTIVAS"}]},{"gru":8,"grupo":"Protección Especifica y Detección Temprana","servicios":[{"cod":"907","ser":"PROTECCIÓN ESPECÍFICA - ATENCIÓN DEL PARTO"},{"cod":"908","ser":"PROTECCIÓN ESPECÍFICA - ATENCIÓN AL RECIÉN NACIDO"},{"cod":"909","ser":"DETECCIÓN TEMPRANA - ALTERACIONES DEL CRECIMIENTO Y DESARROLLO ( Menor a 10 años)"},{"cod":"910","ser":"DETECCIÓN TEMPRANA - ALTERACIONES DEL DESARROLLO DEL JOVEN ( De 10 a 29 años)"},{"cod":"911","ser":"DETECCIÓN TEMPRANA - ALTERACIONES DEL EMBARAZO"},{"cod":"912","ser":"DETECCIÓN TEMPRANA - ALTERACIONES EN EL ADULTO ( Mayor a 45 años)"},{"cod":"913","ser":"DETECCIÓN TEMPRANA - CÁNCER DE CUELLO UTERINO"},{"cod":"914","ser":"DETECCIÓN TEMPRANA - CÁNCER SENO"},{"cod":"915","ser":"DETECCIÓN TEMPRANA - ALTERACIONES DE LA AGUDEZA VISUAL"},{"cod":"916","ser":"PROTECCIÓN ESPECÍFICA - VACUNACIÓN"},{"cod":"917","ser":"PROTECCIÓN ESPECÍFICA - ATENCIÓN PREVENTIVA EN SALUD BUCAL"},{"cod":"918","ser":"PROTECCIÓN ESPECÍFICA - ATENCIÓN EN PLANIFICACIÓN FAMILIAR HOMBRES Y MUJERES"}]},{"gru":9,"grupo":"Procesos","servicios":[{"cod":"950","ser":"PROCESO ESTERILIZACIÓN"}]},{"gru":10,"grupo":"Atención Inmediata","servicios":[{"cod":"1101","ser":"ATENCIÓN DEL PARTO"},{"cod":"1102","ser":"URGENCIAS"},{"cod":"1103","ser":"TRANSPORTE ASISTENCIAL BASICO"},{"cod":"1104","ser":"TRANSPORTE ASISTENCIAL MEDICALIZADO"},{"cod":"1105","ser":"ATENCIÓN PREHOSPITALARIA"}]}]
        }
    },
    watch: {
        f_depto: function(val){
            this.mcpios = [];
            for(var i = 0; i < this.deptos.length; i++){
                if(this.deptos[i].depto == val){
                    this.mcpios = this.deptos[i].mcpios.sort(this.orderBy);
                    break;
                }
            }
        },
        f_cup: function(val){
            this.f_cup = val.replace(/^\s+/, '').replace(/\s{2,}/g, ' ');
        }
    },
    methods: {
        orderBy: function(a, b){
            if(a.mcpio > b.mcpio){
                return 1;
            }
            if(a.mcpio < b.mcpio){
                return -1;
            }
            return 0;
        },
        changeMap: function(num){
            if(this.modo == 'mapa'){
                this.$refs.mapa.changeStyle(num);
                this.style = num;
            }
        },
        loadPredata: function(){
            var params = new FormData();
            params.append('coleccion', 'red_nativa_1');
            params.append('grupo', 'dep:mcp');
            params.append('sumar', 1);
            axios.post(root_path + 'aseguramiento/grupos', params).then(res => {
                console.log('rudeku');
                console.log(res);
                var rdep = {};
                res.data[0].rs.forEach(elm => {
                    var dep = elm._id['dep'];
                    if(rdep[dep] == undefined) rdep[dep] = {'depto': dep, 'mcpios': [], 'total': 0};
                    rdep[dep].mcpios.push({'mcpio': elm._id['mcp'], 'total': elm.total});
                    rdep[dep].total += elm.total;
                });
                this.deptos = Object.values(rdep).sort((a, b) => {
                    if(a.depto > b.depto){
                        return 1;
                    }
                    if(a.depto < b.depto){
                        return -1;
                    }
                    return 0;
                });
            }).catch(err => {console.log(err)});
        },
        loadData: function(){
            this.removePins();
            this.d_aux = this.f_cup.replace(/(,\s*|;\s*|\s*-\s*)/g, '|').replace(/\s+$/, '');
            if(this.validateForm() > 0){
                var rawcup = this.f_cup.replace(/(,\s*|;\s*|\s*-\s*)/g, '|').replace(/\s+$/, '');
                this.cups = (rawcup == '')? []: rawcup.split('|');
                // console.log(this.cups);
                var params = new FormData();
                params.append('depto', this.f_depto);
                params.append('mcpio', this.f_mcpio);
                params.append('prestador', this.f_nombre.replace(/(^\s+|\s+$)/g, ''));
                params.append('natu', this.f_natu);
                params.append('servi', this.f_servi);
                params.append('cups', rawcup);
                this.status = this.state.LOADING;
                this.$refs.mapa.loading = true;
                axios.post(root_path + 'aseguramiento/geodata', params).then(res => {
                    this.rawdata = res.data;
                    this.rawdata.forEach((elm, i) => {
                        elm.px = i;
                        this.datos.push({'lat': elm.loc[0], 'lng': elm.loc[1], 'title': elm.nom, 'icon': this.getIcon(elm.nat), 'pxD': i, 'id': elm._id.$oid});
                    });
                    this.drawLocations();
                    this.status = this.state.LOADED;
                    this.$refs.counter.setValor(this.datos.length);
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        loadIPS: function(id){
            var params = new FormData();
            params.append('id', id);
            this.status_one = this.state.LOADING;
            axios.post(root_path + 'aseguramiento/geodata/by/id', params).then(res => {
                this.dataFocus = res.data;
                this.dataFocus.servicios.forEach(elm => elm.foc = (this.f_servi == elm.cod));
                this.dataFocus.servicios.sort((a, b) => {
                    if(a.cod > b.cod){
                        return 1;
                    }
                    return (a.cod < b.cod)? -1: 0;
                });
                this.dataFocus.cups.forEach(elm => elm.foc = this.isFocus(elm.CODIGO));
                this.dataFocus.cups.sort((a, b) => {
                    if(a.CODIGO > b.CODIGO){
                        return 1;
                    }
                    return (a.CODIGO < b.CODIGO)? -1: 0;
                });
                this.dataFocus.cups.sort((a, b) => {
                    return (a.foc === b.foc)? 0: a.foc? -1: 1;
                });
                this.status_one = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status_one = this.state.FAILED;
            });
        },
        loadProximity: function(){
            if(this.coords != null){
                this.removePins();
                var rawcup = this.f_cup.replace(/(,\s*|;\s*|\s*-\s*)/g, '|').replace(/\s+$/, '');
                this.cups = (rawcup == '')? []: rawcup.split('|');
                var params = new FormData();
                params.append('lat', this.coords.lat);
                params.append('lng', this.coords.lng);
                params.append('natu', this.f_natu);
                params.append('servi', this.f_servi);
                params.append('cups', rawcup);
                params.append('limite', this.limite);
                this.status = this.state.LOADING;
                this.$refs.mapa.loading = true;
                this.coords['fixed'] = true;
                this.$refs.mapa.starEvent = false;
                axios.post(root_path + 'aseguramiento/geodata/proximity', params).then(res => {
                    this.rawdata = res.data;
                    this.rawdata.forEach((elm, i) => {
                        elm.px = i;
                        this.datos.push({'lat': elm.loc[0], 'lng': elm.loc[1], 'title': elm.nom, 'icon': this.getIcon(elm.nat), 'pxD': i, 'id': elm._id.$oid});
                    });
                    this.drawLocations();
                    this.status = this.state.LOADED;
                    this.$refs.counter.setValor(this.datos.length);
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        setSearchMode: function(arg){
            this.modo_search = arg;
            this.removePins(true);
            if(this.modo_search == 'near'){
                this.modo = 'mapa';
                this.$refs.mapa.starEvent = true;
            }else{
                this.$refs.mapa.starEvent = false;
            }
        },
        removePins: function(starPin=false){
            this.maquetado = false;
            this.setIndice(-1);
            this.datos = [];
            this.rawdata = [];
            this.$refs.mapa.setDatos(this.datos);
            if(starPin){
                this.$refs.mapa.starClear();
                this.coords = null;
            }
        },
        validateForm: function(){
            var cmps = ['f_depto', 'f_mcpio', 'f_nombre', 'f_natu', 'f_servi', 'd_aux'];
            return cmps.reduce((mem, elm) => mem + ((this[elm] == '')? 0: 1), 0);
        },
        isFocus: function(arg){
            return (this.cups.indexOf(arg) >= 0);
        },
        setModo: function(arg){
            this.modo = arg;
            this.drawLocations();
        },
        getIcon: function(nat){
            return (nat == 'Privada')? static_path + 'pin_01.png': static_path + 'pin_02.png';
        },
        setIndice: function(ind){
            this.indice = ind;
            this.prestador = (ind == -1)? null: this.rawdata[this.indice];
            if(this.prestador != null){
                this.prestador.servicios.sort((a, b) => parseInt(a.cod) - parseInt(b.cod));
            }
        },
        getPX: function(px){
            for(var i = 0; i < this.rawdata.length; i++){
                if(px == this.rawdata[i].px){
                    this.prestador = this.rawdata[i];
                    $('#modalMap').modal('show');
                    break;
                }
            }
        },
        drawLocations: function(){
            if(this.modo == 'mapa' && this.maquetado == false){
                this.maquetado = true;
                this.$refs.mapa.setDatos(this.datos);
            }
        },
        listen: function(){
            this.$eventBus.$on('click-pin', arg => {
                this.loadIPS(arg.id);
                this.getPX(arg.pxD);
            });
            this.$eventBus.$on('position-load', arg => {
                this.coords = arg;
                this.coords['fixed'] = false;
            });
        }
    },
    mounted() {
        this.loadPredata();
        this.listen();
        this.style = this.$refs.mapa.getStyle();
    }
}
</script>
<style scoped>
    .colmin {width:1%; white-space: nowrap; text-align: center}
    .table td.master {background: #FFF}
    .table td.master ~ td {display: none !important}
    .table tr.biometal {user-select: none; pointer-events: none; opacity: .3}
    .bolder {font-weight: bold !important}
    .modal-header {background:#EDEDED; border-bottom:1px solid #CCC}
    .slot {padding-top:.35rem; padding-bottom: .35rem; border:1px solid #DDD}
    .text-bold {font-weight: bold}
    .btn-group > .btn.btn-font {font:normal 11px Arial !important; letter-spacing: 1px; padding:.4rem}
    .bg-focus {background: #2ECD99 !important; color: #FFF !important}
    tr.bg-focus > td {border-color:#FFF !important}
    .tab-struct.custom-tab-2 > .nav.nav-tabs li > a {background:#C0C3C8 !important; color: #F2F2F2}
    .tab-struct.custom-tab-2 > .nav.nav-tabs .active > a {background:#FFF !important; color: #000; border-left:1px solid #DEE2E6; border-right:1px solid #DEE2E6; border-top:1px solid #DEE2E6}

    /* <div class="tab-struct custom-tab-2">
        <ul class="nav nav-tabs">
            <li class="active"><a href="javascript:void(0)">Filtros</a></li> */
</style>