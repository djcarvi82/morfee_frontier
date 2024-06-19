<template>
    <div>
        <div v-if="data_show == 'form'">
            <div :class="card_mode? 'panel panel-default card-view p-0 border': ''">
                <div :class="card_mode? 'panel-wrapper collapse in': ''">
                    <div :class="card_mode? 'panel-body pt-0': ''">
                        <div class="wizard clearfix">
                            <div class="steps clearfix">
                                <ul role="tablist">
                                    <li :class="stepClass(1, 'first')" role="tab">
                                        <div class="d-flex align-items-center mx-3">
                                            <span class="number">1</span>
                                            <span class="head-font capitalize-font" v-if="f_tipo == ''">TIPO DE INFORMACIÓN</span>
                                            <div v-else>
                                                <div class="micro-head">RECURSO</div>
                                                <div class="tx-value">{{ txtipo }}</div>
                                            </div>
                                        </div>
                                    </li>
                                    <li :class="stepClass(2)" role="tab">
                                        <div class="d-flex align-items-center mx-3">
                                            <span class="number">2</span>
                                            <span class="head-font capitalize-font" v-if="f_periodo == ''">PERIODO</span>
                                            <div v-else>
                                                <div class="micro-head">PERIODO</div>
                                                <div class="tx-value">{{ f_periodo }}</div>
                                            </div>
                                        </div>
                                    </li>
                                    <li :class="stepClass(3)" role="tab">
                                        <div class="d-flex align-items-center mx-3">
                                            <span class="number">3</span>
                                            <span class="head-font capitalize-font" v-if="f_archivo == ''">ARCHIVO</span>
                                            <div v-else>
                                                <div class="micro-head">ARCHIVO</div>
                                                <div class="tx-value">{{ f_archivo }}</div>
                                            </div>
                                        </div>
                                    </li>
                                    <li :class="stepClass(4, 'last')" role="tab">
                                        <div class="d-flex align-items-center mx-3">
                                            <span class="number">4</span>
                                            <span class="head-font capitalize-font" v-if="status_import == 'init' || status_import == 'loading'">IMPORTAR</span>
                                            <div v-else>
                                                <div class="micro-head">IMPORTAR</div>
                                                <div class="tx-value" v-if="status_import == 'loaded'">Importado</div>
                                                <div class="tx-value" v-if="status_import == 'failed'">Importación fallida</div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                        <div class="p-3 mt-4">
                            <!-- SECTION ONE -->
                            <div :class="(paso == 0)? '': 'd-none'">
                                <div class="p-4 text-center" style="border:4px dashed #EAEAEA; background:#FCFCFC">
                                    <button type="button" class="btn btn-success px-5 pt-3 pb-2" v-on:click="paso = 1">
                                        <i class="fa fa-cloud-upload fs-3"></i>
                                        <div>Iniciar</div>
                                    </button>
                                </div>
                            </div>
                            <div :class="(paso == 1)? '': 'd-none'">
                                <div class="row">
                                    <div class="col-sm-3 col-md-3">
                                        <div :class="(f_tipo == 'liq')? 'border border-success bg-light-success p-4 text-center': 'border p-4 text-center bg-unselect'" v-on:click="setTipo('liq')">
                                            <img :src="base_path + 'ik_liq.png'" alt="">
                                            <h5 class="fs-6">LIQUIDACIÓN</h5>
                                        </div>
                                    </div>
                                    <div class="col-sm-3 col-md-3">
                                        <div :class="(f_tipo == 'ret')? 'border border-success bg-light-success p-4 text-center': 'border p-4 text-center bg-unselect'" v-on:click="setTipo('ret')">
                                            <img :src="base_path + 'ik_ret.png'" alt="">
                                            <h5 class="fs-6">RETENCIONES</h5>
                                        </div>
                                    </div>
                                    <div class="col-sm-3 col-md-3">
                                        <div :class="(f_tipo == 'esp')? 'border border-success bg-light-success p-4 text-center': 'border p-4 text-center bg-unselect'" v-on:click="setTipo('esp')">
                                            <img :src="base_path + 'ik_esp.png'" alt="">
                                            <h5 class="fs-6">POB. ESPECIAL</h5>
                                        </div>
                                    </div>
                                    <div class="col-sm-3 col-md-3">
                                        <div :class="(f_tipo == 'nase')? 'border border-success bg-light-success p-4 text-center': 'border p-4 text-center bg-unselect'" v-on:click="setTipo('nase')">
                                            <img :src="base_path + 'ik_nase.png'" alt="">
                                            <h5 class="fs-6">POB. NO ASEGURADA</h5>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-4 text-right">
                                    <button class="btn btn-success" type="button" disabled>Anterior</button>
                                    <button type="button" class="btn btn-success" v-on:click="paso = 2" :disabled="f_tipo == ''">Siguiente</button>
                                </div>
                            </div>
                            <div :class="(paso == 2)? '': 'd-none'">
                                <select-periodo manual></select-periodo>
                                <div class="mt-4 text-right">
                                    <button class="btn btn-success" type="button" v-on:click="paso = 1">Anterior</button>
                                    <button type="button" class="btn btn-success" v-on:click="paso = 3" :disabled="f_periodo == ''">Siguiente</button>
                                </div>
                            </div>
                            <div :class="(paso == 3)? '': 'd-none'">
                                <div class="input-group">
                                    <input type="text" class="form-control" placeholder="Ningún archivo seleccionado" v-model="f_archivo" readonly>
                                    <input type="file" class="d-none" id="fl_file" v-on:change="selectFile">
                                    <span class="input-group-btn" v-if="fileTarget != null">
                                        <button type="button" class="btn btn-danger" v-on:click="clearFile"><i class="fa fa-trash"></i> Remover</button>
                                    </span>
                                    <span class="input-group-btn" v-else>
                                        <button type="button" class="btn btn-primary" v-on:click="dispatchFocus"><i class="fa fa-upload"></i> Seleccionar archivo</button>
                                    </span>
                                </div>
                                <div class="mt-4 text-right">
                                    <button class="btn btn-success" type="button" v-on:click="paso = 2">Anterior</button>
                                    <button type="button" class="btn btn-success" v-on:click="sendFileUpload" :disabled="fileTarget == null">Importar</button>
                                </div>
                            </div>
                            <div :class="(paso == 4)? '': 'd-none'">
                                <div class="text-center" v-if="status_import == state.LOADING">
                                    <i class="zmdi zmdi-spinner zmdi-hc-spin zmdi-rotate-right zmdi-hc-5x"></i>
                                    <p class="mt-2">Importando datos...</p>
                                </div>
                                <div class="text-center" v-else-if="status_import == state.LOADED">
                                    <i class="icon-check fs-1 txt-success"></i>
                                    <p class="mt-2 mb-3 txt-success">Importación exitosa!</p>
                                    <button class="btn btn-success btn-sm" v-on:click="resetImport">Importar otro recurso</button>
                                </div>
                                <div class="text-center" v-else-if="status_import == state.FAILED">
                                    <i class="zmdi zmdi-alert-triangle zmdi-hc-5x"></i>
                                    <p class="mt-2 mb-3 txt-danger">Ocurrió un error al importar los datos!</p>
                                    <button class="btn btn-success btn-sm" v-on:click="resetImport">Intentar nuevamente</button>
                                </div>
                            </div>
                        </div>
                        <!-- End section content -->
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view p-0 border" v-if="detallar && card_mode">
                <div class="panel-wrapper collapse in">
                    <div class="panel-heading">
                        <div class="d-flex">
                            <h6 class="panel-title fs-5">IMPORTACIONES REALIZADAS</h6>
                            <a href="#" class="inline-block full-screen ms-auto">
                                <i class="zmdi zmdi-fullscreen"></i>
                            </a>
                        </div>
                    </div>
                    <div class="panel-body pt-0">
                        <div class="table-wrap" v-if="registros.length > 0">
                            <div class="table-responsive">
                                <table class="table table-borderedx table-hover mb-0">
                                    <thead>
                                        <tr><th class="colmin">No.</th><th>Tipo</th><th>Periodo</th><th class="text-center">Fecha de importación</th><th class="text-center">Código de importación</th><th class="text-center colmin">Estado</th><th class="text-center colmin">Acción</th></tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(dat, i) in registros" :key="i">
                                            <td class="colmin">{{ i + 1 }}</td>
                                            <td>{{ sources[dat.tipo] }}</td>
                                            <td>{{ dat.periodo }}</td>
                                            <td class="text-center">{{ dat.created_at }}</td>
                                            <td class="text-center">CTR-{{ dat.id }}</td>
                                            <td class="text-center"><i class="fa fa-check-circle text-success fs-4"></i></td>
                                            <td class="text-center">
                                                <div class="d-flex justify-content-center mx-4">
                                                    <a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Datos" v-on:click="loadBatch(dat.id, dat.diccionario)"><i class="fa fa-list-alt"></i></a>
                                                    <a href="javascript:void(0)" class="ms-4" data-toggle="tooltip" data-original-title="Eliminar" v-on:click="preDelete(dat.id)"><i class="fa fa-close text-danger"></i></a>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div><!-- End table-wrap -->
                        <div class="bg-light-warning border border-warning txt-dark px-3 py-3 mx-3 mb-2" v-else>
                            <div class="d-flex align-items-center">
                                <i class="fa fa-warning fs-3 me-3 txt-warning"></i>
                                <div>
                                    No se han realizado importaciones en la LMA de este cliente!
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div><!-- End form and history -->
        <div v-else>
            <div class="panel panel-default card-view p-0 border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title fs-5">REGISTROS DE LA IMPORTACIÓN</h6>
                            <a href="javascript:void(0)" v-on:click="data_show = 'form'"><i class="zmdi zmdi-close"></i></a>
                        </div>
                    </div>
                    <div class="panel-body pt-0">
                        <div class="table-wrap" v-if="lote.length > 0">
                            <div class="table-responsive">
                                <table class="table display table-striped table-borderedx table-hover table-sm mb-0">
                                    <thead>
                                        <tr>
                                            <th class="colmin">No.</th>
                                            <th class="text-center" v-for="(field, i) in diccionario" :key="i">{{ field }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(reg, i) in lote" :key="i">
                                            <td class="colmin">{{ (i + 1) * pagina }}</td>
                                            <td class="text-center" v-for="(field, c) in diccionario" :key="c">{{ reg[field] }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div><!-- End table-wrap -->
                        <div class="bg-light-warning border border-warning txt-dark px-3 py-3 mx-3 mb-2" v-else>
                            <div class="d-flex align-items-center">
                                <i class="fa fa-warning fs-3 me-3 txt-warning"></i>
                                <div>
                                    Esta importación no tiene datos!
                                </div>
                            </div>
                        </div>
                        <div class="btn-group mt-4 mx-3" v-if="paginas.length > 0">
                            <button type="button" v-on:click="loadBatch(lastId, null, pg, false)" :class="(pagina == pg)? 'btn btn-success px-3': 'btn btn-default btn-outline px-3'" v-for="(pg, i) in paginas" :key="i">{{ pg }}</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Periodo from './tools/ymonth.vue';
export default {
    components: {'select-periodo': Periodo},
    props: {
        card_mode: {type: Boolean, default: false},
        detallar: {type: Boolean, default: false},
        ruta: {type: String, default: 'none'},
        history: {type: String, default: 'none'},
        autorize: {type: String, default: 'none'},
        batch: {type: String, default: 'none'}
    },
    data() {
        return {
            data_show: 'form',
            sources: {'liq': 'Liquidación', 'ret': 'Retenciones', 'esp': 'Pob. Especial', 'nase': 'Pob. no asegurada'},
            // statusCode: {1: 'Archivo guardado', 2: 'Archivo importado', 3: 'Vaciado'},
            base_path: '',
            paso: 0,
            f_tipo: '',
            f_periodo: '',
            f_archivo: '',
            fileTarget: null,
            txyear: '',
            txmonth: '',
            txtipo: '',
            txrecurso: '',
            registros: [],
            diccionario: [],
            lote: [],
            paginas: [],
            pagina: 1,
            memory: -1,
            lastId: -1,
            status_import: 'init',
            state: {'INIT': 'init', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
        }
    },
    methods: {
        loadData: function(){
            if(this.history != 'none' && this.detallar){
                axios.post(this.history).then(res => this.registros = res.data).catch(err => {console.log(err)});
            }
        },
        loadBatch: function(id, dic, page=1, firstTime=true){
            this.lastId = id;
            this.pagina = page;
            if(firstTime){
                this.diccionario = (dic != undefined)? dic.split("|"): [];
            }
            var param = new FormData();
            param.append('codex', id);
            param.append('pagina', this.pagina);
            if(!firstTime && this.memory != -1) param.append('memory', this.memory);
            axios.post(this.batch, param).then(res => {
                console.log(res.data);
                if(firstTime){
                    this.memory = res.data.attach;
                    var num = Math.ceil(this.memory / 100);
                    this.paginas = [];
                    for(var i = 1; i <= num; i++){
                        this.paginas.push(i);
                    }
                }
                this.lote = res.data.datos;
                this.data_show = 'batch';
            }).catch(err => {console.log(err)});
        },
        stepClass: function(step, pre = ''){
            if(this.paso < step){
                return (pre == '')? 'disabled py-3': pre + ' disabled py-3';
            }else if(this.paso == step){
                if(this.paso == 4 && this.status_import == this.state.LOADED){
                    return (pre == '')? 'done py-3 boletf': pre + ' done py-3 boletf';
                }else{
                    return (pre == '')? 'current py-3': pre + ' current py-3';
                }
            }else{
                return (pre == '')? 'done py-3 boletf': pre + ' done py-3 boletf';
            }
        },
        setTipo: function(arg){
            this.f_tipo = arg;
            this.txtipo = this.sources[arg];
        },
        selectFile: function(evt){
            if(evt.target.files.length > 0){
                this.fileTarget = evt.target.files[0];
                this.f_archivo = this.fileTarget.name;
            }else{
                this.fileTarget = null;
                this.f_archivo = '';
            }
        },
        clearFile: function(){
            document.getElementById('fl_file').value = "";
            this.fileTarget = null;
            this.f_archivo = '';
        },
        dispatchFocus: function(){
            document.getElementById('fl_file').click();
        },
        sendFileUpload: function(){
            if(this.fileTarget != null){
                let fdata = new FormData();
                fdata.append('csrfmiddlewaretoken', token_root);
                fdata.append('tipo', this.f_tipo);
                fdata.append('periodo', this.f_periodo);
                fdata.append('rawfile', this.fileTarget);
                fdata.append('estado', 1);
                this.status_import = this.state.LOADING;
                this.paso = 4;
                axios.post(this.ruta, fdata, {headers: {'content-type': 'multipart/form-data', 'cache': false, 'processData': false}}).then(res => {
                    this.status_import = (res.data.status == 'success')? this.state.LOADED: this.state.FAILED;
                    this.loadData();
                }).catch(err => {
                    console.log(err);
                    this.status_import = this.state.FAILED;
                });
            }
        },
        preDelete: function(cid){
            swal({
                title: "¿Está seguro?",
                text: "Confirma que procederá a eliminar todos los registros que hacen parte de esta importación?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#f0c541",
                confirmButtonText: "Eliminar",
                cancelButtonText: "Cancelar",
                closeOnConfirm: true
            }, () => this.secureDelete(cid));
        },
        secureDelete: function(cx){
            let params = new FormData();
            params.append('codex', cx);
            axios.post(this.autorize, params).then(res => {
                console.log(res.data);
                if(res.data.status == 'success'){
                    this.loadData();
                }
            }).catch(err => {console.log(err)});
        },
        resetImport: function(){
            this.f_tipo = '';
            this.f_periodo = '';
            this.txyear = '';
            this.txmonth = '';
            this.txtipo = '';
            this.txrecurso = '';
            this.clearFile();
            this.status_import = this.state.INIT;
            this.paso = 1;
        },
        listen: function(){
            this.$eventBus.$on('mf-change-date', evt => {
                if(evt.change == 'month'){
                    this.f_periodo = evt.periodo;
                    this.txyear = evt.year;
                    this.txmonth = evt.month;
                }
            });
        }
    },
    mounted() {
        this.listen();
        this.base_path = static_path;
        this.loadData();
    }
}
</script>
<style scoped>
.micro-head {letter-spacing: 1px; font-size:.65rem; color:#FFF !important}
.tx-value {color:#FFF !important; font-weight: 100 !important; letter-spacing: 1px; font-size:1.3rem; line-height: 1rem}
li.current span.head-font.capitalize-font {color:#FFF !important; font-weight: bold; letter-spacing: 2px}
li.done span.head-font.capitalize-font {color:#FFF !important; font-weight: bold; letter-spacing: 2px}
li.disabled span.head-font.capitalize-font {color:#B6AAAA !important}
.bg-unselect {background: #F7F7F7}
.boletf {border-left:1px solid #FFFFFF55}
.wizard > .steps > ul > li {width: 25% !important}
</style>
