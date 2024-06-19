<template>
    <div>
        <div class="row">
            <div class="col-sm-12 col-md-12">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left"><h6 class="panel-title txt-dark" id="titleMain">SISTEMA DE IMPORTACIÓN DE LMA</h6></div>
                        <div class="pull-right"><a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a></div><div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="panel-steps">
                                <div class="row">
                                    <div class="col-sm-3 col-md-3">
                                        <div class="box-step">
                                            <i :class="(step > 1)? 'fa fa-calendar font-24 txt-success': 'fa fa-calendar font-24'"></i>
                                            <div class="mb-5">Periodo</div>
                                            <span class="label label-success font-15 label-expand" v-if="f_periodo != ''">{{ f_periodo }}</span>
                                        </div>
                                    </div>
                                    <div class="col-sm-3 col-md-3">
                                        <div class="box-step">
                                            <i :class="(step > 2)? 'fa fa-cubes font-24 txt-success': 'fa fa-cubes font-24'"></i>
                                            <div class="mb-5">Tipo de recurso</div>
                                            <span class="label label-success font-15 label-expand" v-if="f_recurso != ''">{{ txrecurso }}</span>
                                        </div>
                                    </div>
                                    <div class="col-sm-3 col-md-3">
                                        <div class="box-step">
                                            <i class="fa fa-file-text-o font-24"></i>
                                            <div class="mb-5">Archivo</div>
                                            <span class="label label-success font-15 label-expand" v-if="f_archivo != ''">{{ f_archivo }}</span>
                                        </div>
                                    </div>
                                    <div class="col-sm-3 col-md-3">
                                        <div class="box-step">
                                            <i class="fa fa-upload font-24"></i>
                                            <div class="mb-5">Importado</div>
                                            <span class="label label-success font-15 label-expand" v-if="is_import">Finalizado</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- SECTION ONE -->
                            <div :class="(step == 1)? '': 'lc_hidden'">
                                <select-periodo predata="04" manual></select-periodo>
                                <div class="pull-right mt-20">
                                    <button type="button" class="btn btn-success" v-on:click="step = 2" :disabled="f_periodo == ''">Siguiente</button>
                                </div>
                                <div class="clearfix"></div>
                            </div>
                            <!-- SECTION TWO -->
                            <div :class="(step == 2)? 'row': 'lc_hidden'">
                                <div class="col-sm-3 col-md-3">
                                    <div :class="(f_recurso == 'liq')? 'box-card is-target': 'box-card'" v-on:click="setRecurso('liq')">
                                        <img :src="static_url + 'ik_liq.png'" alt="">
                                        <div class="box-item">LIQUIDACIÓN</div>
                                    </div>
                                </div>
                                <div class="col-sm-3 col-md-3">
                                    <div :class="(f_recurso == 'ret')? 'box-card is-target': 'box-card'" v-on:click="setRecurso('ret')">
                                        <img :src="static_url + 'ik_ret.png'" alt="">
                                        <div class="box-item">RETENCIONES</div>
                                    </div>
                                </div>
                                <div class="col-sm-3 col-md-3">
                                    <div :class="(f_recurso == 'esp')? 'box-card is-target': 'box-card'" v-on:click="setRecurso('esp')">
                                        <img :src="static_url + 'ik_esp.png'" alt="">
                                        <div class="box-item">POB. ESPECIAL</div>
                                    </div>
                                </div>
                                <div class="col-sm-3 col-md-3">
                                    <div :class="(f_recurso == 'nase')? 'box-card is-target': 'box-card'" v-on:click="setRecurso('nase')">
                                        <img :src="static_url + 'ik_nase.png'" alt="">
                                        <div class="box-item">POB. NO ASEGURADA</div>
                                    </div>
                                </div>
                                <div class="col-sm-12 col-md-12">
                                    <div class="pull-right mt-20">
                                        <button type="button" class="btn btn-success" v-on:click="backStep">Anterior</button>
                                        <button type="button" class="btn btn-success" v-on:click="step = 3" :disabled="f_recurso == ''">Siguiente</button>
                                    </div>
                                    <div class="clearfix"></div>
                                </div>
                            </div>
                            <!-- SECTION THREE -->
                            <div :class="(step == 3)? 'mt-5': 'lc_hidden'">
                                <div class="input-group">
                                    <input type="text" class="form-control" placeholder="Ningún archivo seleccionado" v-model="f_archivo" readonly>
                                    <input type="file" class="lc_hidden" id="fl_file" accept="application/json" v-on:change="selectFile">
                                    <span class="input-group-btn" v-if="fileTarget != null">
                                        <button type="button" class="btn btn-danger" v-on:click="clearFile"><i class="fa fa-trash"></i> Remover</button>
                                    </span>
                                    <span class="input-group-btn" v-else>
                                        <button type="button" class="btn btn-primary" v-on:click="dispatchFocus"><i class="fa fa-upload"></i> Seleccionar archivo</button>
                                    </span>
                                </div>
                                <div class="pull-right mt-20">
                                    <button type="button" class="btn btn-success" v-on:click="backStep">Anterior</button>
                                    <button type="button" class="btn btn-success" v-on:click="sendFileUpload" :disabled="f_archivo == ''">Siguiente</button>
                                </div>
                                <div class="clearfix"></div>
                            </div>
                            <!-- SECTION FOUR -->
                            <div :class="(step == 4)? 'mt-5': 'lc_hidden'">
                                <div v-if="is_import">
                                    <div class="alert alert-success">
                                        Los datos del archivo han sido cargados correctamente en la base de datos!
                                    </div>
                                </div>
                                <div v-else>
                                    <div class="alert alert-success">
                                        Archivo cargado correctamente en el servidor!
                                    </div>
                                    <div class="pull-right mt-20">
                                        <button type="button" class="btn btn-success" v-on:click="importFile(precodigo)">Importar datos del archivo</button>
                                    </div>
                                    <div class="clearfix"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div><!-- End row -->
        <div class="row">
            <div class="col-sm-12 col-md-12">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left"><h6 class="panel-title txt-dark" id="titleMain">HISTÓRICO DE IMPORTACIONES</h6></div>
                        <div class="pull-right"><a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a></div><div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <table class="table table-striped table-bordered">
                                <thead>
                                    <tr>
                                        <th>Recurso</th>
                                        <th>Código</th>
                                        <th>Estado</th>
                                        <th class="text-center">Acciones</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(reg, i) in registros" :key="i">
                                        <td>{{ reg.recurso }}</td>
                                        <td>{{ reg.codigo }}</td>
                                        <td>{{ statusCode[reg.estado] }}</td>
                                        <td class="text-center" v-if="reg.estado == 3">
                                            <span class="label label-primary" v-on:click="importFile(reg.codigo)">Reimportar datos</span>
                                            <span class="label label-danger" v-on:click="removeFile(reg.codigo)">Eliminar</span>
                                        </td>
                                        <td class="text-center" v-else>
                                            <span class="label label-primary" v-if="reg.estado == 2" v-on:click="clearImport(reg.codigo)">Vaciar</span>
                                            <span class="label label-warning" v-else-if="reg.estado == 1" v-on:click="importFile(reg.codigo)">Importar datos</span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div><!-- End row -->
    </div>
</template>
<script>
import Recurso from './tools/ymonth.vue';

export default {
    components: {'select-periodo': Recurso},
    props: {
        titulo: {type: String, default: 'Título'},
        static_url: {type: String, default: ''},
        uploadpath: {type: String, default: ''},
        token: {type: String, default: ''},
        loadpath: {type: String, default: ''},
        pushpath: {type: String, default: ''},
        clearpath: {type: String, default: ''},
        deletepath: {type: String, default: ''}
    },
    data(){
        return {
            step: 1,
            steps_fields: ['', 'f_periodo', 'f_recurso', 'f_archivo', 'f_etl'],
            sources: {'liq': 'Liquidación', 'ret': 'Retenciones', 'esp': 'Población Especial', 'nase': 'Población no asegurada'},
            statusCode: {1: 'Archivo guardado', 2: 'Archivo importado', 3: 'Vaciado'},
            fileSelector: null,
            fileTarget: null,
            f_periodo: '',
            f_recurso: '',
            f_archivo: '',
            f_etl: '',
            txyear: '',
            txmonth: '',
            txrecurso: '',
            registros: [],
            is_import: false,
            precodigo: '',
        }
    },
    computed: {
        campos: function(){
            return 'Periodo: ' + this.f_periodo + "\r\n" + 'Recurso: ' + this.f_recurso;
        }
    },
    methods: {
        loadData: function(){
            if(this.loadpath != ''){
                axios.post(this.loadpath).then(res => {
                    this.registros = res.data;
                }).catch(err => {console.log(err)});
            }
        },
        dispatchFocus: function(){
            document.getElementById('fl_file').click();
        },
        clearFile: function(){
            document.getElementById('fl_file').value = "";
            this.fileTarget = null;
            this.f_archivo = '';
        },
        getVarStep: function(){
            return this[this.steps_fields[this.step]];
        },
        nextStep: function(num){
            if(num == (this.step + 1)){
                if(this.getVarStep() != ''){
                    this.step = num;
                }
            }
        },
        backStep: function(){
            if(this.step > 1){
                this[this.steps_fields[this.step]] = '';
                this.step--;
            }
        },
        setRecurso: function(arg){
            if(this.step == 2){
                this.f_recurso = arg;
                this.txrecurso = this.sources[arg];
            }
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
        sendFileUpload: function(){
            if(this.fileTarget != null){
                let codigo = this.f_archivo.replace(/^.*_/, '').replace(/\.\w+$/, '');
                let fdata = new FormData();
                fdata.append('rawfile', this.fileTarget);
                fdata.append('csrfmiddlewaretoken', this.token);
                fdata.append('codigo', codigo);
                fdata.append('recurso', this.txrecurso);
                fdata.append('filename', 'media/' + this.f_archivo);
                fdata.append('modulo', 'ase');
                fdata.append('periodo', this.f_periodo);
                fdata.append('estado', 1);
                fdata.append('total', 0);
                fdata.append('user_id', 1);
                axios.post(this.uploadpath, fdata, {headers: {'content-type': 'multipart/form-data', 'cache': false, 'processData': false}}).then(res => {
                    console.log(res.data);
                    this.precodigo = res.data.codigo;
                    console.log(this.precodigo);
                    this.step = 4;
                }).catch(err => {
                    console.log('Errata');
                    console.log(err);
                });
            }
        },
        importFile: function(codex){
            if(codex != ''){
                let fdata = new FormData();
                fdata.append('codigo', codex);
                axios.post(this.pushpath, fdata).then(res => {
                    console.log(res.data);
                    this.is_import = true;
                    this.loadData();
                }).catch(err => {console.log(err)});
            }else{
                alert('No se encontró el código de importación!');
            }
        },
        clearImport: function(codex){
            if(codex != ''){
                let fdata = new FormData();
                fdata.append('codigo', codex);
                axios.post(this.clearpath, fdata).then(res => {
                    console.log(res.data);
                    this.loadData();
                }).catch(err => {console.log(err)});
            }else{
                alert('No se encontró el código de importación!');
            }
        },
        removeFile: function(codex){
            if(codex != ''){
                let fdata = new FormData();
                fdata.append('codigo', codex);
                axios.post(this.deletepath, fdata).then(res => {
                    console.log(res.data);
                    this.loadData();
                }).catch(err => {console.log(err)});
            }else{
                alert('No se encontró el código de importación!');
            }
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
    mounted(){
        console.log('Import System!');
        this.listen();
        this.loadData();
        //alert('Fihama');
    }
}
</script>
<style scoped>
    .box-card {border:1px solid #DDD; margin:0 auto; padding:1.5rem !important; text-align:center; cursor:pointer}
    .box-card:hover {background:linear-gradient(#F4F4F4,#FFFFFF)}
    .box-card:hover > .box-item {font-weight: bold; color:#000}
    .box-card.is-target {background:linear-gradient(#F6F6EB, #EFD986); border:1px solid #F7D00B}

    .box-step {text-align: center}

    .lc_hidden {display: none !important}
    .label.label-expand {padding-left: 10px !important; padding-right: 10px !important}
    .panel-steps {border:1px solid #DEDEDE; background:linear-gradient(#FFFFFF, #F4F4F4); margin-bottom:20px; padding-top:20px; padding-bottom:20px}
</style>