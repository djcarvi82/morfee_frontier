<template>
    <div>
        <div class="row">
            <div class="col-sm-7">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">GEOCODIFICACIÓN</h6>
                                <!-- <span class="txt-dark">Temporal</span> -->
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="table-responsive mb-4">
                                <table class="table table-min">
                                    <thead>
                                        <tr>
                                            <th class="colmin">No.</th>
                                            <th>Habilitación</th>
                                            <th>Prestador</th>
                                            <th>Dirección</th>
                                            <th>Latitud</th>
                                            <th>Longitud</th>
                                            <th class="colmin">Acción</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(r, i) in red" :key="i">
                                            <td>{{ i + 1 }}</td>
                                            <td>
                                                {{ r.hab }}<br>
                                                <div class="detail">{{ r.dep }}</div>
                                                <div class="detail">{{ r.mcp }}</div>
                                            </td>
                                            <td>
                                                {{ r.rso }}
                                                <div class="text-danger detail" v-if="r.state != ''">Geocode no tuvo éxito por la siguiente razón: {{ r.state }}</div>
                                            </td>
                                            <td>{{ r.dir }}</td>
                                            <td>{{ r.lat }}</td>
                                            <td>{{ r.lng }}</td>
                                            <td class="colmin">
                                                <a href="javascript:void(0)" class="btn btn-xs btn-warning px-2" @click="preUpdate(r)" ><i class="fa fa-pencil"></i></a>
                                                <a href="javascript:void(0)" class="btn btn-xs btn-success px-2" :disabled="isValidCoord(r.lat, r.lng)" @click="processOne(r.dir, r._id.$oid)"><i class="fa fa-play"></i></a>
                                                <a href="javascript:void(0)" class="btn btn-xs btn-primary px-2" :disabled="!isValidCoord(r.lat, r.lng)" @click="drawCoord(r.lat, r.lng, r.rso)" ><i class="fa fa-map-marker"></i></a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <!-- <button class="btn btn-success"><i class="fa fa-plus fs-3"></i> <div>Agregar dirección</div></button> -->
                            <!-- <button class="btn btn-success"><i class="fa fa-file-text-o me-1 fs-3"></i> <div>Leer archivo</div></button> -->
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-5">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">NIVEL DE GEOCODIFICACIÓN</h6>
                                <!-- <span class="txt-dark">Temporal</span> -->
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-barra-vertical 
                                ref="gp_1" 
                                campo_categoria="_id" 
                                unidad="40" 
                                altura_minima="100" 
                                etiquetas 
                                tooltip 
                                multicolor 
                                paleta="#D61C4E,#17B978"></amchart-barra-vertical>
                        </div>
                    </div>
                </div>
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">MAPA</h6>
                                <!-- <span class="txt-dark">Temporal</span> -->
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <simple-map ref="mapa" class="border border-primary" altura="64" unidad="vh" localcenter autocentrar zoom="8"></simple-map>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Begin modal -->
        <div id="lc_modal_fac" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" style="display: none;">
            <div class="modal-dialog modal-lgx">
                <div class="modal-content" v-if="targetData != null">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h5 class="modal-title" id="myLargeModalLabel">{{ targetData.rso }}</h5>
                    </div>
                    <div :class="'modal-body ' + status">
                        <div class="form-group">
                            <label for="" class="control-label">Nombre del prestador:</label>
                            <input type="text" class="form-control" disabled :value="targetData.rso">
                        </div>
                        <div class="form-group">
                            <label for="" class="control-label">Código de habilitación:</label>
                            <input type="text" class="form-control" disabled :value="targetData.hab">
                        </div>
                        <div class="form-group">
                            <label for="" class="control-label">Departamento:</label>
                            <input type="text" class="form-control" disabled :value="targetData.dep">
                        </div>
                        <div class="form-group">
                            <label for="" class="control-label">Municipio:</label>
                            <input type="text" class="form-control" disabled :value="targetData.mcp">
                        </div>
                        <div class="form-group">
                            <label for="" class="control-label">Dirección:</label>
                            <input type="text" class="form-control" v-model="f_dir">
                        </div>
                        <div class="row">
                            <div class="col-sm-6">
                                <div class="form-group">
                                    <label for="" class="control-label">Latitud:</label>
                                    <input type="text" class="form-control" v-model="f_lat" @keypress="onlyNumber">
                                </div>
                            </div>
                            <div class="col-sm-6">
                                <div class="form-group">
                                    <label for="" class="control-label">Longitud:</label>
                                    <input type="text" class="form-control" v-model="f_lng" @keypress="onlyNumber">
                                </div>
                            </div>
                        </div>
                    </div><!-- End modal-body -->
                    <div :class="'modal-footer ' + status">
                        <button type="button" class="btn btn-danger text-left" data-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-success" @click="modalSave">Guardar cambios</button>
                    </div>
                </div><!-- /.modal-content -->
            </div><!-- /.modal-dialog -->
        </div>        
        <!-- End modal -->
    </div>
</template>
<script>
export default {
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''}
    },
    data() {
        return {
            targetData: null,
            geocoder: null,
            f_dir: '',
            f_lat: '',
            f_lng: '',
            red: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        onlyNumber: function(e){
            let char = String.fromCharCode(e.keyCode);
            if(char == '-' && String(e.target.value) == ''){
                return true;
            }else if(char == '.' && /\./.test(String(e.target.value)) == false){
                return true;
            }
            if(/[0-9]/.test(char) || e.keyCode == 13){
                return true;
            }else{
                e.preventDefault();
            }
        },
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        limpiar: function(arg){
            return arg.replace(/\s{2,}/g, ' ').replace(/(^\s+|\s+$)/g, '');
        },
        isValidCoord: function(a, b){
            return !this.isEmpty(a) && !this.isEmpty(b);
        },
        getCoord: function(loc, pos){
            if(typeof loc == 'object'){
                return loc[pos];
            }
            return "";
        },
        initialize: function(){
            this.geocoder = new google.maps.Geocoder();
        },
        drawDir: function(elm){
            this.$refs.mapa.setDatos([{'title': elm.dir, 'lat': elm.lat, 'lng': elm.lng}]);
        },
        drawCoord: function(lat, lng, pre){
            console.log('drawCoord!');
            console.log(lat, lng);
            if(!this.isEmpty(lat) && !this.isEmpty(lng)){
                this.$refs.mapa.setDatos([{'title': pre, 'lat': lat, 'lng': lng}]);
            }
        },
        iterateRed: function(oid, lat, lng, stt, dire='-none-'){
            for(let i = 0; i < this.red.length; i++){
                if(this.red[i]._id.$oid == oid){
                    this.red[i].lat = lat;
                    this.red[i].lng = lng;
                    this.red[i].state = stt == 'OK'? '': stt;
                    if(dire != '-none-'){
                        this.red[i].dir = dire;
                    }
                    break;
                }
            }
        },
        processOne: function(dir, oid){
            console.log(dir, oid);
            let tx = this.limpiar(dir);
            if(!this.isEmpty(tx)){
                this.geocoder.geocode({'address': tx}, (rs, stt) => {
                    let lat = '';
                    let lng = '';
                    if(stt == 'OK'){
                        lat = rs[0].geometry.location.lat();
                        lng = rs[0].geometry.location.lng();
                        this.saveCoords(oid, lat, lng);
                    }else{
                        this.iterateRed(oid, '', '', stt);
                    }
                });
            }
        },
        saveCoords: function(oid, lat, lng){
            let pam = new FormData();
            pam.append('id', oid);
            pam.append('lat', lat);
            pam.append('lng', lng);
            axios.post(root_path + 'aseguramiento/manager/coords/save', pam).then(res => {
                if(res.data.status == 'success'){
                    this.iterateRed(oid, lat, lng, '');
                }else{
                    this.iterateRed(oid, '', '', 'MORFEE UPDATE FAILED');
                }
            }).catch(err => {
                console.log(err);
                this.iterateRed(oid, '', '', 'MORFEE SERVER ERROR!');
            });
        },
        modalSave: function(){
            if(this.status != this.state.LOADING && this.targetData != null){
                this.status = this.state.LOADING;
                let clave = this.targetData._id.$oid;
                let pam = new FormData();
                pam.append('id', clave);
                pam.append('lat', this.f_lat);
                pam.append('lng', this.f_lng);
                if(this.f_dir != this.targetData.dir){
                    pam.append('dir', this.f_dir);
                }
                axios.post(root_path + 'aseguramiento/manager/coords/save', pam).then(res => {
                    if(res.data.status == 'success'){
                        this.iterateRed(clave, this.f_lat, this.f_lng, '', this.f_dir);
                    }else{
                        this.iterateRed(clave, '', '', 'MORFEE UPDATE FAILED');
                    }
                    this.status = this.state.LOADED;
                    $('#lc_modal_fac').modal('hide');
                }).catch(err => {
                    console.log(err);
                    this.iterateRed(clave, '', '', 'MORFEE SERVER ERROR!');
                    this.status = this.state.FAILED;
                    $('#lc_modal_fac').modal('hide');
                });
            }
        },
        loadNativa: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                let pam = new FormData();
                axios.post(root_path + 'aseguramiento/manager/red', pam).then(res => {
                    this.red = res.data[0].prestadores.map(elm => {
                        elm.lat = this.getCoord(elm.loc, 0);
                        elm.lng = this.getCoord(elm.loc, 1);
                        elm.state = '';
                        return elm;
                    });
                    console.log('kabrim');
                    let tm = res.data[0].kalima.map(elm => {
                        return {"_id": elm._id? 'Sin geocode': 'Geocodificado', 'valor': elm.total };
                    });
                    this.$refs.gp_1.setDatos(tm);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                });
            }
        },
        preUpdate: function(elm){
            this.targetData = elm;
            this.f_dir = this.targetData.dir;
            this.f_lat = this.targetData.lat;
            this.f_lng = this.targetData.lng;
            $('#lc_modal_fac').modal('show');
        }
    },
    mounted() {
        this.initialize();
        this.loadNativa();
    }
}
</script>
<style scoped>
    .loading {opacity: .4; pointer-events: none}
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .btn > div {letter-spacing: 2px; font-family: Verdana; font-size:12px; text-transform: none}
    .detail {font-size:11px; font-family: Arial; letter-spacing: 1px}
    table.table.table-min > tbody > td {padding: .2rem auto !important}
</style>
