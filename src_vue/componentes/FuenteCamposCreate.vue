
<template>
    <div>
        <div class="row">
            <div class="col-sm-5 col-md-5">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left"><h6 class="panel-title txt-dark">INFORMACIÓN</h6></div>
                        <div class="pull-right"><a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a></div>
                        <div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div v-if="fuente != null">
                                <span class="pull-left inline-block capitalize-font txt-dark">Fuente de información</span>
                                <span class="pull-right capitalize-font">{{ fuente.nombre }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Colección</span>
                                <span class="pull-right capitalize-font">integra_{{ fuente.alias }}</span>
                                <div class="clearfix"></div><hr class="light-grey-hr row mt-10 mb-10">
                                <span class="pull-left inline-block capitalize-font txt-dark">Fecha de creación</span>
                                <span class="pull-right capitalize-font">{{ fuente.created_at }}</span>
                                <div class="clearfix"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-7 col-md-7">
                <div class="panel panel-default card-view">
                    <div class="panel-heading">
                        <div class="pull-left"><h6 class="panel-title txt-dark" id="titleMain">CAMPOS DE LA FUENTE DE INFORMACIÓN</h6></div>
                        <div class="pull-right"><a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a></div><div class="clearfix"></div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div class="table-wrap" v-if="fuente != null">
                                <div class="table-responsive">
                                    <table class="table table-hover mb-0">
                                        <thead>
                                            <tr>
                                                <th>Nombre del campo</th>
                                                <th>Atributo json</th>
                                                <th class="text-center">Acciones</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(cmp, ic) in fuente.campos" :key="ic">
                                                <td>{{ cmp.campo }}</td>
                                                <td>{{ cmp.json }}</td>
                                                <td class="text-center"><span class="label label-success puntero">Eliminar</span></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div><!-- End panel -->
                </div>
                <div class="panel panel-success card-view">
                    <div class="panel-heading">
                        <h6 class="panel-title text-white" id="titleMain">REGISTRO DE CAMPO</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="row">
                                <div class="col-sm-5 col-md-5">
                                    <label for="" class="control-label">Nombre del campo:</label>
                                    <input type="text" class="form-control" v-model="f_nombre" required>
                                </div>
                                <div class="col-sm-4 col-md-4">
                                    <label for="" class="control-label">Alias json:</label>
                                    <input type="text" class="form-control" v-model="f_json" required v-on:keydown="filtro">
                                    <p class="font-10 text-success">Nombre único sin espacios</p>
                                </div>
                                <div class="col-sm-3 col-md-3">
                                    <label for="" class="control-label">&nbsp;</label>
                                    <div><button type="button" class="btn btn-success btn-block" :disabled="f_nombre == '' || f_json == ''" v-on:click="saveData">Guardar</button></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!-- End panel -->
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        loadpath: {type: String, default: ''},
        fieldpath: {type: String, default: ''},
    },
    data(){
        return {
            teclas: [8,9,13,37,39,46,109,189],
            f_nombre: '',
            f_json: '',
            fuente: null,
        }
    },
    methods: {
        loadData: function(){
            axios.post(this.loadpath).then(res => {
                if(res.data.length > 0){
                    this.fuente = res.data[0];
                }else{
                    this.fuente = null;
                }
            }).catch(err => {console.log(err)});
        },
        filtro: function(e){
            if(/^[A-Z]$/i.test(e.key)){
                return true;
            }else if(this.teclas.indexOf(e.keyCode) >= 0){
                if(e.keyCode == 13){
                    //this.loadData();
                }
                return true;
            }else{
                e.preventDefault();
                return false;
            }
        },
        saveData: function(){
            var info = new FormData();
            info.append('campo', this.f_nombre);
            info.append('json', this.f_json);
            axios.post(this.fieldpath, info).then(res => {
                this.f_nombre = '';
                this.f_json = '';
                this.loadData();
            }).catch(err => {console.log(err)});
        }
    },
    mounted(){
        console.log('Caja fotográfica!');
        this.loadData();
        //alert('Ingrid');
    }
}
</script>
<style scoped>
.text-white {color:#FFF !important}
</style>