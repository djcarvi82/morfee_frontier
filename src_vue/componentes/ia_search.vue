<template>
    <div>
        <div class="row">
            <div class="col-sm-3">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <h5 class="panel-title txt-dark fs-5">FILTROS</h5>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div  class="panel-body">
                            <div class="pills-struct mb-4">
                                <ul class="nav nav-pills">
                                    <li :class="tagfilter == 'level'? 'active': ''"><a href="javascript:void(0)" @click="changeTag('level')">Niveles</a></li>
                                    <li :class="tagfilter == 'code'? 'active': 'd-none'"><a href="javascript:void(0)" @click="changeTag('code')">Código</a></li>
                                    <li :class="tagfilter == 'text'? 'active': ''"><a href="javascript:void(0)" @click="changeTag('text')">Texto</a></li>
                                </ul>
                            </div>
                            <div :class="tagfilter == 'level'? '': 'd-none'">
                                <div class="form-group">
                                    <label class="control-label">1 Dígito:</label>
                                    <select class="form-control" v-model="f_1">
                                        <option value=""></option>
                                        <option :value="cue" v-for="(cue, i) in cuentas" :key="i">{{ cue.cod + ' - ' + cue.den }}</option>
                                    </select>
                                </div>
                                <div class="form-group" v-if="niveles[2].activo">
                                    <label class="control-label">2 Dígitos: <i class="txt-primary" v-if="niveles[2].stt == state.LOADING">Cargando datos...</i></label>
                                    <select class="form-control" v-model="f_2" :disabled="niveles[2].data.length == 0 && f_1 == ''">
                                        <option value=""></option>
                                        <option :value="cue" v-for="(cue, i) in niveles[2].data" :key="i">{{ cue.cod + ' - ' + cue.den }}</option>
                                    </select>
                                </div>
                                <div class="form-group" v-if="niveles[3].activo">
                                    <label class="control-label">4 Dígitos: <i class="txt-primary" v-if="niveles[3].stt == state.LOADING">Cargando datos...</i></label>
                                    <select class="form-control" v-model="f_4" :disabled="niveles[3].data.length == 0 && f_2 == ''">
                                        <option value=""></option>
                                        <option :value="cue" v-for="(cue, i) in niveles[3].data" :key="i">{{ cue.cod + ' - ' + cue.den }}</option>
                                    </select>
                                </div>
                                <div class="form-group" v-if="niveles[4].activo">
                                    <label class="control-label">6 Dígitos: <i class="txt-primary" v-if="niveles[4].stt == state.LOADING">Cargando datos...</i></label>
                                    <select class="form-control" v-model="f_6" :disabled="niveles[4].data.length == 0 && f_4 == ''">
                                        <option value=""></option>
                                        <option :value="cue" v-for="(cue, i) in niveles[4].data" :key="i">{{ cue.cod + ' - ' + cue.den }}</option>
                                    </select>
                                </div>
                                <div class="btn btn-success btn-block" @click="changeNivel(1)" v-if="nivel == 1"><i class="fa fa-plus me-2"></i> Nivel</div>
                                <div class="row" v-else>
                                    <div class="col-sm-6">
                                        <div class="btn btn-danger btn-block" @click="changeNivel(-1)"><i class="fa fa-minus me-2"></i> Nivel</div>
                                    </div>
                                    <div class="col-sm-6">
                                        <div class="btn btn-success btn-block" @click="changeNivel(1)" :disabled="nivel == 4"><i class="fa fa-plus me-2"></i> Nivel</div>
                                    </div>
                                </div>
                            </div>
                            <div :class="tagfilter == 'code'? '': 'd-none'">

                            </div>
                            <div :class="tagfilter == 'text'? '': 'd-none'">
                                <div class="form-group">
                                    <label class="control-label" style="text-transform:none">Texto a buscar:</label>
                                    <div class="input-group">
                                        <input type="text" class="form-control" v-model.trim="f_texto">
                                        <span class="input-group-btn">
                                            <button class="btn btn-success" @click="loadResultText" :disabled="isEmpty(f_texto)">
                                                <i class="fa fa-search me-2"></i> Buscar
                                            </button>
                                        </span>
                                    </div>
                                    <span class="txt-primary">La búsqueda se realiza en códigos de 8 dígitos.</span>
                                    <div class="alert border border-warning bg-light-warning txt-dark mt-4" v-if="status == state.LOADED">
                                        <div class="d-flex align-items-center">
                                            <i class="fa fa-info-circle fs-3 me-2"></i>
                                            <span v-if="codigos.length == 0">No se encontraron cuentas de 8 dígitos con el texto <strong>{{ f_texto }}.</strong></span>
                                            <span v-else>Se encontraon <strong>{{ codigos.length }}</strong> códigos con el texto <strong>{{ f_texto }}.</strong></span>
                                        </div>
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
                        <h5 class="panel-title txt-dark fs-5" v-if="targetCuenta == null">{{ (tagfilter == 'text' && !isEmpty(f_texto) && status == state.LOADED)? 'RESULTADO CON EL TEXTO ' + f_texto: 'RESULTADO' }}</h5>
                        <h5 class="panel-title txt-dark fs-5" v-else>{{ targetCuenta.cod + ' - ' + targetCuenta.den }}</h5>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div  class="panel-body">
                            <div :class="((targetCuenta == null && tagfilter == 'level') || (tagfilter == 'text' && isEmpty(f_texto)))? 'd-none': ''">
                                <amchart-barra 
                                    ref="bary"
                                    altura="400"
                                    campo_categoria="eps" 
                                    campo_valor="suma" 
                                    multicolor
                                    rotar
                                    tooltip
                                    custom="{valueY}"
                                    ordenado
                                    cursor
                                    etiquetas>
                                </amchart-barra>
                            </div>
                            <div v-if="((targetCuenta == null && tagfilter == 'level') || (tagfilter == 'text' && isEmpty(f_texto)))" class="alert alert-warning">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-warning fs-4 me-3"></i>
                                    <span>Utilice los filtros para obtener los resultados esperados.</span>
                                </div>
                            </div>
                            <div class="border py-3 px-4" style="background:#FAFAFA">
                                <span @click="selectAll" :class="select_all? 'badge badge-success dk-click pt-2 pb-2 px-3': 'badge dk-click pt-2 pb-2 px-3'" style="font-size:.8rem; letter-spacing:1px">
                                    <i :class="select_all? 'fa fa-check-square': 'fa fa-square-o'"></i> <span>Seleccionar todo</span>
                                </span>
                                <div class="border-bottom mt-2 mb-3"></div>
                                <div class="row">
                                    <div class="col-sm-4" v-for="(elm, i) in eps_list" :key="i">
                                        <div class="form-group">
                                            <div class="checkbox checkbox-success">
                                                <input type="checkbox" :id="'kx_' + i" :checked="elm.check" @click="changeCheck(elm.eps, elm.check, i)">
                                                <label :for="'kx_' + i">{{ elm.eps }}</label>
                                            </div>
                                        </div>
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
export default {
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''},
        pathresult: {type: String, default: ''},
        pathsub: {type: String, default: ''},
    },
    data() {
        return {
            tagfilter: 'level', // level | text | code
            cuentas: [
                {'cod': '1', 'den': 'ACTIVOS'}, 
                {'cod': '2', 'den': 'PASIVOS'}, 
                {'cod': '3', 'den': 'PATRIMONIO'}, 
                {'cod': '4', 'den': 'INGRESOS'},
                {'cod': '5', 'den': 'GASTOS'},
                {'cod': '6', 'den': 'COSTOS DEL SISTEMA GENERAL DE SEGURIDAD SOCIAL EN SALUD'},
                {'cod': '8', 'den': 'CUENTAS DE ORDEN DEUDORAS'},
                {'cod': '9', 'den': 'CUENTAS DE ORDEN ACREEDORAS'},
            ],
            niveles: [
                {'tx': 'Filled', 'num': 0, 'activo': true},
                {'tx': 'Nivel 1', 'num': 1, 'activo': true},
                {'tx': 'Nivel 2', 'num': 2, 'activo': false, 'data': [], 'stt': 'ini'},
                {'tx': 'Nivel 3', 'num': 3, 'activo': false, 'data': [], 'stt': 'ini'},
                {'tx': 'Nivel 4', 'num': 4, 'activo': false, 'data': [], 'stt': 'ini'},
            ],
            nivel: 1,
            targetCuenta: null,
            f_1: '',
            f_2: '',
            f_4: '',
            f_6: '',
            f_texto: '',
			datos: [],
            eps_list: [],
            eps: {},
            codigos: [],
            select_all: true,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    watch: {
        f_1: function(val){
            this.niveles.forEach(elm => {
                if(elm.num > 1) elm.data = [];
            });
            if(this.nivel == 1){
                if(val != ''){
                    this.targetCuenta = val;
                    this.loadResult(val.cod);
                }
            }else if(this.niveles[2].activo){
                this.loadSubcuentas(val.cod, 2)
            }
        },
        f_2: function(val){
            this.niveles.forEach(elm => {
                if(elm.num > 2) elm.data = [];
            });
            if(this.nivel == 2){
                if(val != ''){
                    this.targetCuenta = val;
                    this.loadResult(val.cod);
                }
            }else if(this.niveles[3].activo){
                this.loadSubcuentas(val.cod, 3)
            }
        },
        f_4: function(val){
            this.niveles.forEach(elm => {
                if(elm.num > 3) elm.data = [];
            });
            if(this.nivel == 3){
                if(val != ''){
                    this.targetCuenta = val;
                    this.loadResult(val.cod);
                }
            }else if(this.niveles[4].activo){
                this.loadSubcuentas(val.cod, 4)
            }
        },
        f_6: function(val){
            this.niveles.forEach(elm => {
                if(elm.num > 4) elm.data = [];
            });
            if(this.nivel == 4){
                if(val != ''){
                    this.targetCuenta = val;
                    this.loadResult(val.cod);
                }
            // }else if(this.niveles[3].activo){
            //     this.loadSubcuentas(val.cod, 3)
            }
        },
    },
    methods: {
        selectAll: function(){
            this.select_all = !this.select_all;
            this.eps_list.forEach(elm => {
                elm.check = this.select_all;
                this.eps[elm.eps] = this.select_all;
            });
            // this.$refs.bary.setDatos(this.datos.filter(elm => this.eps[elm.eps] === true));
            this.$refs.bary.setDatos(this.getDatos());
        },
        changeNivel: function(num){
            if(num === 1){
                if(this.nivel < 4){
                    this.nivel++;
                    this.niveles[this.nivel].activo = true;
                    this.niveles[this.nivel].stt = 'ini';
                }
            }else{
                if(this.nivel > 1){
                    this.niveles[this.nivel].activo = false;
                    this.niveles[this.nivel].stt = 'ini';
                    this.nivel--;
                }
            }
            this.f_1 = '';
            this.f_2 = '';
            this.f_4 = '';
            this.f_6 = '';
            this.targetCuenta = null;
            this.$refs.bary.setDatos([]);
        },
        changeCheck: function(tx, bool, pos){
            let neg = !bool;
            this.eps[tx] = neg;
            this.eps_list[pos].check = neg;
            this.$refs.bary.setDatos(this.getDatos());
            // this.$refs.bary.setDatos(this.datos.filter(elm => this.eps[elm.eps] === true));
        },
        changeTag: function(arg){
            if(this.status != this.state.LOADING){
                this.f_1 = '';
                this.f_2 = '';
                this.f_4 = '';
                this.f_6 = '';
                this.f_texto = '';
                this.targetCuenta = null;
                this.datos = [];
                this.codigos = [];
                this.$refs.bary.setDatos([]);
                this.status = this.state.INI;
                this.tagfilter = arg;
            }
        },
        getDatos: function(){
            let tmp = {};
            let num = 0;
            this.eps_list.filter(elm => elm.check).forEach(elm => {
                tmp[elm.eps] = {'eps': elm.eps, 'suma': 0};
                num++;
            });
            this.datos.forEach(elm => {
                if(this.eps[elm.eps] === true){
                    tmp[elm.eps]['suma'] = elm.suma;
                }
            });
            this.select_all = (this.eps_list.length == num)? true: false;
            return Object.values(tmp);
            // return this.datos.filter(elm => (this.eps[elm.eps] === true));
        },
        isEmpty: function(arg){
            if(['', undefined, null].includes(arg)) return true;
            return /^\s*$/.test(arg);
        },
        loadEPS: function(){
            axios.post(this.pathdata).then(res => {
                res.data.forEach(elm => this.eps[elm._id] = true);
                this.eps_list = Object.entries(this.eps).map(par => ( {'eps': par[0], 'check': par[1]} ));
            }).catch(err => {console.log(err)});
        },
        loadResult: function(cod){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('codigo', cod);
                this.status = this.state.LOADING;
                axios.post(this.pathresult, pam).then(res => {
                    this.datos = res.data.map(elm => {
                        return {'eps': elm._id.n_eps, 'suma': elm.suma};
                    });
                    this.$refs.bary.setDatos(this.getDatos());
                    this.status = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        loadResultText: function(){
            let pam = new FormData();
            pam.append('texto', this.f_texto);
            this.status = this.state.LOADING;
            axios.post(this.pathresult + '/texto', pam).then(res => {
                console.log(res.data);
                this.codigos = res.data[0].codigos;
                this.datos = res.data[0].datos.map(elm => {
                    return {'eps': elm._id, 'suma': elm.suma};
                });
                console.log('CÓDIGOS ENCONTRADOS');
                console.log(this.codigos);
                this.$refs.bary.setDatos(this.getDatos());
                this.status = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status = this.state.FAILED;
            });
        },
        loadSubcuentas: function(cod, level){
            if(!this.isEmpty(cod)){
                let pam = new FormData();
                pam.append('codigo', cod);
                this.niveles[level].stt = this.state.LOADING;
                axios.post(this.pathsub, pam).then(res => {
                    this.niveles[level].data = res.data[0].cuentas.map(elm => ( {'cod': elm.cod, 'den': elm.den} ));
                    this.niveles[level].stt = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.niveles[level].stt = this.state.FAILED;
                });
            }
        }
    },
    mounted() {
        this.loadEPS();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .dk-click {user-select: none; cursor: pointer}
    .btn-custom {background:#DEDEDE; color:#878787}
    .btn-custom:hover {background: #F2F2F2; color:#212128}
</style>