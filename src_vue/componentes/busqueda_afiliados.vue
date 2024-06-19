<template>
    <div>
        <div class="row">
            <div class="col-md-12">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <h6 class="panel-title txt-dark">FILTROS DE CONSULTA</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <ul class="nav nav-pills">
                                <li :class="(criterio == 'ident')? 'active': ''" v-on:click="selectCriterio('ident')"><a href="#">Por identificación</a></li>
                                <li :class="(criterio == 'names')? 'active': ''" v-on:click="selectCriterio('names')"><a href="#">Por nombres y apellidos</a></li>
                            </ul>
                            <hr class="light-grey-hr mb-5" v-if="criterio != ''">
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
        <div class="panel panel-default card-view" v-if="!isLoad && targetUser == null && usuarios.length > 0">
            <div class="panel-heading">
                <div class="pull-left">
                    <h6 class="panel-title txt-dark">RESULTADO DE LA CONSULTA</h6>
                </div>
                <div class="pull-right">
                    <a href="#" class="pull-left inline-block full-screen">
                        <i class="zmdi zmdi-fullscreen"></i>
                    </a>
                </div>
                <div class="clearfix"></div>
            </div>
            <div class="panel-wrapper collapse in">
                <div class="panel-body row pa-0">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Departamento</th>
                                        <th>Municipio</th>
                                        <th>Primer nombre</th>
                                        <th>Segundo nombre</th>
                                        <th>Primer apellido</th>
                                        <th>Segundo apellido</th>
                                        <th>Tipo doc</th>
                                        <th>Identificación</th>
                                        <th>Edad</th>
                                        <th>BDUA</th>
                                        <th>EPS</th>
                                        <th class="text-center">Acción</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(user, iu) in usuarios.slice(0, 10)" :key="iu">
                                        <td>{{ showDepto(user.dep) }}</td>
                                        <td>{{ showMcpio(user.mun, user.dep) }}</td>
                                        <td>{{ user.nom_1 }}</td>
                                        <td>{{ user.nom_2 }}</td>
                                        <td>{{ user.ape_1 }}</td>
                                        <td>{{ user.ape_2 }}</td>
                                        <td>{{ user.t_doc }}</td>
                                        <td>{{ user.n_doc }}</td>
                                        <td>{{ user.edad }}</td>
                                        <td>{{ user.s_BDUA }}</td>
                                        <td>{{ user.cod_EPS }}</td>
                                        <td class="text-center"><span class="label label-success puntero" v-on:click="selectUser(user)">Seleccionar</span></td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="alert alert-warning ma-10" v-if="usuarios.length > 10">
                                <div class="d-flex align-items-center">
                                    <i class="zmdi zmdi-alert-circle-o fs-1 pr-15"></i>
                                    <p style="line-height:1rem">Esta es una interfaz de búsqueda individualizada, y se encontraron más de 10 usuarios con los criterios de búsqueda utilizados, por lo tanto, le sugiero utilizar mejores filtros para encontrar el usuario que está buscando.</p>
                                </div>
                                <div class="clearfix"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="row" v-else-if="!isLoad && targetUser != null">
            <div class="col-md-5 col-sm-5">
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
                                <span class="pull-right capitalize-font">{{ targetUser.nom_1 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Segundo nombre</span>
                                <span class="pull-right capitalize-font">{{ targetUser.nom_2 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Primer apellido</span>
                                <span class="pull-right capitalize-font">{{ targetUser.ape_1 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Segundo apellido</span>
                                <span class="pull-right capitalize-font">{{ targetUser.ape_2 }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Tipo doc</span>
                                <span class="pull-right capitalize-font">{{ targetUser.t_doc }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Identificación</span>
                                <span class="pull-right capitalize-font">{{ targetUser.n_doc }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">                                
                                <span class="pull-left inline-block capitalize-font txt-dark">Edad</span>
                                <span class="pull-right capitalize-font">{{ targetUser.edad }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Departamento</span>
                                <span class="pull-right capitalize-font">{{ showDepto(targetUser.dep) }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Municipio</span>
                                <span class="pull-right capitalize-font">{{ showMcpio(targetUser.mun, targetUser.dep) }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Departamento residencia</span>
                                <span class="pull-right capitalize-font">{{ showDepto(targetUser.dep_res) }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Municipio residencia</span>
                                <span class="pull-right capitalize-font">{{ showMcpio(targetUser.mun_res, targetUser.dep_res) }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Régimen</span>
                                <span class="pull-right capitalize-font">{{ showRegimen(targetUser.regimen) }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">EPS</span>
                                <span class="pull-right capitalize-font">{{ showEPS(targetUser.cod_EPS) }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Latitud</span>
                                <span class="pull-right capitalize-font">{{ (targetUser.lat != undefined)? targetUser.lat: '--' }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Longitud</span>
                                <span class="pull-right capitalize-font">{{ (targetUser.lng != undefined)? targetUser.lng: '--' }}</span>
                                <div class="clearfix"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <h6 class="panel-title txt-dark">DATOS DE SISBÉN</h6>
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
                            <div v-if="targetUser.sisben.length > 0">
                                <span class="pull-left inline-block capitalize-font txt-dark">Manzana</span>
                                <span class="pull-right capitalize-font">{{ targetUser.sisben[0].manz }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Comuna</span>
                                <span class="pull-right capitalize-font">{{ targetUser.sisben[0].comuna }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Dirección</span>
                                <span class="pull-right capitalize-font">{{ targetUser.sisben[0].direcc }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Tel contacto</span>
                                <span class="pull-right capitalize-font">{{ targetUser.sisben[0].telecontac }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Barrio</span>
                                <span class="pull-right capitalize-font">{{ targetUser.sisben[0].n_barrio }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Vereda</span>
                                <span class="pull-right capitalize-font">{{ targetUser.sisben[0].n_vereda }}</span>
                                <div class="clearfix"></div>
                            </div>
                            <div class="alert alert-warning" v-else>
                                <i class="pull-left zmdi zmdi-alert-circle-o pr-15"></i>
                                <p class="pull-left">No se encontró información de SISBÉN relacionada a este usuario!</p>
                                <div class="clearfix"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <h6 class="panel-title txt-dark">DIRECCIÓN SUMINISTRADA POR DANE</h6>
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
                            <div v-if="targetUser.dane.length > 0">
                                <span class="pull-left inline-block capitalize-font txt-dark">Dirección</span>
                                <span class="pull-right capitalize-font">{{ targetUser.dane[0].UVA_DIRUND }}</span>
                                <div class="clearfix"></div>
                            </div>
                            <div class="alert alert-warning" v-else>
                                <i class="pull-left zmdi zmdi-alert-circle-o pr-15"></i>
                                <p class="pull-left">No se encontró información del DANE relacionada a este usuario!</p>
                                <div class="clearfix"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div><!-- End column left -->
            <div class="col-md-4 col-sm-4">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <h6 class="panel-title txt-dark">AGENDAMIENTO</h6>
                        </div>
                        <div class="pull-right">
                            <a href="#" class="pull-left inline-block full-screen">
                                <i class="zmdi zmdi-fullscreen"></i>
                            </a>
                        </div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-15">
                            <div class="alert alert-warning">
                                <i class="pull-left zmdi zmdi-alert-circle-o pr-15 inline-block"></i>
                                <p class="pull-left">No se encontró información relacionada!</p>
                                <div class="clearfix"></div>
                            </div>
                            <div>
                                <a :href="dispatchAgenda" class="btn btn-success btn-block" type="button">Registrar agenda</a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <h6 class="panel-title txt-dark">REGISTRO DE VACUNACIÓN</h6>
                        </div>
                        <div class="pull-right">
                            <a href="#" class="pull-left inline-block full-screen">
                                <i class="zmdi zmdi-fullscreen"></i>
                            </a>
                        </div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0" v-if="targetUser.paiweb.length > 0">
                            <table class="table mb-0">
                                <thead>
                                    <tr><th>Biológico</th><th>Apliación</th><th>Dosis</th></tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(pai, ip) in targetUser.paiweb" :key="ip">
                                        <td>{{ pai.biol }}</td>
                                        <td>{{ pai.f_apli }}</td>
                                        <td>{{ pai.Dosis }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="panel-body row pa-15" v-else>
                            <div class="alert alert-warning">
                                <i class="pull-left zmdi zmdi-alert-circle-o pr-15 inline-block"></i>
                                <p class="pull-left">No se encontró información relacionada!</p>
                                <div class="clearfix"></div>
                            </div>
                            <div>
                                <button class="btn btn-success btn-block" type="button">Registrar aplicación de vacuna</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div><!-- End column central -->
            <div class="col-md-3 col-sm-3">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <h6 class="panel-title txt-dark">MAPA</h6>
                        </div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div class="alert alert-warning ml-15 mr-15" v-if="direcciones.length == 0">
                                <i class="pull-left zmdi zmdi-alert-circle-o pr-15 inline-block"></i>
                                <p class="pull-left">Este usuario o afiliado no tiene una dirección asociada.</p>
                                <div class="clearfix"></div>
                            </div>
                            <div v-if="isLocalize == 'load'" class="text-center font-14 vertical-align-middle ml-15 mr-15">
                                <i class="fa fa-spinner fa-spin"></i> Cargando ubicación en Google maps: {{ direcciones[targetIndex].dir }}.
                            </div>
                            <div :class="(direcciones.length > 0)? 'pa-15': 'is-hidden'">
                                <mapa-personal ref="maparef" altura="400" sincontroles></mapa-personal>
                            </div>
                            <div class="alert alert-warning ml-15 mr-15" v-if="isLocalize == 'no'">
                                <i class="pull-left zmdi zmdi-alert-circle-o pr-15 inline-block"></i>
                                <p class="pull-left">El geocoder no pudo localizar la dirección <strong>{{ direcciones[targetIndex].dir }}</strong>.</p>
                                <div class="clearfix"></div>
                            </div>
                            <ul class="chat-list-wrap">
                                <li class="chat-list">
                                    <div class="chat-body">
                                        <a :class="(targetIndex == ir)? 'is-active': ''" href="javascript:void(0)" v-for="(dr, ir) in direcciones" :key="ir" v-on:click="loadLocation(ir)">
                                            <div class="chat-data">
                                                <img class="user-img img-circle" :src="icono" alt="Dirección"/>
                                                <div class="user-data">
                                                    <span class="name block capitalize-font">{{ dr.fuente }}</span>
                                                    <span class="time block truncate txt-grey" :title="dr.dir">{{ dr.dir }}</span>
                                                </div>
                                                <div class="clearfix"></div>
                                            </div>
                                        </a>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div><!-- End column right -->
        </div><!-- End user description -->
    </div>
</template>
<script>
import Mapa from './mapas/googlemap.vue';

export default {
    components: {'mapa-personal': Mapa},
    props: {
        ruta: {type: String, default: ''},
        icono: {type: String, default: 'none'},
        url_agendar: {type: String, default: 'none'}
    },
    data(){
        return {
            teclas: [8,9,13,37,39,46,109,189],
            op_reg: {'S': 'Subsidiado', 'C': 'Contributivo', 'E': 'Especial'},
            process: {'param': '', 'status': -1},
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
            usuarios: [],
            direcciones: [],
            targetUser: null,
            targetDirection: 'void',
            targetIndex: -1,
            result: null,
            salida: '',
            isLoad: false,
            isLocalize: 'init',      // load | yes | no | init | fixed
            dispatchAgenda: '',
            _temporal: '',
        }
    },
    methods: {
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
                this.usuarios = [];
                this.targetUser = null;
                var path = this.getRuta();
                if(!this.isLoad){
                    if(path != 'void'){
                        this.isLoad = true;
                        axios.get(path).then(response => {
                            console.log('Duma estatal: ');
                            console.log(response.data.length);
                            console.log(response.data);
                            if(response.data == -1){
                                this.salida = 'No se pudo establecer conexión con la base de datos!';
                            }else{
                                console.log('Entró en el else!');
                                console.log(typeof response.data);
                                this.usuarios = response.data;
                                console.log('Los usuarios:');
                                console.log(this.usuarios);
                                if(this.usuarios.length == 0){
                                    this.salida = 'No se encontraron resultados con los criterios de búsqueda seleccionados!';
                                }else if(this.usuarios.length == 1){
                                    this.criterio = '';
                                    this.selectUser(this.usuarios[0]);
                                }else{
                                    this.criterio = '';
                                }
                            }
                            this.isLoad = false;
                        }).catch(err => {console.log});
                    }else{
                        this.salida = 'Debe seleccionar al menos un filtro para realizar la búsqueda!';
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
        showRegimen: function(arg){
            var tm = this.op_reg[arg];
            return (tm == undefined)? '--': tm;
        },
        showEPS: function(codex){
            return dane_get_eps(codex);
        },
        loadLocation: function(index){
            this.targetIndex = index;
            var ref = this.direcciones[this.targetIndex];
            if(ref != undefined && this.$refs.maparef != undefined){
                if(ref.fuente == 'App móvil'){
                    this.isLocalize = 'fixed';
                    this.$refs.maparef.localizarLocation(ref.dir, {'lat': this.targetUser.lat, 'lng': this.targetUser.lng});
                }else{
                    if(ref.position == null){
                        this.isLocalize = 'load';
                        this.$refs.maparef.localizar(ref.dir);
                    }else{
                        this.isLocalize = 'fixed';
                        this.$refs.maparef.localizarLocation(ref.dir, ref.position);
                    }
                }
            }
        },
        selectUser: function(arg){
            this.targetUser = arg;
            this.dispatchAgenda = this.url_agendar.replace('@', this.targetUser._id.$oid);
            console.log(arg);
            console.log(this.dispatchAgenda);
            this.isLocalize = 'init';
            this.extractDirs();
        },
        selectCriterio: function(cri){
            this.criterio = (this.criterio == cri)? '': cri;
            this.targetUser = null;
        },
        extractDirs: function(){
            if(this.targetUser != null){
                this.targetIndex = -1;
                this.direcciones = [];
                var depmun = this.extractDirZona();
                if(this.targetUser.lat != undefined && this.targetUser.lng != undefined){
                    this.direcciones.push({
                        'dir': 'Latitud: ' + this.targetUser.lat + ', longitud: ' + this.targetUser.lng,
                        'fuente': 'App móvil',
                        'position': null
                    });
                }
                if(this.targetUser.dane != undefined && this.targetUser.dane.length > 0){
                    this.direcciones.push({
                        'dir': this.targetUser.dane[0].UVA_DIRUND + depmun,
                        'fuente': 'Dane',
                        'position': null
                    });
                }
                if(this.targetUser.sisben != undefined && this.targetUser.sisben.length > 0){
                    this.direcciones.push({
                        'dir': this.targetUser.sisben[0].direcc + depmun,
                        'fuente': 'Sisben',
                        'position': null
                    });
                }
                if(this.direcciones.length > 0){
                    console.log('Into direcciones');
                    this.loadLocation(0);
                }
            }
        },
        extractDirZona: function(){
            if(this.targetUser.dep_res != '' && this.targetUser.mun_res != ''){
                return ' ' + this.showMcpio(this.targetUser.mun_res, this.targetUser.dep_res) + ', ' + this.showDepto(this.targetUser.dep_res);
            }else{
                return ' ' + this.showMcpio(this.targetUser.mun, this.targetUser.dep) + ', ' + this.showDepto(this.targetUser.dep);
            }
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
        },
        listen: function(){
            this.$eventBus.$on('mf-map-ini', msn => {
                if(this.isLocalize == 'init'){
                    if(this.targetIndex != -1 && this.$refs.maparef != undefined){
                        this.loadLocation(this.targetIndex);
                    }
                }
            });
            this.$eventBus.$on('mf-localize', locale => {
                this.isLocalize = 'yes';
                this.direcciones[this.targetIndex].position = locale
            });
            this.$eventBus.$on('mf-not-localize', msn => {
                this.isLocalize = 'no';
            });
        }
    },
    mounted(){
        this.listen();
    }
}
</script>
<style scoped>
    .puntero {cursor: pointer !important}
    .is-hidden {display:none !important}
    .chat-body > a.is-active > .chat-data {background:linear-gradient(#FFF2CC,#FFE699) !important}
</style>