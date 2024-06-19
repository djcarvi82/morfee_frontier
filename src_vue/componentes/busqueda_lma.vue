<template>
    <div>
        <div class="row">
            <div class="col-md-12">
                <div class="panel panel-default card-view">
                    <div class="panel-heading" v-if="titulo != 'none'">
                        <h6 class="panel-title txt-dark">{{ titulo }}</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <!--<ul class="nav nav-pills">
                                <li :class="(criterio == 'ident')? 'active': ''" v-on:click="selectCriterio('ident')"><a href="#">Por identificación</a></li>
                                <li :class="(criterio == 'names')? 'active': ''" v-on:click="selectCriterio('names')"><a href="#">Por nombres y apellidos</a></li>
                            </ul>
                            <hr class="light-grey-hr mb-5" v-if="criterio != ''">-->
                            <div class="row mt-15" v-if="criterio == 'ident'">
                                <div class="col-md-3 col-sm-3">
                                    <div class="form-group">
                                        <label class="control-label">Tipo documento</label>
                                        <select class="form-control" name="tipodoc" v-model="t_doc" :disabled="ruta == ''">
                                            <option value=""></option>
                                            <option value="CC">CC - Cédula de Ciudadanía</option>
                                            <option value="TI">TI - Tarjeta de Identidad</option>
                                            <option value="RC">RC - Registro Civil</option>
                                            <option value="CE">CE - Cédula de Extranjería</option>
                                            <option value="PA">PA - Pasaporte</option>
                                            <option value="PE">PE - Per Especial Permanencia</option>
                                            <option value="AS">AS - Adulto sin identificación</option>
                                            <option value="MS">MS - Menor sin identificación</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label">Número de identificación</label>
                                        <div class="input-group">
                                            <input type="text" class="form-control" placeholder="Digite el número de identificación aquí" v-model="n_doc" :disabled="ruta == ''" v-on:keydown="filtro">
                                            <span class="input-group-btn">
                                                <button type="button" class="btn btn-success" v-on:click="loadData" :disabled="ruta == '' || isLoad">
                                                    <i class="fa fa-search"></i>
                                                </button>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row mt-15" v-else-if="criterio == 'names'">
                                <div class="col-md-10 col-sm-10">
                                    <div class="row">
                                        <div class="col-md-3 col-sm-3">
                                            <div class="form-group">
                                                <label class="control-label">Primer nombre</label>
                                                <input type="text" class="form-control" v-model="nom_1" :disabled="ruta == ''" v-on:keydown="filtro">
                                            </div>
                                        </div>
                                        <div class="col-md-3 col-sm-3">
                                            <div class="form-group">
                                                <label class="control-label">Segundo nombre</label>
                                                <input type="text" class="form-control" v-model="nom_2" :disabled="ruta == ''" v-on:keydown="filtro">
                                            </div>
                                        </div>
                                        <div class="col-md-3 col-sm-3">
                                            <div class="form-group">
                                                <label class="control-label">Primer apellido</label>
                                                <input type="text" class="form-control" v-model="ape_1" :disabled="ruta == ''" v-on:keydown="filtro">
                                            </div>
                                        </div>
                                        <div class="col-md-3 col-sm-3">
                                            <div class="form-group">
                                                <label class="control-label">Segundo apellido</label>
                                                <input type="text" class="form-control" v-model="ape_2" :disabled="ruta == ''" v-on:keydown="filtro">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-2 col-sm-2">
                                    <div class="form-group">
                                        <label for="" class="control-label">&nbsp;</label>
                                        <button class="btn btn-success btn-block" type="button" v-on:click="loadData" :disabled="ruta == '' || isLoad"><i class="fa fa-search"></i></button>
                                    </div>
                                </div>
                            </div>
                            <div class="alert alert-warning mt-15" v-if="salida != '' && !isLoad">
                                <i class="pull-left zmdi zmdi-alert-circle-o pr-15"></i>
                                <p class="pull-left">{{ salida }}</p>
                                <div class="clearfix"></div>
                            </div>
                        </div><!-- End panel body -->
                    </div>
                </div>
            </div>
        </div>
        <!-- SECTION RESULT -->
        <div class="row" v-if="!isLoad && giros.length > 0">
            <div class="col-sm-3 col-md-3">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <h6 class="panel-title txt-dark">DATOS BÁSICOS</h6>
                        </div>
                        <div class="pull-right">
                            <a href="#" class="pull-left inline-block full-screen">
                                <i class="zmdi zmdi-fullscreen"></i>
                            </a>
                        </div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div>
                                <span class="pull-left inline-block capitalize-font txt-dark">Primer nombre</span>
                                <span class="pull-right capitalize-font">{{ giros[0].nom_1 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Segundo nombre</span>
                                <span class="pull-right capitalize-font">{{ giros[0].nom_2 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Primer apellido</span>
                                <span class="pull-right capitalize-font">{{ giros[0].ape_1 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Segundo apellido</span>
                                <span class="pull-right capitalize-font">{{ giros[0].ape_2 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Tipo doc</span>
                                <span class="pull-right capitalize-font">{{ giros[0].t_doc }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Identificación</span>
                                <span class="pull-right capitalize-font">{{ giros[0].n_doc }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Fecha de nacimiento</span>
                                <span class="pull-right capitalize-font">{{ giros[0].f_nac }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Sexo</span>
                                <span class="pull-right capitalize-font">{{ giros[0].sexo }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Departamento</span>
                                <span class="pull-right capitalize-font">{{ showDepto(giros[0].dep) }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Municipio</span>
                                <span class="pull-right capitalize-font">{{ showMcpio(giros[0].mun, giros[0].dep) }}</span>
                                <div class="clearfix"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <contadore texto="TOTAL LIQUIDACIÓN" :valor="formatMiles(suma)" duracion="1" icono="icon-magnifier-add"></contadore>
            </div><!-- End col -->
            <div class="col-sm-9 col-md-9">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <h6 class="panel-title txt-dark">HISTÓRICO</h6>
                        </div>
                        <div class="pull-right">
                            <a href="#" class="pull-left inline-block full-screen">
                                <i class="zmdi zmdi-fullscreen"></i>
                            </a>
                        </div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="table-wrap">
                                <div class="table-responsive">
                                    <table class="table table-striped mb-0">
                                        <thead>
                                            <tr>
                                                <th class="text-center">No.</th>
                                                <th>Tipo</th>
                                                <th>Identificación</th>
                                                <th>Afiliación</th>
                                                <th>EPS</th>
                                                <th>Departamento</th>
                                                <th>Municipio</th>
                                                <th>Subsidio</th>
                                                <th>Fecha periodo</th>
                                                <th>Días</th>
                                                <th>Valor</th>
                                                <th>Periodo</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(gi, indice) in giros" :key="indice">
                                                <td class="text-center">{{ indice + 1 }}</td>
                                                <td>{{ gi.t_doc }}</td>
                                                <td>{{ gi.n_doc }}</td>
                                                <td>{{ gi.giros.f_afi }}</td>
                                                <td>{{ showEPS(gi.giros.eps) }}</td>
                                                <td>{{ showDepto(gi.dep) }}</td>
                                                <td>{{ showMcpio(gi.mun, gi.dep) }}</td>
                                                <td>{{ gi.giros.t_sub }}</td>
                                                <td>{{ gi.giros.f_per }}</td>
                                                <td>{{ gi.giros.dias }}</td>
                                                <td>{{ formatMiles(gi.giros.valor) }}</td>
                                                <td>{{ gi.giros.per }}</td>
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
    </div>
</template>
<script>
import Contador from './Contador.vue';

export default {
    components: {'contadore': Contador},
    props: {
        ruta: {type: String, default: ''},
        titulo: {type: String, default: 'none'}
    },
    data(){
        return {
            teclas: [8,9,13,37,39,46,109,189],
            op_reg: {'S': 'Subsidiado', 'C': 'Contributivo', 'E': 'Especial'},
            criterio: 'ident',   //  ident | names
            t_doc: '',
            n_doc: '',
            //bdua: '',
            nom_1: '',
            nom_2: '',
            ape_1: '',
            ape_2: '',
            identidad: '',
            tipo: '',
            bdua: '',
            giros: [],
            suma: 0,
            salida: '',
            isLoad: false,
        }
    },
    methods: {
        formatMiles: function(num){
            var regla = /(\d+)(\d{3})/;
            var tmp = String(num);
            while(regla.test(tmp)){
                tmp = tmp.replace(regla, '$1' + ',' + '$2');
            }
            return tmp;
        },
        getRuta: function(){
            var regla = /^\s*$/;
            var pares = [];
            var campos = (this.criterio == 'ident')? ['t_doc', 'n_doc']: ['nom_1', 'nom_2', 'ape_1', 'ape_2'];
            campos.forEach(elm => {
                if(!regla.test(this[elm])){
                    pares.push(elm + '=' + this[elm]);
                }
            });
            if(pares.length > 0){
                pares.push('criterio=' + this.criterio);
                return this.ruta + '?' + pares.join('&');
            }else{
                return 'void';
            }
        },
        loadData: function(){
            if(this.ruta != ''){
                this.salida = '';
                var path = this.getRuta();
                if(!this.isLoad){
                    if(path != 'void' && this.n_doc != ''){
                        this.isLoad = true;
                        axios.get(path).then(response => {
                            if(response.data == -1){
                                this.salida = 'No se pudo establecer conexión con la base de datos!';
                            }else{
                                this.suma = 0;
                                this.giros = response.data;
                                this.giros.forEach(elm => {
                                    this.suma += elm.giros.valor;
                                });
                                if(this.giros.length == 0){
                                    this.salida = 'No se encontraron resultados con los criterios de búsqueda seleccionados!';
                                }
                            }
                            this.isLoad = false;
                        }).catch(err => {console.log});
                    }else{
                        this.salida = (this.n_doc == '')? 'Ingrese el número de identificación del usuario!': 'Debe seleccionar al menos un filtro para realizar la búsqueda!';
                    }
                }
            }
        },
        showDepto: function(arg){
            return dane_get_depto(arg);
        },
        showMcpio: function(mcp, dep = ''){
            return dane_get_mcpio(dep + '' + mcp);
        },
        showEPS: function(codex){
            return dane_get_eps(codex);
        },
        selectCriterio: function(cri){
            this.criterio = (this.criterio == cri)? '': cri;
            //this.targetUser = null;
        },
        filtro: function(e){
            if(/^[A-Z0-9Ñ]$/i.test(e.key)){
                return true;
            }else if(this.teclas.indexOf(e.keyCode) >= 0){
                if(e.keyCode == 13){
                    this.loadData();
                }
                return true;
            }else{
                e.preventDefault();
                return false;
            }
        }
    },
    mounted(){
        //alert('Pastrana');
    }
}
</script>
<style scoped>
    .puntero {cursor: pointer !important}
    .is-hidden {display:none !important}
    .chat-body > a.is-active > .chat-data {background:linear-gradient(#FFF2CC,#FFE699) !important}
</style>