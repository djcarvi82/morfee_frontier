<template>
    <div id="dk-modal" class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" style="display: none">
        <div class="modal-dialog modal-lg" style="width:90%">
            <div class="modal-content">
                <div class="modal-header border-bottom" style="background:linear-gradient(#E7E7E7, #F7F7F7)">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                    <h5 class="modal-title" id="myLargeModalLabel">{{ titulo }}</h5>
                </div>
                <div class="modal-body">
                    <div v-if="status == state.LOADED">
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th class="colmin">No.</th>
                                        <th v-for="(elm, i) in fields" :key="i">{{ elm.alias }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(row, i) in datos.slice(0, lc_cantidad)" :key="i">
                                        <td class="text-center">{{ getId(i) }}</td>
                                        <td :class="cssFoco(elm.field)" v-for="(elm, i) in fields" :key="i">{{ row[elm.field] }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="d-flex justify-content-between mt-3">
                            <button type="button" class="btn btn-success" @click="setPagina(-1)" :disabled="pagina == 1">Anterior</button>
                            <button type="button" class="btn btn-success" @click="setPagina(1)" :disabled="is_more == false">Siguiente</button>
                        </div>
                    </div>
                    <div class="d-flex align-items-center" v-if="status == state.LOADING">
                        <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                        <span>Cargando información...</span>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger text-left" @click="launch(false)">Cerrar</button>
                </div>
            </div>
            <!-- /.modal-content -->
        </div>
    </div>
</template>
<script>
export default {
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''},
        altpath: {type: String, default: ''},
        coleccion: {type: String, default: ''},
        campos: {type: String, default: ''},
        cantidad: {type: String, default: ''}
    },
    data() {
        return {
            params: null,
            is_show: false,
            titulo: '',
            lc_coleccion: this.coleccion,
            lc_campos: '',
            lc_cantidad: parseInt(this.cantidad),
            // fields: this.campos.split(',').map( elm => ({'field': elm.split(':')[0], 'alias': elm.split(':')[1]}) ),
            fields: this.fillCampos(),
            pagina: 1,
            periodo: 0,
            filtros: '',
            foco: '',
            is_more: false,
			datos: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        fillCampos: function(){
            let tmp = this.campos.split(',').map(elm => {
                let bi = elm.split(':');
                let alt = bi.length > 1? bi[1]: bi[0];
                return {'field': bi[0], 'alias': alt}
            });
            return tmp;
        },
        getId: function(i){
            return (i + 1) + ((this.pagina - 1) * this.lc_cantidad);
        },
        cssFoco: function(field){
            if(this.foco == ''){
                return '';
            }
            return field == this.foco? 'bg-warning': '';
        },
        isEmpty: function(arg){
            if(['', undefined, null].includes(arg)) return true;
            return /^\s*$/.test(arg);
        },
        setTitulo: function(arg){
            this.titulo = arg;
        },
        launch: function(bool){
            $('#dk-modal').modal(bool? 'show': 'hide');
        },
        loadData: function(){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('coleccion', this.lc_coleccion);
                pam.append('campos', this.lc_campos);
                pam.append('pagina', this.pagina);
                pam.append('cantidad', this.lc_cantidad);
                pam.append('periodo', this.periodo);
                pam.append('filtros', this.filtros);
                this.status = this.state.LOADING;
                axios.post(root_path + 'reservas/slice/data', pam).then(res => {
                    this.datos = (typeof res.data == 'string')? JSON.parse(String(res.data).replace(/:\s+NaN/g, ": null")): res.data;
                    this.is_more = this.datos.length > this.lc_cantidad? true: false;
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        loadAltData: function(){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('pagina', this.pagina);
                pam.append('cantidad', this.lc_cantidad);
                Object.entries(this.params).forEach(elm => {
                    pam.append(elm[0], elm[1]);
                });
                this.status = this.state.LOADING;
                axios.post(this.altpath, pam).then(res => {
                    this.datos = (typeof res.data == 'string')? JSON.parse(String(res.data).replace(/:\s+NaN/g, ": null")): res.data;
                    this.is_more = this.datos.length > this.lc_cantidad? true: false;
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        setParams: function(obj){
            //
        },
        setPagina: function(num){
            if(num == 1 && this.is_more){
                this.pagina++;
                if(this.altpath != ''){
                    this.loadAltData();
                }else{
                    this.loadData();
                }
            }else if(num == -1 && this.pagina > 1){
                this.pagina--;
                if(this.altpath != ''){
                    this.loadAltData();
                }else{
                    this.loadData();
                }
            }
        },
        listen: function(){
            this.$eventBus.$on('open-modal', arg => {   // {'open': bool, }
                this.pagina = 1;
                if(arg.titulo != undefined) this.titulo = arg.titulo;
                if(arg.periodo != undefined) this.periodo = arg.periodo;
                if(arg.filtros != undefined) this.filtros = arg.filtros;
                if(arg.params != undefined) this.params = arg.params;
                this.foco = (arg.foco != undefined)? arg.foco: '';
                $('#dk-modal').modal('show');
                if(this.altpath != ''){
                    this.loadAltData();
                }else{
                    this.loadData();
                }
            });
        }
    },
    mounted() {
        this.lc_campos = this.campos.split(',').map(elm => elm.split(':')[0]).join(',');
        this.listen();
    }
}
</script>
<style scoped>
.colmin {width: 1%; white-space: nowrap; text-align: center}
.modal.mod-hide {display: none !important}
.modal.mod-block {display: block !important}
</style>