<template>
    <div>
        <div class="row">
            <div class="col-md-11 col-sm-11">
                <div class="row">
                    <div class="col-md-3 col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Departamento: Návaro Rusia</label>
                            <select class="form-control" v-model="f_depto">
                                <option value="">Todos...</option>
                                <option v-for="(dp, i) in getDeptos()" :key="i" :value="i">{{ dp }}</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-2 col-sm-2">
                        <div class="form-group">
                            <label for="" class="control-label">Municipio:</label>
                            <select class="form-control" v-model="f_mcpio">
                                <option value="">Todos...</option>
                                <option v-for="(mcp, mi) in munches" :key="mi" :value="mcp.cod">{{ mcp.tx }}</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-2 col-sm-2">
                        <div class="form-group">
                            <label for="" class="control-label">EPS:</label>
                            <select class="form-control" v-model="f_eps">
                                <option value="">Todas...</option>
                                <option v-for="(item, ei) in epsdata" :key="ei" :value="item.cod">{{ item.tx }} <span>({{ item.cod }})</span></option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-2 col-sm-2">
                        <div class="form-group">
                            <label for="" class="control-label">Estado:</label>
                            <select class="form-control" v-model="f_state">
                                <option value="">Todos...</option>
                                <option value="0">Sin vacunar</option>
                                <option value="1">Solo 1ra dosis</option>
                                <option value="2">2da dosis</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-3 col-sm-3">
                        <div class="form-group">
                            <label for="" class="control-label">Edad:</label>
                            <select class="form-control" v-model="f_edad">
                                <option value="">Todos...</option>
                                <option :value="item.a" v-for="(item, i) in buildRange()" :key="i">{{ item.b }}</option>
                            </select>
                            <div class="radio-list">
                                <div class="radio-inline pl-0">
                                    <span class="radio radio-success">
                                        <input type="radio" id="radio_9" value="mayores" v-model="tipoEdad"><label for="radio_9">Mayores</label>
                                    </span>
                                </div>
                                <div class="radio-inline pl-0">
                                    <span class="radio radio-success">
                                        <input type="radio" id="radio_10" value="rango" v-model="tipoEdad"><label for="radio_10">Rango</label>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-1 col-sm-1">
                <div class="form-group">
                    <label for="" class="control-label">&nbsp;</label>
                    <button class="btn btn-success btn-block" type="button" v-on:click="loadData()"><i class="fa fa-search"></i></button>
                </div>
            </div>
        </div>
        <hr class="light-grey-hr">
        <my-pagination ref="spage"></my-pagination>
        <div class="table-wrap">
            <div class="table-responsive">
                <table class="table table-bordered table-striped mt-10 mb-10">
                    <thead>
                        <tr>
                            <th>No.</th>
                            <th>Departamento</th>
                            <th>Municipio</th>
                            <th>Residencia</th>
                            <th>TD</th>
                            <th>NDOC</th>
                            <th>Nombre de Usuario</th>
                            <th>Sexo</th>
                            <th>Edad</th>
                            <th>EPS</th>
                            <th>Régimen</th>
                            <th>1ra dosis</th>
                            <th>Fecha 1ra dosis</th>
                            <th>2da dosis</th>
                            <th>Fecha 2da dosis</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, key) in registros" :key="key">
                            <td>{{ showNo(key) }}</td>
                            <td>{{ showDepto(item.dep) }}</td>
                            <td>{{ showMcpio(item.mun, item.dep) }}</td>
                            <td>{{ showMcpio(item.mun_res, item.dep_res) + ' - ' + showDepto(item.dep_res) }}</td>
                            <td>{{ item.t_doc }}</td>
                            <td>{{ item.n_doc }}</td>
                            <td>{{ showFullname(item.nom_1, item.nom_2, item.ape_1, item.ape_2)}}</td>
                            <td>{{ item.sexo }}</td>
                            <td>{{ item.edad }}</td>
                            <td>{{ showEPS(item.cod_EPS) }}</td>
                            <td>{{ showRegimen(item.regimen) }}</td>
                            <td class="dosis">{{ showDosisOne(item.paiweb, 'biol') }}</td>
                            <td class="dosis">{{ showDosisOne(item.paiweb, 'f_apli') }}</td>
                            <td class="dosis">{{ showDosisTwo(item.paiweb, 'biol') }}</td>
                            <td class="dosis">{{ showDosisTwo(item.paiweb, 'f_apli') }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
<script>
import Paginator from './paginacion.vue';

export default {
    components: {'my-pagination': Paginator},
    props: {
        url_main: {type: String, default: 'none'},
        url_count: {type: String, default: 'none'},
        departamento: {type: String, default: 'none'}
    },
    data(){
        return {
            teclas: [8,9,13,37,39,46,109,189],
            op_reg: {'S': 'Subsidiado', 'C': 'Contributivo', 'E': 'Especial'},
            page: 1,
            cantidad: 0,
            registros: [],
            munches: [],
            epsdata: [],
            tipoEdad: 'rango',
            f_depto: '',
            f_mcpio: '',
            f_eps: '',
            f_state: '',
            f_edad: '',
            f_from: '',
            f_to: '',
            validation: {'page': 'page', 'dep': 'f_depto', 'mun': 'f_mcpio', 'estado': 'f_state', 'from': 'f_from', 'to': 'f_to', 'eps': 'f_eps'},
            params: {'page': '', 'dep': '', 'mun': '', 'estado': '', 'from': '', 'to': '', 'eps': ''},
            last_params: {'page': '', 'dep': 'void', 'mun': 'void', 'estado': 'void', 'from': 'void', 'to': 'void', 'eps': 'void'},
            chainget: '',
            isLoad: false,
        }
    },
    watch: {
        f_edad: function(val){
            if(val == ''){
                this.f_from = '';
                this.f_to = '';
            }else if(this.tipoEdad == 'mayores'){
                this.f_from = val;
                this.f_to = '';
            }else{
                var par = val.split(':');
                this.f_from = par[0];
                this.f_to = (par[1] == '...')? '': par[1];
            }
        },
        f_depto: function(val){
            this.fillMcpios();
        },
        tipoEdad: function(val){
            this.f_edad = '';
        },
    },
    methods: {
        buildRange: function(){
            var tmp = [];
            if(this.tipoEdad == 'mayores'){
                for(var i = 10; i < 100; i++){
                    tmp.push({a:i, b:i + ' o más años'});
                }
            }else{
                tmp = [
                    {a:'0:39', b:'Entre 0 y 39 años'}, 
                    {a:'40:44', b:'Entre 40 y 44 años'}, 
                    {a:'45:49', b:'Entre 45 y 49 años'}, 
                    {a:'50:54', b:'Entre 50 y 54 años'}, 
                    {a:'55:59', b:'Entre 55 y 59 años'}, 
                    {a:'60:64', b:'Entre 60 y 64 años'}, 
                    {a:'65:69', b:'Entre 65 y 69 años'}, 
                    {a:'70:74', b:'Entre 70 y 74 años'}, 
                    {a:'75:79', b:'Entre 75 y 79 años'}, 
                    {a:'80:...', b:'Mayores de 80 años'}
                ];
            }
            return tmp;
        },
        buildURL: function(){
            var pares = [];
            for(var i in this.validation){
                this.params[i] = this[this.validation[i]];
                if(this.params[i] != ''){
                    pares.push(i + '=' + this.params[i]);
                }
            }
            this.chainget = pares.join('&');
            return this.url_main + '?' + this.chainget;
        },
        loadData: function(){
            var ruta = this.buildURL();
            axios.get(ruta).then(response => {
                this.loadDataCount();
                this.setRegistros(response.data);
            }).catch(err => {console.log(err)});
        },
        loadDataCount: function(){
            var isChange = false;
            ['dep', 'mun', 'estado', 'from', 'to', 'eps'].forEach(elm => {
                if(this.params[elm] != this.last_params[elm]){
                    this.last_params[elm] = this.params[elm];
                    isChange = true;
                }
            });
            if(isChange){
                axios.get(this.url_count + '?' + this.chainget).then(response => {
                    this.$refs.spage.setTotal(response.data);
                }).catch(err => {console.log(err)});
            }else{
                console.log('no change');
            }
        },
        setRegistros: function(arg){
            this.registros = arg;
        },
        showNo: function(itera){
            return itera + 1 + ((this.page - 1) * 50);
        },
        showDepto: function(arg){
            return dane_get_depto(arg);
        },
        showMcpio: function(mcp, dep = ''){
            return dane_get_mcpio(dep + '' + mcp);
        },
        showFullname: function(a, b, c, d){
            return a + ' ' + b + ' ' + c + ' ' + d;
        },
        showRegimen: function(arg){
            var tm = this.op_reg[arg];
            return (tm == undefined)? '--': tm;
        },
        showDosisOne: function(pai, out){
            return (pai.length > 0)? pai[0][out]: '';
        },
        showDosisTwo: function(pai, out){
            return (pai.length > 1)? pai[1][out]: '';
        },
        showEPS: function(codex){
            return dane_get_eps(codex);
        },
        getDeptos: function(){
            return divipola_dps;
        },
        fillMcpios: function(){
            this.f_mcpio = '';
            this.munches = []
            if(this.f_depto != ''){
                Object.entries(divipola[this.f_depto].mps).forEach(elm => {
                    this.munches.push({'cod': elm[0].slice(-3), 'tx': elm[1]})
                });
            }
        },
        fillEPS: function(){
            for(var i in col_eps){
                this.epsdata.push({'cod': i, 'tx': col_eps[i]});
            }
        },
        filtro: function(e){
            if(/^[A-Z0-9Ñ]$/i.test(e.key)){
                return true;
            }else if(this.teclas.indexOf(e.keyCode) >= 0){
                return true;
            }else{
                e.preventDefault();
                return false;
            }
        },
        listen: function(){
            this.$eventBus.$on('mf-select-page', currentPage => {
                this.page = currentPage;
                this.loadData();
            });
        }
    },
    mounted(){
        if(this.departamento != 'none') this.f_depto = this.departamento;
        this.loadData();
        this.listen();
        this.fillEPS();
    }
}
</script>
<style scoped>
    td.dosis {background:#2ECD99 !important; color:#FFF; text-align: center}
    td.dosis:not(:last-child) {border-right-color:#FFF !important}
    td.dosis:empty {background:#F9CCC2 !important}
    td.dosis:empty::before {content:'--'}
    input[type="radio"]:checked + label {color:#2ECD99 !important}
    select.form-control > option > span {font-size:.85rem !important; color:blue !important}
</style>