<template>
    <div>
        <div class="row">
            <div class="col-md-12">
                <div class="panel panel-success card-view">
                    <div class="panel-heading">
                        <h6 class="panel-title txt-light">BÚSQUEDA DE USUARIOS</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="row">
                                <div class="col-md-4 col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label">Tipo documento</label>
                                        <select class="form-control" name="tipodoc" v-model="tipo" :disabled="ruta == ''">
                                            <option value=""></option>
                                            <option value="CC">CC</option>
                                            <option value="TI">TI</option>
                                            <option value="RC">RC</option>
                                            <option value="CE">CE</option>
                                            <option value="PA">PA</option>
                                            <option value="PE">PE</option>
                                            <option value="AS">AS</option>
                                            <option value="MS">MS</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label">Referencia BDUA</label>
                                        <input type="text" class="form-control" placeholder="Digite el número de referencia BDUA" v-model="bdua" :disabled="ruta == ''" v-on:keydown="filtro">
                                    </div>
                                </div>
                                <div class="col-md-4 col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label">Número de identificación</label>
                                        <div class="input-group">
                                            <input type="text" class="form-control" autofocus placeholder="Digite el número de identificación aquí" v-model="identidad" :disabled="ruta == ''" v-on:keydown="filtro">
                                            <span class="input-group-btn">
                                                <button type="button" class="btn btn-success" v-on:click="loadData" :disabled="ruta == '' || isLoad">
                                                    <i class="fa fa-search"></i>
                                                </button>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="text-center font-14 vertical-align-middle" v-if="isLoad">
                                <i class="fa fa-spinner fa-spin"></i> Buscando usuario
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="alert alert-danger" v-if="result == null && !isLoad && process.status == 1">
            <p>No se encontró ningún resultado con el número de identificación <strong style="letter-spacing:2px">{{ process.param }}</strong>!</p>
        </div>
        <div class="row" v-else-if="result != null && !isLoad">
            <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">
                <div class="panel panel-primary contact-card card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <div class="user-detail-wrap">
                                <span class="block card-user-name">DATOS PERSONALES</span>
                                <span class="block card-user-desn">Información básica</span>
                            </div>
                        </div>
                        <div class="pull-right"><a href="#" class="inline-block"><i class="zmdi zmdi-view-list txt-light"></i></a></div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div>
                                <span class="pull-left inline-block capitalize-font">Primer nombre</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.nom_1 }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Segundo nombre</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.nom_2 }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Primer apellido</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.ape_1 }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Segundo apellido</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.ape_2 }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Sexo</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.sexo }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Tipo de documento</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.t_doc }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Identificación</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.n_doc }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Fecha de nacimiento</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.f_nac }}</span>
                                <div class="clearfix"></div>
                            </div>
                        </div>	
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">
                <div class="panel panel-primary contact-card card-view">
                    <div class="panel-heading">
                        <div class="pull-left">
                            <div class="user-detail-wrap">
                                <span class="block card-user-name">AFILIACIÓN</span>
                                <span class="block card-user-desn">Régimen de salud</span>
                            </div>
                        </div>
                        <div class="pull-right"><a href="#" class="inline-block"><i class="zmdi zmdi-view-list txt-light"></i></a></div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div>
                                <span class="pull-left inline-block capitalize-font">Régimen</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.regimen }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">EPS</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.cod_EPS }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Fecha de afiliación</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.f_af }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Estado</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.estado }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">BDUA</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.s_BDUA }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Departamento</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.dep }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Municipio</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.mun }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Zona</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.zona }}</span>
                                <div class="clearfix"></div>
                                <hr class="light-grey-hr row mt-10 mb-10"/>
                                <span class="pull-left inline-block capitalize-font">Población</span>
                                <span class="capitalize-font txt-dark pull-right">{{ result.t_pob }}</span>
                                <div class="clearfix"></div>
                            </div>
                        </div>	
                    </div>
                </div>
            </div>
            <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">

            </div>
            <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">

            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        ruta: {type: String, default: ''},
    },
    data(){
        return {
            teclas: [8,9,13,37,39,46,109,189],
            process: {'param': '', 'status': -1},
            identidad: '',
            tipo: '',
            bdua: '',
            result: null,
            isLoad: false,
        }
    },
    methods: {
        loadData: function(){
            if(this.ruta != ''){
                if(this.identidad != '' || this.bdua != ''){
                    this.isLoad = true;
                    this.process = {'param': this.identidad, 'status': -1};
                    axios.post(this.ruta, {'identidad': this.identidad, 'tipo': this.tipo, 'bdua': this.bdua}).then(response => {
                        this.result = response.data;
                        this.isLoad = false;
                        this.process.status = 1;
                    }).catch(err => {
                        console.log(err);
                        this.isLoad = false;
                        this.process.status = 0;
                    });
                }else{
                    this.result = null;
                    this.process = {'param': '', 'status': -1};
                    this.isLoad = false;
                }
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
        }
    },
    mounted(){
        console.log('Form is mounted!');
    }
}
</script>