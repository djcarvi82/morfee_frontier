<template>
    <div>
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">ESTADO</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de auditorías</div>
            </div>
            <div class="d-flex">
                <div class="me-3">
                    <select class="form-control" v-model="f_depto">
                        <option value="">Departamento</option>
                        <option :value="dep._id" v-for="(dep, i) in deptos" :key="i">{{ dep._id }} ({{ formatMiles(dep.total) }})</option>
                    </select>
                </div>
                <div class="me-3">
                    <select class="form-control" v-model="f_user">
                        <option value="">Todos los usuarios</option>
                        <option :value="user._id" v-for="(user, i) in users" :key="i">{{ user._id }} ({{ formatMiles(user.total) }} registros)</option>
                    </select>
                </div>
                <div class="me-3">
                    <select class="form-control" v-model="f_pos">
                        <option value="">Modalidad</option>
                        <option value="POS">POS</option>
                        <option value="NO POS">NO POS</option>
                    </select>
                </div>
                <div class="me-3" style="width:250px">
                    <select class="form-control" v-model="f_nipre">
                        <option :value="{'_id': '', 'prestador': ''}">Todos los prestadores</option>
                        <option :value="ips" v-for="(ips, i) in ipss" :key="i">{{ ips.prestador }}</option>
                    </select>
                </div>
                <div class="me-3">
                    <select class="form-control" v-model="f_periodo">
                        <option value="">Todos...</option>
                        <optgroup :label="elm.anio" v-for="(elm, i) in times" :key="i">
                            <option v-for="(mes, m) in elm.meses" :key="m" :value="mes.ym">{{ mes.tx }} ({{ formatMiles(mes.total) }} registros)</option>
                        </optgroup>
                    </select>
                </div>
                <div>
                    <button class="btn btn-success" @click="loadData"><i class="fa fa-search me-2"></i>Buscar</button>
                </div>
            </div>
        </div>
        <div :class="'row ' + status">
            <div class="col-sm-8">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title txt-dark">ESTADO DE LAS FACTURAS</h6>
                            <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <!-- <div :class="elm.css" v-for="(elm, i) in fillText('ESTADO DE LAS FACTURAS')" :key="i">{{ elm.tx }}</div> -->
                            <amchart-barra 
                                ref="gph_1" 
                                paleta="#6a4c93,#1982c4,#8ac926,#ffca3a,#ff595e" 
                                campo_categoria="_id" 
                                campo_valor="total:No. de registros" 
                                empty_category="(Vacío)" 
                                multicolor 
                                redondeado
                                etiquetas 
                                sin_valores 
                                cursor 
                                lanzarevento="barrilla"
                                tooltip>
                            </amchart-barra>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-4">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title txt-dark">POS / NO POS</h6>
                            <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-torta 
                                ref="gph_2" 
                                paleta="#ffbf69,#00afb9,#ffca3a,#8ac926,#6a4c93" 
                                campo_categoria="_id" 
                                campo_valor="total" 
                                etiquetas 
                                tooltip 
                                altura="300">
                            </amchart-torta>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="panel panel-default card-view border" v-if="status_bar != 'ini'">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <h6 class="panel-title txt-dark">FACTURAS SELECCIONADAS</h6>
                    <div>
                        <div class="btn-group">
                            <button class="btn btn-default btn-outline" :disabled="pagina == 1" type="button" @click="loadSelectBar(barSelect, pagina - 1)"><i class="fa fa-chevron-left me-2"></i> Anterior</button>
                            <button class="btn btn-default btn-outline" :disabled="!hasNext" type="button" @click="loadSelectBar(barSelect, pagina + 1)">Siguiente <i class="fa fa-chevron-right ms-2"></i></button>
                        </div>
                    </div>
                    <!-- <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a> -->
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <div class="d-flex align-items-center" v-if="status_bar == state.LOADING">
                        <i class="fa fa-spinner fa-spin fs-2 me-3"></i>
                        <span>Cargando facturas...</span>
                    </div>
                    <div v-if="status_bar == state.LOADED">
                        <table class="table mb-4">
                            <thead>
                                <tr>
                                    <th class="colmin px-4">No.</th>
                                    <th class="text-center">Número de radicación</th>
                                    <th class="text-centerx">Razón social</th>
                                    <th class="text-center">Factura</th>
                                    <th class="colmin px-4">Fecha radicado</th>
                                    <th>Auditor</th>
                                    <th class="text-center">Departamento</th>
                                    <th class="text-center">Municipio</th>
                                    <th class="text-center">Estado</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(elm, i) in slice" :key="i">
                                    <td class="text-center">{{ wpage(i) }}</td>
                                    <td class="text-center">{{ elm.numero_radicacion }}</td>
                                    <td class="text-centerx">{{ elm.razon_social }}</td>
                                    <td class="text-center">{{ elm.factura }}</td>
                                    <td class="text-center">{{ elm.fecha_radicado }}</td>
                                    <td class="text-center">{{ elm.usuario_auditoria_tecnica }}</td>
                                    <td class="text-center">{{ elm.departamento }}</td>
                                    <td class="text-center">{{ elm.municipio }}</td>
                                    <td class="text-center">{{ elm.estado_tecnica }}</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="d-flex justify-content-end">
                            <div class="btn-group">
                                <button class="btn btn-default btn-outline" :disabled="pagina == 1" type="button" @click="loadSelectBar(barSelect, pagina - 1)"><i class="fa fa-chevron-left me-2"></i> Anterior</button>
                                <button class="btn btn-default btn-outline" :disabled="!hasNext" type="button" @click="loadSelectBar(barSelect, pagina + 1)">Siguiente <i class="fa fa-chevron-right ms-2"></i></button>
                            </div>
                        </div>
                    </div>
                </div><!-- End panel-body -->
            </div><!-- End panel wrapper -->
        </div><!-- End panel -->
    </div><!-- End root element -->
</template>
<script>
export default {
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''}
    },
    data() {
        return {
            mss: ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            f_depto: '',
            f_user: '',
            f_nipre: {'_id': '', 'prestador': ''},
            f_nit: '',
            f_periodo: '',
            f_pos: '',
            prestador: '',
			datos: [],
            posdata: [],
            ipss: [],
            times: [],
            users: [],
            deptos: [],
            slice: [],
            pagina: 1,
            barSelect: '',
            hasNext: false,
            status: 'ini',
            status_bar: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
            last: {'f_user': '', 'f_nit': '', 'f_periodo': '', 'f_pos': '', 'prestador': ''},
        }
    },
    watch: {
        f_nipre: function(val){
            this.f_nit = val._id;
            this.prestador = val.prestador;
        }  
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        clearNumber: function(num){
            return (num % 1 == 0)? num: parseFloat(num).toFixed(2);
        },
        formatMiles: function(num){
            return this.isEmpty(num)? num: num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        wpage: function(it){
            return (50 * (this.pagina -1)) + (it + 1);
        },
        fillText: function(title){
            let tm = [{'tx': title, 'css': 'fs-4'}];
            if(this.status == this.state.LOADED){
                let aux = {'f_user': 'Usuario: ', 'f_nit': 'Prestador: ', 'f_periodo': 'Periodo: ', 'f_pos': 'Modalidad: '};
                ['f_user', 'f_nit', 'f_periodo', 'f_pos'].forEach(elm => {
                    if(this.last[elm] != '' && this[elm] == this.last[elm]){
                        if(elm == 'f_nit'){
                            tm.push({'tx': aux[elm] + this.last.prestador, 'css': ''});
                        }else{
                            tm.push({'tx': aux[elm] + this.last[elm], 'css': ''});
                        }
                    }
                });
            }
            return tm;
        },
        loadInit: function(){
            this.status = this.state.LOADING;
            axios.post(this.pathdata + '/init').then(res => {
                this.datos = res.data[0].estado;
                this.posdata = res.data[0].pos;
                this.ipss = res.data[0].ipss;
                this.users = res.data[0].users.map(elm => {
                    let aux = elm._id == ''? '(Vacio)': elm._id;
                    return {'_id': aux, 'total': elm.total};
                });
                this.deptos = res.data[0].deptos;
                console.log(this.deptos);
                let tmp = {};
                res.data[0].times.forEach(elm => {
                    if(this.isEmpty(elm._id)){

                    }else{
                        let bi = elm._id.toString().split('-');
                        if(tmp[bi[0]] == undefined){
                            tmp[bi[0]] = {'anio': bi[0], 'meses': []};
                        }
                        tmp[bi[0]].meses.push({'tx': this.mss[parseInt(bi[1])], 'ym': elm._id, 'total': elm.total});
                    }
                });
                this.times = Object.values(tmp);
                this.$refs.gph_1.setDatos(this.datos);
                this.$refs.gph_2.setDatos(this.posdata);
                this.status = this.state.LOADED;
            }).catch(err => {
                this.status = this.state.FAILED;
                console.log(err);
            });

        },
        loadData: function(){
            if(this.status != this.state.LOADING && this.status_bar != this.state.LOADING){
                this.status = this.state.LOADING;
                this.status_bar = 'ini';
                this.slice = [];
                this.hasNext = false;
                let pam = new FormData();
                pam.append('depto', this.f_depto);
                pam.append('nit', this.f_nipre._id);
                pam.append('periodo', this.f_periodo);
                pam.append('user', this.f_user);
                pam.append('pos', this.f_pos);
                this.last = {'f_user': this.f_user, 'f_nit': this.f_nipre._id, 'f_periodo': this.f_periodo, 'f_pos': this.f_pos, 'prestador': this.prestador};
                axios.post(this.pathdata, pam).then(res => {
                    this.datos = res.data[0].estado;
                    this.posdata = res.data[0].pos;
                    this.$refs.gph_1.setDatos(this.datos);
                    this.$refs.gph_2.setDatos(this.posdata);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        loadSelectBar: function(stt, page=1){
            if(this.status_bar != this.state.LOADING){
                this.status_bar = this.state.LOADING;
                let pam = new FormData();
                pam.append('depto', this.f_depto);
                pam.append('pagina', page);
                pam.append('nit', this.last.f_nit);
                pam.append('periodo', this.last.f_periodo);
                pam.append('user', this.last.f_user);
                pam.append('pos', this.last.f_pos);
                pam.append('estado', stt);
                this.pagina = (page < 1)? 1: page;
                this.barSelect = stt;
                axios.post(this.pathdata + '/select/bar', pam).then(res => {
                    this.slice = res.data[0].slice;
                    this.hasNext = this.slice.length > 50;
                    if(this.hasNext) this.slice.pop();
                    this.status_bar = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status_bar = this.state.FAILED;
                });
            }
        },
        listen: function(){
            this.$eventBus.$on('barrilla', evt => {
                this.loadSelectBar(evt._id, 1);
            });
        }
    },
    mounted() {
        this.loadInit();
        this.listen();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .loading {opacity: .4}
</style>
