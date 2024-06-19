<template>
    <div>
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">GLOSAS</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de auditorías</div>
            </div>
            <div class="d-flex">
                <div class="me-3" style="width:400px">
                    <select class="form-control" v-model="f_nipre">
                        <option :value="{'_id': '', 'pre': ''}">Todos los prestadores</option>
                        <option :value="ips" v-for="(ips, i) in ipss" :key="i">{{ ips.pre }}</option>
                    </select>
                </div>
                <div>
                    <button class="btn btn-success" @click="loadData(false)"><i class="fa fa-search me-2"></i>Buscar</button>
                </div>
            </div>
        </div>

        <div :class="'row ' + status">
            <div class="col-sm-8">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title txt-dark" v-if="isEmpty(lastpre)">Resumen general</h6>
                            <h6 class="panel-title txt-dark" v-else>Resumen general - <strong>{{ lastpre }}</strong></h6>
                            <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div class="table-wrap">
                                <div class="table-responsive">
                                    <table class="table display product-overview border-none" id="support_table">
                                        <thead>
                                            <tr>
                                                <th class="colminx">Tipo de glosa</th>
                                                <th class="text-center">Número de registros</th>
                                                <th class="text-center">Valor de glosa</th>
                                                <th class="text-center">% Representativo</th>
                                                <th class="colmin px-4">Ver detalles</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(glo, i) in datos" :key="i" :class="cssrow(glo.grupo)">
                                                <td class="colminx">{{ glo.concepto }}</td>
                                                <td class="text-center">{{ formatMiles(glo.total) }}</td>
                                                <td class="text-center">{{ formatMiles(glo.suma) }}</td>
                                                <td class="text-center">{{ glo.percent }}%</td>
                                                <td class="text-center">
                                                    <i class="fa fa-circle fs-5 df-hand text-success" v-if="targetGrupo == glo.grupo"></i>
                                                    <i :class="glo.grupo == '0'? 'fa fa-circle-o fs-5 df-hand xd-none': 'fa fa-circle-o fs-5 df-hand'" @click="setGrupo(glo.grupo)" v-else></i>
                                                </td>
                                            </tr>
                                        </tbody>
                                        <tfoot v-if="datos.length > 0">
                                            <tr>
                                                <th>Sumatoria</th>
                                                <th class="text-center">{{ formatMiles(datos.reduce((a, e) => a + e.total, 0)) }}</th>
                                                <th class="text-center">{{ formatMiles(datos.reduce((a, e) => a + e.suma, 0)) }}</th>
                                                <th></th>
                                                <th></th>
                                            </tr>
                                        </tfoot>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-4">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title txt-dark">Gráfico general</h6>
                            <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <amchart-barra-vertical ref="ismael" porcentaje="%" campo_categoria="concepto" campo_valor="percent:Porcentaje" etiquetas tooltip altura_minima="445" multicolor></amchart-barra-vertical>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div :class="'panel panel-default card-view border ' + status_det" v-if="['loading', 'loaded'].includes(status_det)">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <h6 class="panel-title txt-dark" v-if="isEmpty(lastpre)">Detalles</h6>
                    <h6 class="panel-title txt-dark" v-else>Detalles - <strong>{{ lastpre }}</strong></h6>
                    <a href="#" class="pull-left inline-block full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div class="panel-body row pa-0" v-if="status_det == state.LOADED">
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table class="table display product-overview border-none" id="support_table">
                                <thead>
                                    <tr>
                                        <th :class="targetGrupo == '0'? 'd-none': 'colmin px-3'">Código</th>
                                        <th class="colminx">Glosa</th>
                                        <th class="text-center">Número de registros</th>
                                        <th class="text-center">Valor de glosa</th>
                                        <!-- <th class="text-center">% Representativo</th> -->
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(elm, i) in detalles" :key="i">
                                        <td :class="(targetGrupo == '0')? 'd-none': 'text-center'">{{ elm._id }}</td>
                                        <td>{{ elm.texto }}</td>
                                        <td class="text-center">{{ formatMiles(elm.total) }}</td>
                                        <td class="text-center">{{ formatMiles(elm.suma) }}</td>
                                    </tr>
                                </tbody>
                                <tfoot v-if="detalles.length > 0">
                                    <tr>
                                        <th :colspan="targetGrupo == '0'? 1: 2">Sumatoria</th>
                                        <th class="text-center">{{ formatMiles(detalles.reduce((a, e) => a + e.total, 0)) }}</th>
                                        <th class="text-center">{{ formatMiles(detalles.reduce((a, e) => a + e.suma, 0)) }}</th>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="panel-body" v-else>
                    <div class="d-flex align-items-center">
                        <i class="fa fa-spinner fa-spin fs-2 me-3"></i>
                        <span>Cargando detalles...</span>
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
            temas: {'0': 'Otros conceptos', '1': '1. Facturación', '2': '2. Tarifas', '3': '3. Soportes', '4': '4. Autorización', '5': '5. Cobertura', '6': '6. Pertinencia', '8': '8. Devoluciones', '9': '9. Respuestas a glosas o devoluciones'},
            targetGrupo: '',
            f_nipre: {'_id': '', 'pre': ''},
            ipss: [],
			datos: [],
            detalles: [],
            lastpre: '',
            status: 'ini',
            status_det: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        clearNumber: function(num){
            return (num % 1 == 0)? num: parseFloat(parseFloat(num).toFixed(2));
        },
        cssrow: function(gru){
            if(gru == '0'){
                return (gru == this.targetGrupo)? 'success': 'danger';
            }
            return (gru == this.targetGrupo)? 'success': '';
        },
        setGrupo: function(gru){
            if(this.status_det != this.state.LOADING){
                this.targetGrupo = gru;
                this.loadDetails(this.targetGrupo);
            }
        },
        loadData: function(bool=true){
            if(this.status != this.state.LOADING){
                let yn = bool? 'yes': 'no';
                let pam = new FormData();
                let prename = this.f_nipre.pre;
                pam.append('build', yn);
                pam.append('nit', this.f_nipre._id);
                this.status = this.state.LOADING;
                this.status_det = this.state.INI;
                this.detalles = [];
                this.targetGrupo = '';
                this.lastpre = '';
                axios.post(this.pathdata, pam).then(res => {
                    if(bool){
                        this.ipss = res.data[0].ipss;
                    }
                    let aux = {};
                    let total = res.data[0].general.reduce((ac, elm) => ac + elm.suma, 0);
                    res.data[0].general.map(elm => {
                        let raw = elm.suma / total;
                        elm.factor = this.clearNumber(raw);
                        elm.percent = this.clearNumber(raw * 100);
                        let key = /^\d+$/.test(elm._id)? elm._id: '0';
                        elm.concepto = this.temas[key];
                        elm.orden = (key == '0')? 90: parseInt(key);
                        elm.grupo = key;
                        if(aux[key] == undefined){
                            aux[key] = elm;
                        }else{
                            aux[key].total += elm.total;
                            aux[key].suma += elm.suma;
                            aux[key].factor += elm.factor;
                            aux[key].percent += elm.percent;
                        }
                        return elm;
                    });
                    this.datos = Object.values(aux).sort((a, b) => a.orden - b.orden);
                    this.$refs.ismael.setDatos(this.datos.filter(elm => true).sort((a, b) => b.orden - a.orden));
                    this.lastpre = prename;
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        loadDetails: function(grupo){
            if(this.status_det != this.state.LOADING){
                let pam = new FormData();
                pam.append('grupo', grupo);
                pam.append('nit', this.f_nipre._id);
                this.status_det = this.state.LOADING;
                axios.post(this.pathdata + '/detail', pam).then(res => {
                    this.detalles = res.data[0].general;
                    this.status_det = this.state.LOADED;
                }).catch(err => {
                    this.status_det = this.state.FAILED;
                    console.log(err);
                });
            }
        },
    },
    mounted() {
        this.loadData(true);
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .df-hand {cursor: pointer; user-select: none}
    .loading {opacity: .4}
    .table tfoot th {color:#000; font-weight: bold; letter-spacing: 2px}
</style>
