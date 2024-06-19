<template>
    <div>
        <div :class="display == 'general'? 'row': 'd-none'">
            <div class="col-sm-6">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <h6 class="panel-title fs-6 text-center">VALOR DE CONTRATOS</h6>
                        <div class="text-center fs-6">Primeros 20</div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <am-ver ref="gp_1" sin_valores campo_categoria="txmin" campo_valor="val_contrato" etiquetas grilla="0" multicolor lanzarevento="luka" tooltip unidad="35"></am-ver>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <div class="row">
                    <div class="col-sm-12">
                        <div class="panel panel-default card-view border">
                            <div class="panel-heading">
                                <h6 class="panel-title fs-6 text-center text-bold">FACTURAS POR TIPO DE CONTRATO</h6>
                            </div>
                            <div class="panel-wrapper collapse in">
                                <div class="panel-body">
                                    <!-- <am-pie ref="g_conx" campo_categoria="_id" campo_valor="total" etiquetas radio="40" altura="200" label_align leyenda="bottom" paleta="#5470C5,#86BD6C,#FAC858,#EE6666,#73C0DE,#3BA272,#FC8452,#9A60B4"></am-pie> -->
                                    <am-ver ref="g_con" campo_categoria="_id" campo_valor="total" etiquetas unidad="28" grilla="0" sin_valores></am-ver>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12">
                        <div class="panel panel-default card-view border">
                            <div class="panel-heading">
                                <h6 class="panel-title fs-6 text-center text-bold">MODALIDAD CONTRATO</h6>
                            </div>
                            <div class="panel-wrapper collapse in">
                                <div class="panel-body">
                                    <!-- <am-pie ref="g_modx" campo_categoria="_id" campo_valor="total" etiquetas radio="40" altura="200" label_align leyenda="bottom"></am-pie> -->
                                    <am-ver ref="g_mod" campo_categoria="_id" campo_valor="total" etiquetas unidad="28" grilla="0" sin_valores></am-ver>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="panel panel-default card-view border">
                            <div class="panel-heading">
                                <h6 class="panel-title fs-6 text-center">FACTURAS POR RÉGIMEN</h6>
                            </div>
                            <div class="panel-wrapper collapse in">
                                <div class="panel-body">
                                    <am-pie ref="g_reg" campo_categoria="_id" campo_valor="total" etiquetas radio="40" altura="240" paleta="#70AD47,#4472C4,#FFC000,#43682B"></am-pie>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="panel panel-default card-view border">
                            <div class="panel-heading">
                                <h6 class="panel-title fs-6 text-center">POS</h6>
                            </div>
                            <div class="panel-wrapper collapse in">
                                <div class="panel-body">
                                    <am-pie ref="g_pos" campo_categoria="_id" campo_valor="total" etiquetas radio="40" altura="240" paleta="#70AD47,#4472C4,#FFC000,#43682B"></am-pie>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-12">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <h6 class="panel-title fs-5">CONTRATOS</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div class="table-wrap" v-if="status == state.LOADED">
                                <div class="table-responsive">
                                    <table class="table table-striped mb-0x">
                                        <thead>
                                            <tr>
                                                <th class="colmin">No.</th>
                                                <th>Razón Social</th>
                                                <th class="colmin">No. contrato</th>
                                                <th class="colmin">Valor contrato</th>
                                                <th class="colmin">Copago</th>
                                                <th class="colmin">Retefuente</th>
                                                <th class="colmin">IVA</th>
                                                <th class="colmin">Neto</th>
                                                <th class="colmin">Pagado</th>
                                                <th class="colmin">Facturas radicadas</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(elm, i) in rawdata" :key="i">
                                                <td class="py-2 text-center">{{ i + 1 }}</td>
                                                <td class="py-2">{{ elm.razon }}</td>
                                                <td class="py-2 text-center"><span class="label label-success px-3 c-hand" v-on:click="setDetails(elm)">{{ elm._id.n_ref }}</span></td>
                                                <td class="py-2 text-right">{{ formatMiles(elm.val_contrato) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(elm.sum_copago) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(elm.sum_rete) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(elm.sum_iva) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(elm.sum_neto) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(elm.sum_pay) }}</td>
                                                <td class="py-2 text-center"><span class="label label-primary px-3 c-hand" v-on:click="setContrato(elm)">{{ elm.count_fac }}</span></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div v-else-if="status == state.LOADING" class="d-flex align-items-center justify-content-center mb-5">
                                <i class="fa fa-spinner fa-spin fs-3 me-2"></i>
                                <span>Cargando datos...</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>            
        </div>
        <!-- END DISPLAY GENERAL -->
        <div :class="display == 'factura'? 'row': 'd-none'">
            <div class="col-sm-12">
                <div class="panel panel-default card-view border">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between" v-if="contrato != null">
                            <div>
                                <h6 class="panel-title fs-5 mb-0">{{ contrato.razon }}</h6>
                                <span class="fs-6">Facturas radicadas del contrato No. {{ contrato._id.n_ref }}</span>
                            </div>
                            <a href="javascript:void(0)" class="inline-block fs-5 text-danger" v-on:click="closeFacturas">
                                <i class="fa fa-times"></i>
                            </a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body row pa-0">
                            <div class="table-wrap" v-if="status_fac == state.LOADED">
                                <div class="table-responsive">
                                    <table class="table">
                                        <thead>
                                            <tr>
                                                <th class="colmin">No.</th>
                                                <th class="colmin">No. Contrato</th>
                                                <th class="colmin">Factura</th>
                                                <th>Fecha radicado</th>
                                                <th>Usuario que radica</th>
                                                <th>Régimen</th>
                                                <th>POS</th>
                                                <th class="colmin">Copago</th>
                                                <th class="colmin">Retefuente</th>
                                                <th class="colmin">IVA</th>
                                                <th class="colmin">Valor neto</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(fac, i) in facturas" :key="i">
                                                <td class="py-2 text-center">{{ i + 1 }}</td>
                                                <td class="py-2 text-center">{{ fac.numero_contrato }}</td>
                                                <td class="py-2 text-center">{{ fac.factura }}</td>
                                                <td class="py-2">{{ fac.fecha_radicado }}</td>
                                                <td class="py-2">{{ fac.usuario_radica }}</td>
                                                <td class="py-2">{{ fac.tipo_regimen }}</td>
                                                <td class="py-2">{{ fac.pos }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(fac.valor_total_copago) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(fac.total_retefuente) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(fac.total_reteiva) }}</td>
                                                <td class="py-2 text-right">{{ formatMiles(fac.valor_neto) }}</td>
                                            </tr>
                                            <tr class="txt-dark weight-500" style="font-weight:bold">
                                                <td colspan="7">Total</td>
                                                <td class="text-right">{{ formatMiles(facturas.reduce((acum, elm) => acum + elm.valor_total_copago, 0)) }}</td>
                                                <td class="text-right">{{ formatMiles(facturas.reduce((acum, elm) => acum + elm.total_retefuente, 0)) }}</td>
                                                <td class="text-right">{{ formatMiles(facturas.reduce((acum, elm) => acum + elm.total_reteiva, 0)) }}</td>
                                                <td class="text-right">{{ formatMiles(facturas.reduce((acum, elm) => acum + elm.valor_neto, 0)) }}</td>
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
        <!-- END DISPLAY FACTURA -->
        <div :class="display == 'details'? 'row': 'd-none'">
            <div class="col-sm-4">
                <div class="panel panel-default card-view border" v-if="contrato != null">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title fs-5 mb-0">Contrato No. <strong>{{ contrato._id.n_ref }}</strong></h6>
                            <a href="javascript:void(0)" class="inline-block fs-5 text-danger" v-on:click="closeFacturas">
                                <i class="fa fa-times"></i>
                            </a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <am-bar ref="g_mei" campo_categoria="_id" campo_valor="total" sin_valores grilla="0" altura="200" tooltip etiquetas paleta="#4472C4,#70AD47,#FFC000,#43682B"></am-bar>
                            <hr class="light-grey-hr row mt-10 mb-15"/>
                            <div>
                                <div>
                                    <i class="fa fa-square me-2 txt-primary"></i><span class="txt-dark">{{ contrato.razon }}</span>
                                </div>
                                <div>
                                    <i class="fa fa-square me-2 c-hide"></i><span class="txt-grey">Razón social</span>
                                </div>
                            </div>
                            <hr class="light-grey-hr row mt-10 mb-15"/>
                            <div>
                                <div>
                                    <i class="fa fa-square me-2 txt-primary"></i><span class="txt-dark">{{ contrato._id.n_nit }}-{{ contrato.digito }}</span>
                                </div>
                                <div>
                                    <i class="fa fa-square me-2 c-hide"></i><span class="txt-grey">NIT</span>
                                </div>
                            </div>
                            <hr class="light-grey-hr row mt-10 mb-15"/>
                            <div>
                                <div>
                                    <i class="fa fa-square me-2 txt-primary"></i><span class="txt-dark">{{ contrato.codpre }}</span>
                                </div>
                                <div>
                                    <i class="fa fa-square me-2 c-hide"></i><span class="txt-grey">Código de habilitación</span>
                                </div>
                            </div>
                            <hr class="light-grey-hr row mt-10 mb-15"/>
                            <div>
                                <div>
                                    <i class="fa fa-square me-2 txt-primary"></i><span class="txt-dark">{{ contrato.vige_ini }}</span>
                                </div>
                                <div>
                                    <i class="fa fa-square me-2 c-hide"></i><span class="txt-grey">Vigencia inicial</span>
                                </div>
                            </div>
                            <hr class="light-grey-hr row mt-10 mb-15"/>
                            <div>
                                <div>
                                    <i class="fa fa-square me-2 txt-primary"></i><span class="txt-dark">{{ contrato.vige_fin }}</span>
                                </div>
                                <div>
                                    <i class="fa fa-square me-2 c-hide"></i><span class="txt-grey">Vigencia fin</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-8">

            </div>
        </div>
        <!-- END DISPLAY DETAILS -->
    </div>
</template>
<script>
import Counter from './Contador_light.vue';
import PieChart from './amcharts/pie.vue';
import BarChart from './amcharts/bar.vue';
import VerticalChart from './amcharts/bar-vertical.vue';

export default {
    components: {'local-counter': Counter, 'am-pie': PieChart, 'am-bar': BarChart, 'am-ver': VerticalChart},
    data() {
        return {
            display: 'general',
            after20: {},
            contrato: null,
            rawdata: [],
            entidades: [],
            datos: [],
            facturas: [],
            status: 'ini',
            status_fac: 'ini',
            status_det: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
        }
    },
    methods: {
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        isEmpty: function(a){
            return (a == "" || a == undefined || a == null)? true: false;
        },
        toNumber: function(tx){
            return this.isEmpty(tx)? 0: parseFloat(tx);
        },
        loadGeneral: function(){
            this.status = this.state.LOADING;
            axios.post(root_path + 'auditorias/vue/general').then(res => {
                if(res.data.length > 0){
                    let tm = {};
                    this.rawdata = res.data[0].facet_sum;
                    this.rawdata.forEach(elm => {
                        if(tm[elm._id.n_nit] == undefined){
                            tm[elm._id.n_nit] = {'nit': elm._id.n_nit, 'razon': elm.razon, 'txmin': elm.razon.length > 25? elm.razon.slice(0, 25) + '...': elm.razon, 'digito': elm.digito, 'codpre': elm.codpre, 'val_contrato': this.toNumber(elm.val_contrato), 'contratos': [], 'num_fac': elm.count_fac};
                        }
                        if(elm._id.n_ref != ""){
                            tm[elm._id.n_nit].contratos.push({'ref': elm._id.n_ref, 'sum_copago': elm.sum_copago, 'sum_iva': elm.sum_iva, 'sum_neto': elm.sum_neto, 'sum_pay': elm.sum_pay, 'sum_rete': elm.sum_rete});
                        }
                    });
                    this.entidades = Object.values(tm).sort((a, b) => b.val_contrato - a.val_contrato);
                    let porcion = this.entidades.slice(0, 20).sort((a, b) => a.val_contrato - b.val_contrato);
                    this.$refs.gp_1.setDatos(porcion);
                    this.$refs.g_con.setDatos(res.data[0].facet_con.map(elm => elm._id == ''? ({'_id': '(Vacío)', 'total': elm.total}): elm));
                    this.$refs.g_mod.setDatos(res.data[0].facet_mod.map(elm => elm._id == ''? ({'_id': '(Vacío)', 'total': elm.total}): elm));
                    this.$refs.g_reg.setDatos(res.data[0].facet_reg);
                    this.$refs.g_pos.setDatos(res.data[0].facet_pos);
                }
                this.status = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status = this.state.FAILED;
            });
        },
        loadFacturas: function(nit, rf){
            let pam = new FormData();
            pam.append('nit', nit);
            pam.append('contrato', rf);
            this.status_fac = this.state.LOADING;
            axios.post(root_path + 'auditorias/vue/facturas', pam).then(res => {
                this.facturas = res.data;
                this.status_fac = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status_fac = this.state.FAILED;
            });
        },
        setDetails: function(elm){
            this.contrato = elm;
            this.display = 'details';
            let pam = new FormData();
            pam.append('contrato', this.contrato._id.n_ref);
            this.status_det = this.state.LOADING;
            axios.post(root_path + 'auditorias/vue/details', pam).then(res => {
                this.$refs.g_mei.setDatos([{_id:'Neto factura', total: this.contrato.sum_neto}, {_id:'Valor pagado', total: this.contrato.sum_pay}]);
                this.status_det = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status_det = this.state.FAILED;
            });
        },
        setContrato: function(elm){
            this.contrato = elm;
            this.loadFacturas(this.contrato._id.n_nit, this.contrato._id.n_ref);
            this.display = 'factura';
        },
        closeFacturas: function(){
            this.display = 'general';
            this.facturas = [];
            this.contrato = null;
        },
		makeTimer: function(vige){
			let tmr = [];
			for(var i = 1; i < 12; i++){
				var fc = new Date(vige, i, 0);
				// tmr.push({'anio': vige, 'mes': i, 'tx': this.meses[i], 'len': fc.getDate(), 'codex': vige + '_' + i, 'iniweek': new Date(vige, i - 1, 1).getDay()});
			}
			// tmr.push({'anio': vige, 'mes': 12, 'tx': this.meses[12], 'len': 31, 'codex': vige + '_' + 12, 'iniweek': new Date(vige, 11, 1).getDay()});
			return tmr;
		},
        addDays20: function(ymd){
            if(this.after20[ymd] != undefined){
                console.log('Existente');
                return this.after20[ymd];
            }else{
                console.log('Created in after20');
                let axu = [26, 28, 28, 28, 28, 28, 27];
                let yin = ymd.toString().split('-').map(num => parseInt(num));
                let fec = new Date(yin[0], yin[1] - 1, yin[2]);
                let days = yin[2] + axu[fec.getDay()];
                fec.setDate(days);
                this.after20[ymd] = [fec.getFullYear(), fec.getMonth() + 1, fec.getDate()].map(num => num < 10? `0${num}`: num).join('-');
                return this.after20[ymd];
            }
        },
        listen: function(){
            this.$eventBus.$on('luka', arg => {
                console.log(arg);
            });
        }
    },
    mounted() {
        this.loadGeneral();
        this.listen();
        console.log(this.addDays20("2022-05-31"));
        console.log(this.addDays20("2022-06-10"));
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space:nowrap; text-align: center}
    .c-hand {cursor:pointer}
    .c-hide {visibility: hidden}
    /* .tm {background:linear-gradient(#70AD47,#4472C4,#FFC000,#43682B)} */
</style>