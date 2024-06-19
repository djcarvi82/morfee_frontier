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
                                <table class="table mb-0">
                                    <thead>
                                        <tr>
                                            <th class="colmin">No.</th>
                                            <th>Dirección</th>
                                            <th style="width:15rem">Latitud</th>
                                            <th style="width:15rem">Longitud</th>
                                            <th class="colmin">Acción</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(row, i) in filas" :key="i">
                                            <td>{{ i + 1 }}</td>
                                            <td>
                                                {{ row.dir }}
                                                <div class="text-danger fs-7" v-if="['ini', 'OK'].includes(row.state) == false">Geocode no tuvo éxito por la siguiente razón: {{ row.state }}</div>
                                            </td>
                                            <td>{{ row.lat }}</td>
                                            <td>{{ row.lng }}</td>
                                            <td class="colmin">
                                                <a href="javascript:void(0)" @click="removeRow(i)" class="btn btn-xs btn-danger px-2"><i class="fa fa-times"></i></a>
                                                <a href="javascript:void(0)" @click="processOne(row.dir, i)" class="btn btn-xs btn-success px-2" :disabled="(isEmpty(row.dir) || row.state == 'OK')"><i class="fa fa-play"></i></a>
                                                <a href="javascript:void(0)" @click="drawDir(row)" class="btn btn-xs btn-primary px-2" :disabled="row.state != 'OK'"><i class="fa fa-map-marker"></i></a>
                                            </td>
                                        </tr>
                                        <tr v-if="fila != null">
                                            <td class="py-2 px-0" colspan="4">
                                                <div class="form-group mb-0">
                                                    <input type="text" class="form-control" v-model="f_dir" @keypress.enter="processOne(f_dir)">
                                                </div>
                                            </td>
                                            <td class="text-center">
                                                <a href="javascript:void(0)" @click="processOne(f_dir)" class="btn btn-xs btn-success px-2" :disabled="isEmpty(f_dir)"><i class="fa fa-play"></i></a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <button class="btn btn-success" @click="makeRow"><i class="fa fa-plus fs-3"></i> <div>Agregar dirección</div></button>
                            <button class="btn btn-success" @click="reiniciar"><i class="fa fa-refresh fs-3"></i> <div>Reiniciar</div></button>
                            <button class="btn btn-success" @click="dispatchFocus"><i class="fa fa-file-text-o me-1 fs-3"></i> <div>Leer archivo</div></button>
                            <input type="file" class="d-none" id="fl_file" accept=".txt, .csv" v-on:change="selectFile">
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-5">
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
                            <simple-map ref="mapa" :class="style==1? 'border border-primary': ''" altura="64" unidad="vh" localcenter autocentrar zoom="8"></simple-map>
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
		pathdata: {type: String, default: ''}
    },
    data() {
        return {
            geocoder: null,
            file: null,
            f_dir: '',
            fila: null,
            filas: [],
			datos: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        reiniciar: function(){
            document.getElementById('fl_file').value = '';
            this.file = null;
            this.fila = null;
            this.filas = [];
            this.makeRow();
        },
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        limpiar: function(arg){
            return arg.replace(/\s{2,}/g, ' ').replace(/(^\s+|\s+$)/g, '');
        },
        dispatchFocus: function(){
            document.getElementById('fl_file').click();
        },
        selectFile: function(evt){
            if(evt.target.files.length > 0){
                this.file = evt.target.files[0];
                this.readLines();
            }else{
                this.file = null;
            }
        },
        makeRow: function(){
            this.f_dir = '';
            this.fila = {'dir': '', 'lat': '', 'lng': '', 'state': this.state.INI};
        },
        initialize: function(){
            this.geocoder = new google.maps.Geocoder();
            console.log(this.geocoder);
        },
        removeRow: function(index){
            this.filas.splice(index, 1);
        },
        drawDir: function(elm){
            this.$refs.mapa.setDatos([{'title': elm.dir, 'lat': elm.lat, 'lng': elm.lng}]);
        },
        processOne: function(dir, index=-1){
            let tx = this.limpiar(dir);
            if(!this.isEmpty(tx)){
                this.geocoder.geocode({'address': tx}, (rs, stt) => {
                    console.log(stt);
                    if(stt == 'OK'){
                        let lat = rs[0].geometry.location.lat();
                        let lng = rs[0].geometry.location.lng();
                        this.fila = null;
                        this.f_dir = '';
                        if(index >= 0){
                            this.filas[index].lat = lat;
                            this.filas[index].lng = lng;
                            this.filas[index].state = stt;
                        }else{
                            this.filas.push({'dir': tx, 'lat': lat, 'lng': lng, 'state': stt});
                        }
                    }else{
                        if(index >= 0){
                            this.filas[index].state = stt;
                        }
                    }
                });
            }
        },
        processMany: function(){
            for(let i = 0; i < this.filas.length; i++){
                if(this.filas[i].state != 'OK'){
                    this.processOne(this.filas[i].dir, i);
                }
            }
        },
        readLines: function(){
            let reader = new FileReader();
            reader.readAsText(this.file);
            reader.onload = e => {
                let text = reader.result;
                let tmp = text.split('\r\n');
                if(tmp.length > 0){
                    tmp.forEach(rw => {
                        if(!this.isEmpty(rw)){
                            this.filas.push({'dir': rw, 'lat': '', 'lng': '', 'state': this.state.INI});
                        }
                    });
                    this.processMany();
                }
            };
        },
    },
    mounted() {
        this.makeRow();
        this.initialize();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .btn > div {letter-spacing: 2px; font-family: Verdana; font-size:12px; text-transform: none}
</style>
