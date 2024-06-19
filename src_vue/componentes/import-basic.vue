<template>
    <div>
        <div class="p-4 text-center d-flex justify-content-center classIni" v-if="step == 1">
            <div class="bg-light-danger border border-danger px-3 py-3" v-if="has_error_dict">
                <div v-if="sindiccionario">
                    <div v-if="f_head == ''" class="d-flex align-items-center">
                        <i class="fa fa-times fs-5 me-2 txt-danger"></i>
                        <span class="txt-danger">No se definió cómo manejará las cabeceras el importador.</span>
                    </div>
                    <div v-if="f_head != 'file_fixed' && f_campos == ''" class="d-flex align-items-center">
                        <i class="fa fa-times fs-5 me-2 txt-danger"></i>
                        <span class="txt-danger">Para el tipo de cabeceras <strong>{{ f_head }}</strong> se require definir los campos requeridos.</span>
                    </div>
                </div>
                <div class="d-flex align-items-center" v-else>
                    <i class="fa fa-warning fs-3 me-3 txt-danger"></i>
                    <div class="txt-danger">No se pudo acceder a los datos de configuración de diccionarios para la colección <strong>{{ prefijo + lc_destino }}</strong>!</div>
                </div>
            </div>
            <span class="txhover" v-on:click="step = 2" v-else>
                <div><i class="fa fa-cloud-upload fs-1"></i></div>
                <div class="text-secondary">Iniciar proceso de importación</div>
                <div class="text-secondary text-bold"><b>{{ subtitulo }}</b></div>
                <div class="text-bold" v-if="clientetx != ''" style="font-weight:bold; letter-spacing:1px">{{ clientetx }}</div>
            </span>
        </div>
        <div class="p-4 classEnd" v-else-if="step == 2">
            <div class="border px-4 py-3" style="background:#F9F9F9">
                <h5 class="mb-4" v-if="titulo != ''">{{ titulo }}</h5>
                <div class="d-flex" v-if="destino == ''">
                    <div class="form-group">
                        <label class="control-label tx-capital">Nombre de la colección: <i :class="lc_destino == ''? 'text-danger': 'text-success'">{{ lc_prefijo + lc_destino }}</i></label>
                        <div class="input-group">
                            <span class="input-group-addon" style="cursor:default">{{ lc_prefijo }}</span>
                            <input type="text" class="form-control" v-model="lc_destino" @keypress.space.prevent="$event => false">
                        </div>
                    </div>
                </div>
                <div class="form-group" v-if="withperiodo">
                    <label class="control-label mb-10">Seleccione el año y el mes (periodo de corte de la base de datos):</label>
                    <div class="input-group">
                        <span class="input-group-btn"><button type="button" class="btn btn-default" v-on:click="sumAnio(-1)">-</button></span>
                        <input type="text" class="form-control bg-white text-center" v-model="f_anio" readonly>
                        <span class="input-group-btn"><button type="button" class="btn btn-default" v-on:click="sumAnio(1)">+</button></span>
                    </div>
                    <div class="btn-group btn-group-justified mt-2">
                        <a href="javascript:void(0)" :class="elm.num == f_mes? 'btn btn-success py-2': 'btn btn-default btn-outline py-2 df-white d-border'" v-for="(elm, i) in filled" :key="i" v-on:click="f_mes = elm.num">{{ elm.min }}</a>
                    </div>
                </div>
                <div :class="lc_destino == ''? 'row no-colection': 'row'">
                    <div :class="(separador_mode == 'hide')? 'd-none': 'col-sm-2'">
                        <div class="form-group">
                            <label class="control-label">Separador:</label>
                            <select class="form-control" v-model="f_separator" :disabled="separador_mode == 'disabled'">
                                <option :value="sp.value" v-for="(sp, i) in sepas" :key="i">{{ sp.label }}</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-sm-2" v-if="codec_mode != 'hide'">
                        <div class="form-group">
                            <label class="control-label">Codec:</label>
                            <select class="form-control" v-model="lc_codec" :disabled="codec_mode == 'fixed'">
                                <option :value="cd" v-for="(cd, i) in codecs" :key="i">{{ cd }}</option>
                            </select>
                        </div>
                    </div>
                    <div :class="len_col">
                        <div class="form-group">
                            <label class="control-label">Archivo:</label>
                            <div class="input-group">
                                <input type="text" class="form-control" placeholder="Ningún archivo seleccionado" v-model="f_archivo" readonly>
                                <input type="file" class="d-none" id="fl_file" accept=".txt, .csv, application/vnd.ms-excel" v-on:change="selectFile">
                                <span class="input-group-btn" v-if="fileTarget != null">
                                    <button type="button" class="btn btn-danger" v-on:click="clearFile"><i class="fa fa-trash"></i> Remover</button>
                                </span>
                                <span class="input-group-btn" v-else>
                                    <button type="button" class="btn btn-primary" v-on:click="dispatchFocus"><i class="fa fa-file-text me-1"></i> Seleccionar archivo</button>
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-2">
                        <div class="form-group">
                            <label for="none" class="control-label">&nbsp;</label>
                            <button type="button" class="btn btn-success btn-block" :disabled="rule_disabled" v-on:click="sendFileUpload"><i class="fa fa-upload me-2"></i> Importar</button>
                        </div>
                    </div>
                </div>
                <div v-if="error_mode == 'show'">
                    <span :class="lc_error == 'ignore'? 'dk-click text-success': 'dk-click'" @click="lc_error = (lc_error == 'strict')? 'ignore': 'strict'"><i :class="lc_error == 'ignore'? 'fa fa-check-square': 'fa fa-square-o'"></i> Ignorar errores de codificación</span>
                </div>
            </div>
            <div v-if="info" class="mt-4">
                <div v-if="f_head != 'file_fixed'" class="txt-dark mb-2">El archivo a importar debe tener la siguiente estructura. <mark v-if="f_head == 'auto'">Sin embargo, no debe incluir las cabeceras.</mark></div>
                <div v-if="f_head != 'file_fixed'">
                    <div class="table-responsive">
                        <table class="table table-import mb-0">
                            <thead>
                                <tr :class="f_head == 'auto'? 'opaco': ''">
                                    <th :class="css_th[elm.match]" v-for="(elm, i) in arr_campos" :key="i">{{ elm.head }}</th>
                                    <th class="bg-danger px-4" v-if="f_head == 'file_parse' && !endchar"></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td v-for="(elm, i) in arr_campos" :key="i"><i>{{ elm.rule }}</i></td>
                                    <td v-if="f_head == 'file_parse' && !endchar">Error</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div v-if="fileTarget != null">
                        <div class="bg-light-danger border border-danger px-3 py-2 mt-4 mb-2 text-danger" v-if="f_head == 'file_parse' && !endchar">
                            <p>La línea de cabeceras no puede terminar con <strong>{{ f_separator }}</strong>, porque implica una columna adicional sin nombre.</p>
                        </div>
                        <div class="bg-light-danger border border-danger px-3 py-2 mt-4 mb-2 text-danger" v-if="arr_campos.length != first_line.length">
                            <p>El número de cabeceras del archivo seleccionado, no coincide con el número esperado. Se esperaban {{ arr_campos.length }}, y se encontraron {{ first_line.length}}, en el archivo <strong>{{ fileTarget.name }}.</strong></p>
                            <p class="mb-0">Verifique el archivo seleccionado, y el separador de campos seleccionado.</p>
                        </div>
                        <div class="bg-light-danger border border-danger px-3 py-2 mt-4 text-danger" v-else-if="arr_campos.length == first_line.length && first_line_pass == false">
                            <p class="mb-0">Las cabeceras del archivo no son las esperadas, favor revisar el archivo seleccionado y el separador de campos.</p>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <div class="alert alert-danger" v-if="fileTarget != null && first_line.length > 0 && first_line_pass == false">
                        <div class="d-flex align-items-center">
                            <i class="fa fa-warning me-2"></i>
                            <p class="mb-0">Verifique el separador de campos seleccionado y el contenido del archivo, debido a que sólo se encuentra una columna de datos, lo cual es improbable.</p>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-import mb-0" v-if="fileTarget != null && first_line.length > 0">
                            <thead><tr><th v-for="(elm, i) in first_line" :key="i">{{ elm.head }}</th></tr></thead>
                            <tbody>
                                <tr>
                                    <td v-for="(elm, i) in first_line" :key="i" v-on:click="openModal(i, elm.rule)" class="on-fire">
                                        <i>{{ elm.rule }}</i>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <div class="p-4 classEnd text-center" v-else-if="step == 3">
            <span class="txhover" v-if="status == state.UPLOADING">
                <div v-if="realtime">
                    <div v-if="importData == null"><i class="fa fa-spinner fa-spin fs-1"></i></div>
                    <div v-else>
                        <div v-if="importData.estado == 'void'">
                            <div><i class="fa fa-spinner fa-spin fs-1"></i></div>
                            <div class="text-secondary">{{ msn[importData.estado] }}</div>
                        </div>
                        <div class="d-flex justify-content-center" v-else>
                            <div><i class="fa fa-spinner fa-spin fs-1"></i></div>
                            <div>
                                <span class="fs-3">{{ formatMiles(importData.total) }}</span>
                                <div class="text-secondary">{{ msn[importData.estado] }}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <div><i class="fa fa-spinner fa-spin fs-1"></i></div>
                    <div class="text-secondary">Importando datos...</div>
                </div>
            </span>
            <span class="txhover txt-success" v-else-if="status == state.UPLOADED">
                <div><i class="icon-check fs-1"></i></div>
                <div class="mt-2">Importación exitosa!</div>
                <button class="btn btn-success btn-xs mt-2" type="button" v-on:click="clearImport">Limpiar</button>
            </span>
            <span class="txt-danger" v-else-if="status == state.FAILED">
                <div><i class="zmdi zmdi-alert-triangle zmdi-hc-5x"></i></div>
                <div class="mt-2">Ocurrió un error al importar los datos!</div>
                <mark class="mt-1" v-if="status_msn != ''">{{ status_msn }}</mark>
                <div class="mt-3">
                    <button class="btn btn-danger btn-sm mt-2" type="button" v-on:click="clearImport">Intentar de nuevo</button>
                </div>
            </span>
        </div>
        <div id="responsive-modal" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" style="display: none;" v-if="fileTarget != null && first_line.length > 0">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h5 class="modal-title" style="text-transform:uppercase">Configuración de columna</h5>
                    </div>
                    <div class="modal-body">
                        <form>
                            <div class="form-group">
                                <label class="control-label">Columna seleccionada:</label>
                                <input type="text" class="form-control" :value="tar_indice >= 0? first_line[tar_indice].head: ''" readonly>
                            </div>
                            <div class="form-group">
                                <label class="control-label mb-10">Tipo de columna:</label>
                                <select class="form-control" v-model="tar_rule">
                                    <option value="Mixed">Mixed</option>
                                    <option value="string">String</option>
                                    <option value="int">Integer</option>
                                </select>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Cerrar</button>
                    </div>
                </div>
            </div>
        </div><!-- END MODAL -->
    </div>
</template>
<script>
export default {
    props: {
        titulo: {type: String, default: ''},
        subtitulo: {type: String, default: 'RÉGIMEN CONTRIBUTIVO'},
        separador: {type: String, default: ','},
        prefijo: {type: String, default: ''},
        destino: {type: String, default: ''},
        separador_mode: {type: String, default: 'normal'},  //  normal | disabled | hide
        info: {type: Boolean, default: false},
        sindiccionario: {type: Boolean, default: false},
        head: {type: String, default: ''},  // auto | file_parse | file_fixed
        fields: {type: String, default: ''},
        rules: {type: String, default: ''},
        skipintro: {type: Boolean, default: false},
        codec: {type: String, default: 'utf-8'},
        codec_mode: {type: String, default: 'hide'},    // hide | show | fixed
        error: {type: String, default: 'strict'},       // strict | ignore
        error_mode: {type: String, default: 'hide'},    // hide | show
        extra: {type: Boolean, default: false},
        clientetx: {type: String, default: ''},
        realtime: {type: Boolean, default: false},
        withperiodo: {type: Boolean, default: false},
    },
    data() {
        return {
            step: 1,
            f_anio: '',
            f_mes: '',
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
            sepas: [{'value': ',', 'label': 'Coma'}, {'value': ';', 'label': 'Punto y coma'}, {'value': '|', 'label': 'Barra pipe'}, {'value': 'tab', 'label': 'Tabulador'}],
            css_th: {'0': '', '1': 'bg-success', '2': 'bg-danger'},
            msn: {'void': 'Enviando archivo al servidor...', 'ini': 'Archivo recibido...', 'open': 'Registros importados...', 'close': 'Datos importados correctamente...'},
            len_col: '',
            parts: {},
            codecs: ['utf-8', 'latin1', 'ansi', 'ascii', 'iso-8859-1', 'cp1252'],
            lc_codec: 'utf-8',
            lc_prefijo: '',
            lc_destino: '',
            lc_error: 'strict',
            f_separator: ',',
            f_archivo: '',
            f_campos: '',
            f_head: '',
            f_rules: '',
            arr_campos: [],
            raw_rules: {},
            fileTarget: null,
            diccionario: null,
            status: 'ini',
            status_msn: '',
            state: {'INI': 'ini', 'UPLOADING': 'uploading', 'UPLOADED': 'uploaded', 'FAILED': 'failed'},
            slice_size: 10240,      // 1024 * 10,
            has_error_dict: false,
            first_line: [],
            first_line_raw: '',
            first_line_pass: false,
            tar_indice: -1,
            tar_rule: '',
            endchar: true,
            basedate: '',
            codigo: '',
            interval: null,
            importData: null,
        }
    },
    watch: {
        f_separator: function(val){
            this.setFirstLine();
        },
        tar_rule: function(val){
            this.first_line[this.tar_indice].rule = val;
        }
    },
    computed: {
        rule_disabled: function(){
            if(this.fileTarget == null || this.first_line_pass == false){
                return true;
            }else{
                if(this.extra){
                    return false;
                }else{
                    return (this.f_head == 'file_parse' && this.arr_campos.length != this.first_line.length);
                }
            }
        },
    },
    methods: {
        sumAnio: function(num){
            let tm = parseInt(this.f_anio) + num;
            this.f_anio = tm.toString();
            this.f_mes = '';
        },
        getPeriodo: function(){
            return (this.f_mes == '')? '': `${this.f_anio}${this.f_mes}`;
        },
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        setDestino: function(arg){
            this.lc_destino = arg;
        },
        clearImport: function(){
            this.fileTarget = null;
            this.f_archivo = '';
            this.step = 1;
            this.first_line = [];
            this.first_line_raw = '';
            this.first_line_pass = false;
            this.arr_campos.forEach(elm => elm.match = 0);
        },
        loadInfo: function(){
            this.has_error_dict = false;
            var ruta = root_path + 'users/admin/diccionario/' + this.lc_prefijo + this.lc_destino + '/';
            axios.get(ruta).then(res => {
                if(res.data.status == 'success'){
                    this.diccionario = res.data;
                    this.f_campos = this.diccionario.campos.split('|').map(elm => elm.split(':')[0]).join('|');
                    this.f_head = this.diccionario.type_head;
                    this.f_rules = this.diccionario.reglas;
                    this.f_rules.split('|').forEach(elm => {
                        let bi = elm.split(':');
                        this.raw_rules[bi[0]] = bi[1];
                    });
                    this.arr_campos = this.diccionario.campos.split('|').map(elm => {
                        let tm = elm.split(':');
                        let a = tm[0];
                        let b = (tm.length > 1)? tm[1]: a.toString();
                        let c = (tm.length > 2)? tm[2]: b.toString();
                        return {'field': a, 'head': b, 'human': c, 'rule': (this.raw_rules[a] == undefined)? 'Mixed': this.raw_rules[a], 'has': true, 'match': 0};
                    });
                    if(this.skipintro && this.f_head != '') this.step = 2;
                }else{
                    this.has_error_dict = true;
                }
            }).catch(err => {
                this.has_error_dict = true;
                console.log(err);
            });
        },
        setConfig: function(hd, cmps, rls){
            // auto | file_parse | file_fixed
            var tm = 'head:auto|campos:uno:Titulo'
            if(['auto', 'file_parse', 'file_fixed'].some(elm => elm == hd)){
                this.f_head = hd;
                if(this.fields != ''){
                    this.f_campos = cmps.split('|').map(elm => elm.split(':')[0]).join('|');
                    this.f_rules = this.rules;
                    this.rules.split('|').forEach(elm => {
                        let bi = elm.split(':');
                        this.raw_rules[bi[0]] = bi[1];
                    });
                    this.arr_campos = cmps.split('|').map(elm => {
                        let tm = elm.split(':');
                        let a = tm[0];
                        let b = (tm.length > 1)? tm[1]: a.toString();
                        let c = (tm.length > 2)? tm[2]: b.toString();
                        return {'field': a, 'head': b, 'human': c, 'rule': (this.raw_rules[a] == undefined)? 'Mixed': this.raw_rules[a], 'has': true, 'match': 0};
                    });
                    if(this.skipintro && this.f_head != '') this.step = 2;
                    this.has_error_dict = false;
                }else{
                    this.has_error_dict = true;
                }
            }else{
                this.has_error_dict = true;
            }
        },
        selectFile: function(evt){
            if(evt.target.files.length > 0){
                this.fileTarget = evt.target.files[0];
                this.f_archivo = this.fileTarget.name;
                this.readFirstLine();
            }else{
                this.fileTarget = null;
                this.f_archivo = '';
            }
        },
        clearFile: function(){
            document.getElementById('fl_file').value = "";
            this.fileTarget = null;
            this.f_archivo = '';
            this.first_line = [];
            this.first_line_raw = '';
            this.first_line_pass = false;
            this.arr_campos.forEach(elm => elm.match = 0);
            this.tar_indice = -1;
        },
        dispatchFocus: function(){
            document.getElementById('fl_file').click();
        },
        sendFileUpload: function(){
            let per = (this.withperiodo)? (this.getPeriodo() != ''): true;
            if(per == false){
                alert('Debe seleccionar el periodo de corte de la base de datos!');
            }else{
                if(this.fileTarget != null && this.first_line_pass){
                    let fdata = new FormData();
                    if(this.f_head == 'file_fixed'){
                        this.f_campos = this.first_line.map(elm => elm.head).join('|');
                        this.f_rules = this.first_line.filter(elm => elm.rule != 'Mixed').map(elm => elm.head + ':' + elm.rule).join('|');
                    }
                    if(this.withperiodo){
                        fdata.append('periodo', this.getPeriodo());
                    }
                    fdata.append('csrfmiddlewaretoken', token_root);
                    fdata.append('rawfile', this.fileTarget);
                    if(this.f_head == 'file_parse' && (this.first_line.length > this.arr_campos.length)){
                        let last = (this.first_line.length - this.arr_campos.length) * -1;
                        let ads = this.first_line.slice(last).join('|');
                        fdata.append('campos', this.f_campos + '|' + ads);
                    }else{
                        fdata.append('campos', this.f_campos);
                    }
                    fdata.append('reglas', this.f_rules);
                    fdata.append('type_head', this.f_head);
                    fdata.append('delimitador', this.f_separator);
                    fdata.append('coleccion', this.lc_prefijo + this.lc_destino);
                    fdata.append('codec', this.lc_codec);
                    fdata.append('merror', this.lc_error);
                    if(this.realtime){
                        this.makeCode();
                        fdata.append('codigo', this.codigo);
                    }else{
                        fdata.append('codigo', '');
                    }
                    this.status = this.state.UPLOADING;
                    this.step = 3;
                    this.status_msn = '';
                    console.log('Enviando archivo...');
                    let ruta = root_path + 'users/admin/basic/import';
                    let config = {
                        headers: {'content-type': 'multipart/form-data', 'cache': false, 'processData': false},
                        maxBodyLength: 10000000,
                        maxContentLength: 10000000,
                    };
                    axios.post(ruta, fdata, config).then(res => {
                        if(res.data.status == 'success'){
                            if(this.realtime == false){
                                this.status = this.state.UPLOADED;
                                this.$eventBus.$emit('import-success', this.lc_destino);
                            }
                        }else{
                            this.status_msn = res.data.msn;
                            this.status = this.state.FAILED;
                        }
                    }).catch(err => {
                        console.log(err);
                        if(this.realtime == false){
                            this.status = this.state.FAILED;
                        }
                    });
                    this.realtimeExe();
                }
            }
        },
        readFirstLine: function(){
            this.first_line_raw = '';
            this.first_line = [];
            let reader = new FileReader();
            reader.onload = e => {
                let text = reader.result;
                let tmp = text.split('\r\n', 1);
                if(tmp.length > 0){
                    this.first_line_raw = tmp[0];
                    this.setFirstLine();
                }
            };
            if(this.fileTarget.size > 524288){
                let bety = this.fileTarget.slice(0, 524288);
                reader.readAsText(bety);
            }else{
                reader.readAsText(this.fileTarget);
            }
        },
        setFirstLine: function(){
            this.endchar = true;
            if(this.first_line_raw != ''){
                if(this.f_head == 'file_fixed'){
                    this.first_line = this.first_line_raw.split(this.f_separator).map(elm => ({'head': elm, 'rule': 'Mixed'}));
                }else{
                    this.endchar = (this.first_line_raw.slice(-1) == this.f_separator)? false: true;
                    this.first_line = this.first_line_raw.split(this.f_separator);
                }
            }else{
                this.first_line = [];
            }
            this.isMatch();
        },
        isMatch: function(){
            this.arr_campos.forEach(elm => elm.match = 0);
            if(this.fileTarget != null){
                if(this.f_head != 'file_fixed'){
                    let bool = true;
                    for(var i = 0; i < this.arr_campos.length; i++){
                        let rule = new RegExp("^" + this.arr_campos[i].head + "$", 'i');
                        if(this.arr_campos[i].head == this.first_line[i]){
                            this.arr_campos[i].match = 1;
                        }else{
                            bool = false;
                            this.arr_campos[i].match = 2;
                        }
                    }
                    this.first_line_pass = this.endchar? bool: false;
                }else{
                    this.first_line_pass = (this.first_line.length == 1)? false: true;
                }
            }else{
                this.first_line_pass = false;
            }
        },
        openModal: function(indice, value){
            this.tar_indice = indice;
            this.tar_rule = value;
            $('#responsive-modal').modal('show');
        },
        markdate: function(){
            let fc = new Date();
            this.basedate = fc.getFullYear() + '_' + fc.getMonth() + '_' + fc.getDate() + '_';
        },
        makeCode: function(){
            this.codigo = this.basedate + [1, 2, 3, 4, 5].reduce((ac, elm) => ac += String.fromCharCode(Math.round(Math.random() * 25) + 65), '');
            return this.codigo;
        },
        realtimeExe: function(ini=false){
            if(this.realtime){
                this.importData = null;
                if(this.interval != null){
                    clearTimeout(this.interval);
                    this.interval = null;
                }
                if(ini){
                    this.realtimeLoad();
                }else{
                    this.interval = setTimeout(this.realtimeLoad, 4000);
                }
            }
        },
        realtimeLoad: function(){
            if(this.importData != null && this.importData.estado == 'close'){
                if(this.interval != null){
                    clearTimeout(this.interval);
                    this.interval = null;
                }
                this.status = this.state.UPLOADED;
                this.$eventBus.$emit('import-success', this.lc_destino);
            }else{
                let pam = new FormData();
                pam.append('codigo', this.codigo);
                axios.post(root_path + 'users/admin/codigo/import', pam).then(res => {
                    console.log('Realtime load!');
                    console.log(res.data);
                    this.importData = res.data;
                    if(this.importData.estado == 'close'){
                        if(this.interval != null){
                            clearTimeout(this.interval);
                            this.interval = null;
                        }
                        this.status = this.state.UPLOADED;
                        this.$eventBus.$emit('import-success', this.lc_destino);
                    }
                }).catch(err => {
                    console.log(err);
                });
            }
        },
        sendFirstChunk: function(){

        },
        readFile: function(){

        }
    },
    mounted() {
        let nx = 10;
        if(this.withperiodo){
            this.f_anio = (new Date()).getFullYear().toString();
        }
        if(this.separador_mode != 'hide') nx -= 2;
        if(this.codec_mode != 'hide') nx -= 2;
        this.len_col = 'col-sm-' + nx;
        this.lc_codec = this.codec;
        this.f_separator = this.separador;
        this.lc_prefijo = (this.destino == '' && this.prefijo == '')? 'tmp_': this.prefijo;
        this.lc_error = ['strict', 'ignore'].includes(this.error)? this.error: 'strict';
        this.setDestino(this.destino);
        if(this.sindiccionario){
            this.setConfig(this.head, this.fields, this.rules);
        }else{
            this.loadInfo();
        }
        this.markdate();
    }
}
</script>
<style scoped>
    .btn.df-white {background:#FFF}
    /* .btn.d-border {border:1px solid #999} */
    .control-label {text-transform: none !important}
    .txhover:hover {color:#2ECD99 !important; cursor:pointer}
    .opaco {opacity: .5}
    .classIni {border:4px dashed #EAEAEA; background:#FCFCFC}
    .classEnd {border:2px solid #EAEAEA; background:#FCFCFC}
    .emptyDestiny:hover {color:#ED6F56; cursor:pointer}
    .no-colection {user-select: none !important; pointer-events: none !important; opacity: .5 !important}
    .tx-capital {text-transform: lowercase}
    .tx-capital:first-letter {text-transform: uppercase}
    .table-import thead th {background:linear-gradient(#FAFAFA, #E7E7E7)}
    .table-import thead th.bg-danger {background:#ED6F56 !important; color:#FFF !important}
    .table-import thead th.bg-success {background:#2ECD99 !important; color:#FFF !important}
    .table-import th, .table-import td {padding: .5rem !important; border:1px solid #AAA !important; text-transform: none !important}
    .table-import tr.opaco th {border-color: #DDD !important}
    .table-import td {font-style:italic; cursor: default}
    .table-import td.on-fire:hover {background:#F0C54166; color:#000}
    .dk-click {cursor:pointer; user-select: none}
    /* table.table.table-import tr {border:1px solid #444} */
</style>