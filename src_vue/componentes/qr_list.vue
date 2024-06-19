<template>
    <div>
        <div class="row" :class="display == 'list'? '': 'd-none'">
            <div class="col-sm-8">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title fs-5">LISTADO DE AUDITORÍAS CERTIFICADAS</h6>
                            <button class="btn btn-success btn-xs" @click="display = 'add'">Registrar</button>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="table-wrap">
                                <div class="table-responsive">
                                    <table class="table table-hover mb-0">
                                        <thead>
                                            <tr>
                                                <th class="colmin text-center">No.</th>
                                                <th>Factura</th>
                                                <th>Auditor</th>
                                                <th>Fecha de creación</th>
                                                <td>Estado</td>
                                                <td>Valor</td>
                                                <th class="colmin text-center">Acción</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(elm, i) in listado" :key="i" :class="indice == i? 'bg-warning': ''">
                                                <td class="colmin text-center">{{ i + 1 }}</td>
                                                <td>{{ elm.factura }}</td>
                                                <td>{{ elm.auditor }}</td>
                                                <td>{{ elm.fecha }}</td>
                                                <td>{{ elm.estado }}</td>
                                                <td>{{ formatMiles(elm.valor) }}</td>
                                                <td class="text-center">
                                                    <a href="javascript:void(0)" class="x" title="Datos" v-on:click="setFactura(elm, i)"><i class="fa fa-list-alt"></i></a>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div><!-- End table-wrap -->
                        </div><!-- End panel-body -->
                    </div>
                </div>
            </div>
            <div class="col-sm-4">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <h6 class="panel-title fs-5">INFORMACIÓN</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="d-flex justify-content-center">
                                <div style="border:10px solid #111" v-if="targetFac != null">
                                    <img :src="getURL(targetFac._id.$oid)" alt="" class="img-fluid" style="max-width:100%">
                                </div>
                            </div>
                            <table class="table table-sm mt-4 mb-0" v-if="targetFac != null">
                                <tbody>
                                    <tr>
                                        <td class="py-2 px-1">
                                            <div class="d-flex justify-content-between">
                                                <div>Factura:</div><div class="txt-dark fw-bold">{{ targetFac.factura }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="py-2 px-1">
                                            <div class="d-flex justify-content-between">
                                                <div>Auditor:</div><div class="txt-dark fw-bold">{{ targetFac.auditor }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="py-2 px-1">
                                            <div class="d-flex justify-content-between">
                                                <div>Fecha:</div><div class="txt-dark fw-bold">{{ targetFac.fecha }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="py-2 px-1">
                                            <div class="d-flex justify-content-between">
                                                <div>Estado:</div><div class="txt-dark fw-bold">{{ targetFac.estado }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="py-2 px-1">
                                            <div class="d-flex justify-content-between">
                                                <div>Valor:</div><div class="txt-dark fw-bold">{{ formatMiles(targetFac.valor) }}</div>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- End display list -->
        <div class="row" :class="display == 'add'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <h6 class="panel-title fs-5">REGISTRO DE QR PARA CERTIFICAR AUDITORÍA</h6>
                        <button class="btn btn-success btn-xs" @click="display = 'list'">Atrás</button>
                    </div>

                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="row">
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Valor:</label>
                                    <input type="text" class="form-control" v-model="f_fecha" disabled>
                                </div>
                            </div>
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">No. de factura:</label>
                                    <input type="text" class="form-control" v-model="f_factura">
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="form-group">
                                    <label class="control-label">Auditor:</label>
                                    <input type="text" class="form-control" v-model="f_auditor">
                                </div>
                            </div>
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Estado:</label>
                                    <input type="text" class="form-control" v-model="f_estado">
                                </div>
                            </div>
                            <div class="col-sm-3">
                                <div class="form-group">
                                    <label class="control-label">Valor:</label>
                                    <div class="input-group">
                                        <input type="text" class="form-control" v-model="f_valor">
                                        <span class="input-group-btn">
                                            <button type="button" class="btn btn-success" v-on:click="addFacturaQR" :disabled="is_invalid()"><i class="fa fa-check me-1"></i> Registrar</button>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div><!-- End panel-body -->
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        pathlist: {type: String, default: ''},
        pathqr: {type: String, default: ''}
    },
    data(){
        return {
            display: 'list', // list | add
            indice: -1,
            listado: [],
            targetFac: null,
            f_factura: '',
            f_auditor: '',
            f_fecha: '',
            f_estado: '',
            f_valor: 0
        }
    },
    methods: {
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        clearData: function(arg){
            return arg.replace(/\s{2,}/g, ' ').replace(/(^\s+|\s+$)/g, '');
        },
        isEmpty: function(arg){
            return arg == '';
        },
        loadList: function(){
            axios.post(this.pathlist).then(res => {
                this.listado = res.data;
            }).catch(err => {
                console.log(err);
            });
        },
        setFactura: function(fac, ind){
            this.indice = ind;
            this.targetFac = fac;
            console.log(fac);
        },
        getURL: function(code){
            return this.pathqr.replace('@', code);
        },
        addFacturaQR: function(){
            ['f_factura', 'f_auditor', 'f_fecha', 'f_estado', 'f_valor'].forEach(elm => this[elm] = this.clearData(this[elm]));
            if(this.is_invalid() == false){
                let pam = new FormData();
                pam.append('factura', this.f_factura);
                pam.append('auditor', this.f_auditor);
                pam.append('fecha', this.f_fecha);
                pam.append('estado', this.f_estado);
                pam.append('valor', this.f_valor);
                axios.post(this.pathlist + '/save', pam).then(res => {
                    console.log(res.data);
                    this.display = 'list';
                    ['f_factura', 'f_auditor', 'f_fecha', 'f_estado'].forEach(elm => {
                        this[elm] = '';
                    });
                    this.f_valor = 0;
                    this.loadList();
                }).catch(err => {console.log(err)});
            }
        },
        is_invalid: function(){
            let pass  = ['f_factura', 'f_auditor', 'f_fecha', 'f_estado', 'f_valor'].reduce((acum, elm) => (acum == false)? this.isEmpty(this[elm]): acum, false);
            return pass;
        }
    },
    mounted(){
        this.loadList();
        let date = new Date();
        let mes = date.getMonth() + 1;
        let mx = `00${mes}`.slice(-2);
        let dia = date.getDate();
        let dx = `0${dia}`.slice(-2);
        this.f_fecha = date.getFullYear() + '-' + mx + '-' + dx;
    }
}
</script>
<style scoped>
    .colmin {width:1%; white-space: nowrap; text-align: center}
    .fw-bold {font-weight: bold !important}
</style>