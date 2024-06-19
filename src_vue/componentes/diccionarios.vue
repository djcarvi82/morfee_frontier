<template>
    <div>
        <div class="row" v-if="diccionario != null">
            <div class="col-sm-4">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <h6 class="panel-title txt-dark">INFORMACIÓN GENERAL</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row">
                            <div class="d-flex justify-content-between px-3 py-3 border-bottom">
                                <div><i class="zmdi zmdi-chevron-right me-2 font-16"></i><span>Base de datos</span></div>
                                <div class="txt-primary t-bolder">{{ diccionario.alias }}</div>
                            </div>
                            <div class="d-flex justify-content-between px-3 py-3 border-bottom">
                                <div><i class="zmdi zmdi-chevron-right me-2 font-16"></i><span>Módulo</span></div>
                                <div class="txt-dark weight-500">{{ modic[diccionario.modulo] }}</div>
                            </div>
                            <div class="d-flex justify-content-between px-3 py-3 border-bottom">
                                <div><i class="zmdi zmdi-chevron-right me-2 font-16"></i><span>Cliente</span></div>
                                <div class="txt-dark weight-500">{{ txcliente(diccionario.cliente_id) }}</div>
                            </div>
                            <div class="d-flex justify-content-between px-3 py-3">
                                <div><i class="zmdi zmdi-chevron-right me-2 font-16"></i><span>Colección o tabla</span></div>
                                <div class="txt-dark weight-500">{{ diccionario.coleccion }}</div>
                            </div>
                            <div class="px-3 mt-3">
                                <button type="button" class="btn btn-success btn-anim btn-block" v-on:click="diccionario = null">
                                    <i class="fa fa-long-arrow-left"></i>
                                    <span class="btn-text">Atrás</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div><!-- END PANEL -->
            </div>
            <div class="col-sm-8">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <h6 class="panel-title txt-dark">CONFIGURACIÓN DE CAMPOS</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th class="colmin">No.</th>
                                        <th>Nombre en la colección</th>
                                        <th>Nombre para mostrar</th>
                                        <th>Nombre en cabeceara de archivo</th>
                                        <th class="colmin px-5">Acción</th>
                                    </tr>
                                </thead>
                                <tbody class="lc-compact">
                                    <tr v-for="(cam, i) in campos" :key="i" :class="((indice >= 0 && indice != i) || indice == -2)? 'tr-metal': 'tr-transmetal'">
                                        <td class="text-center">{{ i + 1 }}</td>
                                        <td>
                                            <div v-if="indice == i">
                                                <input type="text" class="form-control" v-model="f_name">
                                            </div>
                                            <div v-else>
                                                {{ cam.name }}
                                            </div>
                                        </td>
                                        <td>
                                            <div v-if="indice == i">
                                                <input type="text" class="form-control" v-model="f_display">
                                            </div>
                                            <div v-else>
                                                <span v-if="cam.display == ''" class="text-custom">{{ cam.head }}</span>
                                                <span v-else>{{ cam.display }}</span>
                                            </div>
                                        </td>
                                        <td>
                                            <div v-if="indice == i">
                                                <input type="text" class="form-control" v-model="f_head">
                                            </div>
                                            <div v-else>
                                                {{ cam.head }}
                                            </div>
                                        </td>
                                        <td class="text-center">
                                            <div v-if="indice == i">
                                                <a href="javascript:void(0)" title="Aceptar" class="txt-dark hov-success" v-on:click="changeField()"><i class="fa fa-check"></i></a>
                                                <a href="javascript:void(0)" title="Cancelar" class="txt-dark hov-danger mx-3" v-on:click="selectRowEdit(-1)"><i class="fa fa-times"></i></a>
                                                <a href="javascript:void(0)" title="Eliminar" class="txt-dark hov-danger" v-on:click="removeField()"><i class="fa fa-trash"></i></a>
                                            </div>
                                            <div v-else>
                                                <a href="javascript:void(0)" title="Editar" v-on:click="selectRowEdit(i)"><i class="fa fa-pencil hov-success"></i></a>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr class="tr-biometal" v-if="indice == -2">
                                        <td class="text-center">{{ campos.length + 1 }}</td>
                                        <td><input type="text" class="form-control" v-model="f_name"></td>
                                        <td><input type="text" class="form-control" v-model="f_display"></td>
                                        <td><input type="text" class="form-control" v-model="f_head"></td>
                                        <td class="text-center">
                                            <a href="javascript:void(0)" title="Aceptar" class="txt-dark hov-success" v-on:click="addField()"><i class="fa fa-check"></i></a>
                                            <a href="javascript:void(0)" title="Cancelar" class="txt-dark hov-danger ms-3" v-on:click="selectRowEdit(-1)"><i class="fa fa-times"></i></a>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="px-3">
                                <div class="d-flex justify-content-between">
                                    <button type="button" class="btn btn-success btn-anim" v-on:click="selectRowEdit(-2)" :disabled="indice >= 0 || indice == -2">
                                        <i class="fa fa-plus"></i> 
                                        <span class="btn-text">Agregar campo</span>
                                    </button>
                                    <button type="button" class="btn btn-success btn-anim" v-on:click="saveFields" :disabled="indice != -1 || diccionario.campos == campos_pretend">
                                        <i class="fa fa-save"></i>
                                        <span class="btn-text">Guardar cambios</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!-- END PANEL -->
            </div>
        </div>
        <div class="panel panel-default card-view border" v-else>
            <div class="panel-heading">
                <h6 class="panel-title fs-5">BASES DE DATOS</h6>
            </div>
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <div class="row mb-4">
                        <div class="col-sm-4">
                            <div class="form-group">
                                <label class="control-label">Módulo:</label>
                                <select class="form-control" v-model="f_modulo">
                                    <option value=""></option>
                                    <option :value="mod.clave" v-for="mod in modulos" :key="mod.id">{{ mod.modulo }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-sm-4">
                            <div class="form-group">
                                <label class="control-label">Cliente:</label>
                                <select class="form-control" v-model="f_cliente_id">
                                    <option value=""></option>
                                    <option value="-none-">- PLANTILLAS MORFEE -</option>
                                    <option :value="cli.id" v-for="cli in clientes" :key="cli.id">{{ cli.cliente }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <div class="form-group">
                                <label class="control-label">&nbsp; </label>
                                <button type="button" class="btn btn-success btn-block" disabled v-if="f_cliente_id == '' || f_modulo == ''">
                                    <span class="btn-text">Buscar</span>
                                </button>
                                <button type="button" class="btn btn-success btn-anim btn-block" v-on:click="loadCollections" v-else>
                                    <i class="fa fa-search"></i>
                                    <span class="btn-text">Buscar</span>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="alert alert-warning" v-if="status == state.INI">
                        <div class="d-flex">
                            <i class="zmdi zmdi-alert-circle-o me-2"></i>
                            <p>Seleccione el módulo y cliente para verificar las bases de datos disponibles!</p>
                        </div>
                    </div>
                    <div v-else-if="status == state.LOADING" class="d-flex">
                        <i class="fa fa-spinner fa-spin"></i>
                        <p>Cargando información...</p>
                    </div>
                    <div v-else-if="status == state.LOADED && diccionarios.length == 0">
                        <div class="alert alert-danger">
                            <div class="d-flex">
                                <i class="zmdi zmdi-alert-triangle me-2"></i>
                                <p>No tiene bases de datos configuradas!</p>
                            </div>
                        </div>
                    </div>
                    <div class="table-wrap" v-if="status == state.LOADED && diccionarios.length > 0">
                        <div class="table-responsive">
                            <table class="table table-bordered table-striped">
                                <thead>
                                    <tr>
                                        <th class="colmin">No.</th>
                                        <th>Base de datos</th>
                                        <th>Nombre de la colección</th>
                                        <th>Módulo</th>
                                        <th>Cliente</th>
                                        <th class="colmin px-5">Acción</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(dic, i) in diccionarios" :key="i">
                                        <td class="text-center">{{ i + 1 }}</td>
                                        <td>{{ dic.alias }}</td>
                                        <td>{{ dic.coleccion }}</td>
                                        <td>{{ modic[dic.modulo] }}</td>
                                        <td>{{ txcliente(dic.cliente_id) }}</td>
                                        <td class="text-center">
                                            <a href="javascript:void(0)" title="Editar" v-on:click="loadOneCollection(dic.id)" class="hov-success"><i class="fa fa-pencil"></i></a>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div><!-- END FIRST SECTION -->
    </div>
</template>
<script>
export default {
    data() {
        return {
            clientes: [],
            modulos: [],
            modic: {},
            clidic: {},
            f_cliente_id: '',
            f_modulo: '',
            f_name: '',
            f_display: '',
            f_head: '',
            diccionarios: [],
            diccionario: null,
            campos: [],
            indice: -1,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            statusDic: {'status': 'init', 'field': 'none'},
        }
    },
    watch: {
        f_name: function(val){
            this.f_name = val.replace(/\s+/g, '');
        },
        f_head: function(val){
            this.f_head = val.replace(/\s+/g, '');
        },
    },
    computed: {
        campos_pretend: function(){
            return this.campos.map(elm => {
                var aux = [elm.name, elm.head];
                if(elm.display != '' && elm.display != elm.head){
                    aux.push(elm.display);
                }
                return aux.join(':');
            }).join('|');
        }
    },
    methods: {
        loadPredata: function(){
            axios.post(root_path + 'diccionario/build').then(res => {
                this.clientes = res.data.result.clientes;
                this.clientes.forEach(elm => this.clidic[elm.id] = elm.cliente);
                this.modulos = res.data.result.modulos;
                this.modulos.forEach(elm => this.modic[elm.clave] = elm.modulo);
            }).catch(err => {console.log(err)});
        },
        loadCollections: function(){
            if(this.f_modulo != '' && this.f_cliente_id != ''){
                var params = new FormData();
                params.append('modulo', this.f_modulo);
                if(this.f_cliente_id != '-none-') params.append('cliente_id', this.f_cliente_id);
                this.status = this.state.LOADING;
                axios.post(root_path + 'diccionario/collections', params).then(res => {
                    this.diccionarios = res.data;
                    this.status = this.state.LOADED;
                    this.$nextTick(() => {
                        $('[data-toggle="tooltip"]').tooltip();
                    });
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        loadOneCollection: function(id){
            this.indice = -1;
            var params = new FormData();
            params.append('id', id)
            axios.post(root_path + 'diccionario/collection', params).then(res => {
                this.diccionario = res.data;
                this.campos = res.data.campos.split('|').map(elm => {
                    var tm = elm.split(':');
                    if(tm.length > 2){
                        return {'name': tm[0], 'head': tm[1], 'display': tm[2]};
                    }else if(tm.length == 2){
                        return {'name': tm[0], 'head': tm[1], 'display': ''};
                    }
                });
            }).catch(err => {console.log(err)});
        },
        txcliente: function(ref){
            return (ref == null)? '- PLANTILLAS MORFEE -': this.clidic[ref];
        },
        isEmpty: function(a){
            return (a == undefined || a == null || /^(\s*|[-\s]+)$/.test(a))? true: false;
        },
        selectRowEdit: function(ind){
            this.indice = ind;
            if(ind >= 0){
                this.f_name = this.campos[this.indice].name;
                this.f_display = this.campos[this.indice].display;
                this.f_head = this.campos[this.indice].head;            
            }else{
                this.f_name = '';
                this.f_display = '';
                this.f_head = '';
            }
        },
        changeField: function(){
            this.campos[this.indice].name = this.f_name;
            this.campos[this.indice].display = this.f_display.replace(/(^\s+|\s+$)/g, '').replace(/\s{2,}/g, ' ');
            this.campos[this.indice].head = this.f_head;
            this.indice = -1;
        },
        removeField: function(){
            this.campos.splice(this.indice, 1);
            this.indice = -1;
        },
        addField: function(){
            this.campos.push({
                'name': this.f_name,
                'head': this.f_head,
                'display': this.f_display
            });
            this.selectRowEdit(-1);
        },
        saveFields: function(){
            if(this.diccionario.campos != this.campos_pretend){
                this.updateField('campos', this.campos_pretend);
            }
        },
        updateField: function(field, value, acceptEmpty=true){
            var verify = acceptEmpty? true: !this.isEmpty(value);
            if(this.diccionario != null && this.statusDic.status != 'loading' && verify){
                var params = new FormData();
                params.append('dic_id', this.diccionario.id);
                params.append('fieldname', field)
                params.append('fieldvalue', value);
                this.statusDic = {'status': 'loading', 'field': field},
                axios.post(root_path + 'diccionario/update', params).then(res => {
                    alert('Listo');
                    console.log(res.data);
                    if(res.data.status == 'success'){
                        this.statusDic.status = this.state.LOADED;
                    }else{
                        this.statusDic.status = this.state.FAILED;
                    }
                }).catch(err => {console.log(err)});
            }
        }
    },
    mounted() {
        this.loadPredata();
    }
}
</script>
<style scoped>
.colmin {width:1%; white-space: nowrap; text-align: center}
.t-bold {font-weight: bold}
.t-bolder {font-weight: bolder}
.lc-compact td {padding-top:.5rem; padding-bottom: .45rem}
.text-custom {color:#CCC}
.tr-metal {opacity: .3; user-select: none; pointer-events: none}
.tr-metal + .tr-transmetal, .tr-biometal {background: #F4F4F4}
.tr-biometal {border-bottom: 1px solid #DEDEDE}
</style>