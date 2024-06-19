<template>
    <div>
        <div class="panel panel-default card-view border">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <div>
                        <h5 class="panel-title txt-dark fs-4">TRIÁNGULOS</h5>
                        <div class="fs-7">Fuente: Facturación</div>
                    </div>
                    <a href="#" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div  class="panel-body">
                    <div class="mb-2">
                        <div class="d-flex">
                            <div class="form-group mb-0">
                                <label class="control-label mb-10">Periodo de referencia</label>
                                <div class="input-group">
                                    <span class="input-group-btn">
                                        <button class="btn btn-default bootstrap-touchspin-down px-2" type="button" @click="downMonth">-</button>
                                    </span>
                                    <input type="text" class="form-control text-center" v-model="f_periodo">
                                    <span class="input-group-btn">
                                        <button class="btn btn-default bootstrap-touchspin-up px-2" type="button" @click="upMonth">+</button>
                                    </span>
                                    <span class="input-group-btn">
                                        <button class="btn btn-success" @click="clickDown">
                                            <i class="fa fa-spinner fa-spin" v-if="status == state.LOADING"></i>
                                            <i class="fa fa-search" v-else></i> 
                                            <span class="ms-2">Consultar</span>
                                        </button>
                                    </span>
                                </div>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between">
                            <div class="d-flex">
                                <div class="me-3">
                                    <div class="checkbox checkbox-success">
                                        <input id="ck1" type="checkbox" :checked="f_cross == 'bg-cruce'" @click="f_cross = (f_cross == 'bg-cruce')? '': 'bg-cruce'">
                                        <label for="ck1">Intersección</label>
                                    </div>
                                </div>
                                <div class="me-3">
                                    <div class="checkbox checkbox-success">
                                        <input id="ck2" type="checkbox" :checked="f_in == 'bg-in'" @click="f_in = (f_in == 'bg-in')? '': 'bg-in'">
                                        <label for="ck2">Rango</label>
                                    </div>
                                </div>
                                <div class="me-3">
                                    <div class="checkbox checkbox-success">
                                        <input id="ck3" type="checkbox" :checked="f_out == 'bg-danger'" @click="f_out = (f_out == 'bg-danger')? '': 'bg-danger'">
                                        <label for="ck3">Fuera de rango</label>
                                    </div>
                                </div>
                                <div class="me-3">
                                    <div class="checkbox checkbox-success">
                                        <input id="ck4" type="checkbox" :checked="f_left == ' df-out'" @click="f_left = (f_left == ' df-out')? '': ' df-out'">
                                        <label for="ck4">Alinear intersecciones</label>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <div class="checkbox checkbox-success">
                                    <input id="ck5" type="checkbox" v-model="show_head">
                                    <label for="ck5">Cabeceras detalladas</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="d-flex align-items-center mb-4" v-if="status == state.LOADING">
                        <i class="fa fa-spinner fa-spin"></i>
                        <span class="ms-2">Cargando datos...</span>
                    </div>
                    <div :class="status == state.LOADING? 'table-responsive opaco': 'table-responsive'" v-if="status != 'ini'">
                        <table class="table table-bordered table-pyramid">
                            <thead v-if="show_head">
                                <tr class="tr-title">
                                    <th style="background:#E5E5E5; border-bottom:1px solid transparent !important"></th><th v-for="(hd, i) in head" :key="i" :colspan="hd.cols" class="df-grey">{{ hd.year }}</th>
                                </tr>
                                <tr class="tr-sub">
                                    <th style="background:#E5E5E5; border-bottom:1px solid transparent !important; border-top:1px solid transparent !important"></th><th class="df-grey py-0" v-for="(elm, i) in rcol" :key="i">{{ getMes(elm.ym) }}</th>
                                </tr>
                                <tr class="tr-sub">
                                    <th style="background:#E5E5E5; border-top:1px solid transparent !important"></th><th class="df-grey py-0" v-for="(elm, i) in rcol" :key="i">{{ i + 1 }}</th>
                                </tr>
                            </thead>
                            <thead v-else>
                                <tr>
                                    <th style="background:#E5E5E5"></th>
                                    <th class="df-grey" v-for="(elm, i) in rcol" :key="i">{{ elm.ym }}</th>
                                </tr>
                            </thead>
                            <tbody v-if="status == state.LOADED">
                                <tr v-for="(row, r) in rcol" :key="r">
                                    <th class="df-grey">{{ row.ym }}</th>
                                    <td v-for="(col, c) in rcol" :key="c" :class="getClass(r, c)">{{ getValor(row.ym, col.ym) }}</td>
                                </tr>
                            </tbody>
                            <tbody v-else>
                                <tr v-for="(row, r) in rcol" :key="r">
                                    <th class="df-grey">{{ row.ym }}</th>
                                    <td v-for="(col, c) in rcol" :key="c"></td>
                                </tr>
                            </tbody>
                        </table>
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
		pathdata: {type: String, default: ''},
        cliente: {type: String, default: ''},
        clientetx: {type: String, default: ''}
    },
    data() {
        return {
            mss: ['', 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            fuente: (this.cliente == '0')? 'retec_facturas_0': this.cliente + '_retec_facturas',
            from: '',
            to: '',
            anio: '',
            mes: '',
            show_head: true,
            f_periodo: '',
            f_cross: 'bg-cruce',
            f_in: 'bg-in',
            f_out: 'bg-danger',
            f_left: '',
			datos: [],
            hash: {},
            rcol: [],
            akey: [],
            head: [],
            status: 'ini',
            status_x: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        getClass: function(r, c){
            if(r == c){
                return this.f_cross;
            }
            return (c < r)? this.f_out + this.f_left: this.f_in;
        },
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        clearNumber: function(num){
            if(num % 1 == 0){
                return this.formatMiles(num);
            }else{
                return this.formatMiles(parseFloat(num).toFixed(2));
            }
        },
        upMonth: function(num){
            if(this.status != this.state.LOADING){
                if(this.mes == 12){
                    this.mes = 1;
                    this.anio++;
                }else{
                    this.mes++;
                }
                this.f_periodo = this.anio + this.mes.toString().padStart(2, '0');
            }
        },
        downMonth: function(num){
            if(this.status != this.state.LOADING){
                if(this.mes == 1){
                    this.mes = 12;
                    this.anio--;
                }else{
                    this.mes--;
                }
                this.f_periodo = this.anio + this.mes.toString().padStart(2, '0');
            }
        },
        getMes: function(ym){
            let m = parseInt(ym.toString().slice(-2));
            return this.mss[m];
        },
        makePyramid: function(y, m){
            this.hash = {};
            this.rcol = [];
            this.akey = [];
            this.head = [];
            let hd = {};
            for(let i = 1; i < 37; i++){
                if(m == 0){
                    m = 12;
                    y--;
                }
                let per = y + m.toString().padStart(2, '0');
                this.akey.push(per);
                this.rcol.unshift({'ym': per, 'desc': i, 'asc': 37 - i, 'valor': 0, 'stt': 'off'});
                if(hd[y] == undefined) hd[y] = {'year': y, 'cols': 0};
                hd[y].cols++;
                m--;
            }
            this.head = Object.values(hd).sort((a, b) => a.year - b.year);
            this.rcol.forEach(elm => {
                this.hash[elm.ym] = {};
                this.rcol.forEach(axu => {
                    this.hash[elm.ym][axu.ym] = {'valor': 0, 'stt': 'off', 'asc': elm.asc};
                });
            });
            this.from = this.rcol[0].ym;
            this.to = this.rcol[this.rcol.length - 1].ym;
            this.loadData();
        },
        loadData: function(){
            if(this.status != this.state.LOADING){
                let pam = new FormData();
                pam.append('tema', this.fuente);
                this.status = this.state.LOADING;
                axios.post(this.pathdata, pam).then(res => {
                    this.datos = (res.data.length > 0)? res.data[0].datos: [];
                    this.datos.forEach(elm => {
                        this.setValor(elm._id.f_pre, elm._id.f_rad, elm.total);
                    });
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        getValor: function(row, col){
            let tm = this.hash[row][col];
            return tm.stt == 'off'? '--': this.clearNumber(tm.valor);
        },
        setValor: function(row, col, val){
            if(this.akey.includes(row) && this.akey.includes(col)){
                this.hash[row][col].valor = val;
                this.hash[row][col].stt = 'on';
            }else{
                // console.log('Not include!');
                // console.log(row, col);
            }
        },
        clickDown: function(){
            this.makePyramid(this.anio, this.mes);
        }
    },
    mounted() {
        let ki = new Date();
        this.anio = ki.getFullYear();
        this.mes = ki.getMonth() + 1;
        this.f_periodo = this.anio + this.mes.toString().padStart(2, '0');
    }
}
</script>
<style scoped>
.opaco {opacity: 0.5 !important; user-select: none}
.table.table-pyramid th, .table.table-pyramid td {padding:.5rem .4rem; color:#000; font-family: Arial}
.table-bordered.table-pyramid th, .table-bordered.table-pyramid td {border:1px solid #000 !important; color:#000}
.table-bordered.table-pyramid td {text-align: right}
.table-bordered.table-pyramid thead tr.tr-title th {font-size:1.2rem; font-weight: bold; text-align: center !important}
.table-bordered.table-pyramid thead tr.tr-sub th {font-size:.7rem; font-weight: bold; text-align: center !important}

.df-grey {background:#F5F5F5}
.bg-cruce {background: #FFE699}
.bg-in {background:#E2EFDA}
.df-out {display: none}
</style>
