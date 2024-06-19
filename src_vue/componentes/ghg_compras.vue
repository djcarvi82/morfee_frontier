<template>
    <div :class="status">
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">GHG</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Compras</div>
            </div>
            <div class="form-group mb-0">
                <div class="input-group">
                    <span class="input-group-btn"><button class="btn btn-default bootstrap-touchspin-down px-2" type="button" @click="selectYear(vigencia--)">-</button></span>
                    <input type="text" class="form-control text-center" style="width:8rem" :value="vigencia" @keydown.prevent.stop>
                    <span class="input-group-btn"><button class="btn btn-default bootstrap-touchspin-up px-2" type="button" @click="selectYear(vigencia++)">+</button></span>
                    <span class="input-group-btn d-none">
                        <button class="btn btn-success">
                            <i class="fa fa-spinner fa-spin" v-if="status == state.LOADING"></i>
                            <i class="fa fa-search" v-else></i> 
                            <!-- <span class="ms-2">Consultar</span> -->
                        </button>
                    </span>
                </div>
            </div>
        </div><!-- End header VIGENCIA -->
        <div class="row mb-4">
            <div :class="elm.index == month? 'col-sm-1 df-solid': 'col-sm-1 df-opaco'" v-for="(elm, i) in periodos" :key="i">
                <div class="box-month" @click="selectMonth(elm.index)">
                    <a href="javascript:void(0)" class="btn btn-block btn-mes px-2 py-2">
                        <div class="df-success" :style="{'width': elm.px}"></div>
                        <div class="df-tx">
                            <div class="d-flex justify-content-between">
                                <div>{{ elm.mes.slice(0, 3) }}</div>
                                <div>{{ elm.total > 0? elm.px: '' }}</div>
                            </div>
                        </div>
                    </a>
                    <div class="fuse">{{ miles(elm.total) }}</div>
                </div>
            </div>
        </div><!-- End month's section -->
        <div :class="status_filter + '-static zone-filter mb-4'">
            <div class="zone-title">ZONA DE FILTROS</div>
            <div class="zone-content d-flex">
                <div class="zone-item py-1 px-2">
                    <div class="d-flex align-items-center">
                        <div>
                            <div class="df-label">AÑO</div>
                            <div>{{ vigencia }}</div>
                        </div>
                        <i class="fa fa-times-circle text-dark fs-5 ms-2"></i>
                    </div>
                </div>
                <div class="zone-item py-1 px-2" v-if="month > 0">
                    <div class="d-flex align-items-center">
                        <div>
                            <div class="df-label">MES</div>
                            <div>{{ meses[month] }}</div>
                        </div>
                        <a href="javascript:void(0)" @click="selectMonth(0)" class="ms-2">
                            <i class="fa fa-times-circle text-danger fs-5"></i>
                        </a>
                    </div>
                </div>
                <div class="zone-item py-1 px-2" v-for="(f, i) in filtros" :key="i">
                    <div class="d-flex align-items-center">
                        <div>
                            <div class="df-label">{{ getHumanLabel(f) }}</div>
                            <div>{{ getHumanFilter(f) }}</div>
                        </div>
                        <a href="javascript:void(0)" @click="removeFilters(f)" class="ms-2">
                            <i class="fa fa-times-circle text-danger fs-5"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-3">
                <div :class="'d-nonex panel panel-default card-view border ' + cssStatus('f_tmed')">
                    <div class="panel-heading pb-1">
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0">BÚSQUEDA DE MEDICAMENTO</h6>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="radio-list">
                                <div class="radio-inline pl-0">
                                    <span class="radio radio-success">
                                        <input type="radio" id="radio_9" value="name" v-model="f_point"><label for="radio_9">Nombre</label>
                                    </span>
                                </div>
                                <div class="radio-inline pl-0">
                                    <span class="radio radio-success">
                                        <input type="radio" id="radio_10" value="code" v-model="f_point"><label for="radio_10">Código</label>
                                    </span>
                                </div>
                            </div>
                            <div class="form-group mb-0">
                                <div class="input-group">
                                    <input type="text" class="form-control" v-model.trim="f_code" :placeholder="f_point == 'code'? 'Ingrese el código': 'Ingrese el nombre'" style="text-transform:none">
                                    <span class="input-group-btn">
                                        <button type="button" class="btn btn-success" @click="getCode">
                                            <i class="fa fa-search"></i>
                                        </button>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!-- End panel card -->
                <div :class="'panel panel-default card-view border ' + cssStatus('f_tpo')">
                    <div class="panel-heading pb-1">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">PROVEEDORES</h6>
                                <!-- <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_tpo')" :key="i">{{ sub }}</div> -->
                                <div class="df-subtitle">{{ titles.timer }}</div>
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="radio-list">
                                <div class="radio-inline pl-0">
                                    <span class="radio radio-success">
                                        <input type="radio" id="radio_a" value="5" v-model="top"><label for="radio_a">Top 5</label>
                                    </span>
                                </div>
                                <div class="radio-inline pl-0">
                                    <span class="radio radio-success">
                                        <input type="radio" id="radio_b" value="10" v-model="top"><label for="radio_b">Top 10</label>
                                    </span>
                                </div>
                                <div class="radio-inline pl-0">
                                    <span class="radio radio-success">
                                        <input type="radio" id="radio_c" value="0" v-model="top"><label for="radio_c">Todos</label>
                                    </span>
                                </div>
                            </div>
                            <amchart-barra-vertical
                                ref="gp_pro" 
                                area="75"
                                campo_categoria="_id"
                                campo_valor="suma"
                                empty_category="(En blanco)" 
                                pretag="$"
                                sin_valores
                                grilla="0"
                                redondeado
                                enfocar
                                unidad="24"
                                etiquetas 
                                tooltip
                                cursor
                                multicolor
                                truncar
                                lanzarevento="evt-pro"
                                :custom="customtx"
                                ></amchart-barra-vertical>
                        </div>
                    </div>
                </div><!-- End panel card -->
                <contador-light ref="cnt_cant" class="border" texto="Cantidad" valor="0" loading duracion="1" miles></contador-light>
                <contador-light ref="cnt_cavun" class="border" texto="Costo" valor="0" loading duracion="1" miles pretag="$ " fontsize="20px"></contador-light>
            </div>
            <div class="col-sm-9">
                <div class="row">
                    <div class="col-sm-4">
                        <div :class="'panel panel-default card-view border ' + cssStatus('f_tmed')">
                            <div class="panel-heading pb-1">
                                <div class="d-flex justify-content-between">
                                    <div>
                                        <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPOS DE MEDICAMENTOS</h6>
                                        <!-- <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_tmed')" :key="i">{{ sub }}</div> -->
                                        <div class="df-subtitle">{{ titles.timer }}</div>
                                    </div>
                                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                            <div class="panel-wrapper collapse in">
                                <div class="panel-body">
                                    <amchart-barra 
                                        ref="gp_tmed" 
                                        campo_categoria="_id"
                                        campo_valor="suma"
                                        empty_category="(En blanco)" 
                                        pretag="$"
                                        etiquetas 
                                        sin_valores 
                                        grilla="0" 
                                        tooltip
                                        cursor
                                        multicolor
                                        redondeado
                                        enfocar
                                        unidad="20"
                                        altura="170"
                                        lanzarevento="evt-tmed"
                                        :custom="customtx"
                                        ></amchart-barra>
                                </div>
                            </div>
                        </div><!-- End panel card -->
                    </div>
                    <div class="col-sm-4">
                        <div :class="'panel panel-default card-view border ' + cssStatus('f_tpo')">
                            <div class="panel-heading pb-1">
                                <div class="d-flex justify-content-between">
                                    <div>
                                        <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPOS</h6>
                                        <!-- <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_tpo')" :key="i">{{ sub }}</div> -->
                                        <div class="df-subtitle">{{ titles.timer }}</div>
                                    </div>
                                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                            <div class="panel-wrapper collapse in">
                                <div class="panel-body">
                                    <amchart-barra
                                        ref="gp_tpo" 
                                        area="75"
                                        campo_categoria="_id"
                                        campo_valor="suma"
                                        pretag="$"
                                        sin_valores
                                        grilla="0"
                                        redondeado
                                        enfocar
                                        unidad="20"
                                        altura="170"
                                        etiquetas 
                                        tooltip
                                        cursor
                                        multicolor
                                        lanzarevento="evt-tpo"
                                        :custom="customtx"
                                        ></amchart-barra>
                                </div>
                            </div>
                        </div><!-- End panel card -->
                    </div>
                    <div class="col-sm-4">
                        <div :class="'panel panel-default card-view border ' + cssStatus('f_tm')">
                            <div class="panel-heading pb-1">
                                <div class="d-flex justify-content-between">
                                    <div>
                                        <h6 class="panel-title txt-dark text-bold text-upper mb-0">TIPO DE MOVIMIENTO</h6>
                                        <!-- <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_tm')" :key="i">{{ sub }}</div> -->
                                        <div class="df-subtitle">{{ titles.timer }}</div>
                                    </div>
                                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                                </div>
                            </div>
                            <div class="panel-wrapper collapse in">
                                <div class="panel-body">
                                    <amchart-barra 
                                        ref="gp_tm"
                                        truncar
                                        campo_categoria="_id"
                                        campo_valor="suma"
                                        pretag="$"
                                        sin_valores
                                        grilla="0"
                                        unidad="20"
                                        altura="170"
                                        enfocar
                                        etiquetas 
                                        tooltip
                                        cursor
                                        multicolor
                                        redondeado
                                        lanzarevento="evt-tm"
                                        :custom="customtx"
                                        ></amchart-barra>
                                </div>
                            </div>
                        </div><!-- End panel card -->
                    </div>
                </div>
                <div :class="'panel panel-default card-view border ' + cssStatus('none')">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">KARDEX</h6>
                                <!-- <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_code')" :key="i">{{ sub }}</div> -->
                                <div class="df-subtitle">{{ titles.timer }}</div>
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="table-wrap">
                                <div class="table-responsive">
                                    <table :class="'table table-striped ' + cssStatus('none')">
                                        <thead>
                                            <tr>
                                                <th class="colmin">No.</th>
                                                <th>Código</th>
                                                <th>Medicamento</th>
                                                <th class="text-center">Cantidad</th>
                                                <th class="text-center">Vl. unidad</th>
                                                <th class="text-center">Total</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(elm, i) in items" :key="i">
                                                <td class="text-center">{{ i + 1 }}</td>
                                                <td>{{ elm._id.xa }}</td>
                                                <td>{{ elm.cmx }}</td>
                                                <td class="text-right">{{ miles(elm.total) }}</td>
                                                <td class="text-right">{{ miles(elm._id.xb) }}</td>
                                                <td class="text-right">${{ miles(elm.suma) }}</td>
                                            </tr>
                                        </tbody>
                                        <tfoot>
                                            <tr>
                                                <th colspan="5">TOTAL</th>
                                                <th class="text-right">$ {{ miles(items.reduce((ac, el) => ac + el.suma, 0)) }}</th>
                                            </tr>
                                        </tfoot>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div><!-- End panel card -->
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
            meses: ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            vigencia: 2022, // new Date().getFullYear(),
            month: 0,
            customtx: `Medicamentos: [bold]{total}[/]
                Costo: [bold]{suma}[/]
                Registros: [bold]{lines}[/]`,
            f_tmed: '',
            f_tpo: '',
            f_tm: '',
            f_code: '',
            f_point: 'name',    // code | name
            top: 5,
            periodos: [],
            providers: [],
            items: [],
			datos: [],
            filtros: [],
            titles: {
                'timer': '',
                'line': '',
                'filtros': [],
            },
            subtitles: {'f_pro': 'Proveedores', 'f_tmed': 'Tipo de medicamento: ', 'f_tpo': 'Tipo: ', 'f_tm': 'Tipo de movimiento: ', 'f_code': 'Código de medicamento: '},
            human: {'f_pro': 'PROVEEDOR', 'f_tmed': 'T. MEDICAMENTO', 'f_tpo': 'TIPO', 'f_tm': 'T. MOVIMIENTO', 'f_code': 'CÓDIGO MED.'},
            filter_exe: '',
            is_loadini: true,
            status: 'ini',
            status_filter: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    watch: {
        top: function(val){
            this.setProvider();
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        miles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        altfixed: function(num, dec=1){
            return (num % 1)? Number.parseFloat(num).toFixed(dec): num;
        },
        cssStatus: function(filtro){
            if(this.status_data == this.state.LOADING){
                return 'loading'
            }
            if(this.status_filter == this.state.LOADING){
                if(filtro == 'none'){
                    return 'loading';
                }
                let pos = this.filtros.indexOf(this.filter_exe);
                let local = this.filtros.indexOf(filtro);
                return (local == -1 || local > pos)? 'loading': 'loading-static';
            }
            return '';
        },
        getSubtitles: function(filtro){
            let sub = [];
            for(let i = 0; i < this.filtros.length; i++){
                if(this.filtros[i] == filtro){
                    break;
                }else{
                    console.log(this[filtro]);
                    sub.push(this.subtitles[filtro] + this[filtro]);

                }
            }
            return sub;
        },
        selectYear: function(vgc){  // En el parámetro se incrementa o decrementa la vigencia.
            this.is_loadini = true;
            this.month = 0;
            this.load();
        },
        selectMonth: function(num){
            this.month = num;
            this.filtros = [];
            this.load();//Control(this.vigencia, this.month, 0);
        },
        buildTitles: function(){
            this.titles.timer = (this.month > 0)? this.meses[this.month] + ' de ' + this.vigencia: "Año " + this.vigencia;
            this.titles.filtros = [];
            this.filtros.forEach(filtro => {
                this.titles.filtros.push({
                    'name': filtro,
                    'label': this.subtitles[filtro] + this[filtro],
                });
            });
        },
        removeFilters: function(arg){   // Es invocado en la 
            let pos = this.filtros.findIndex(elm => elm == arg);
            this.filtros.splice(pos, 10);
            this.loadFilter('no-apply');
            if(arg == 'f_code'){
                this.f_code = '';
            }
        },
        updateFilters: function(arg){
            let pos = this.filtros.findIndex(elm => elm == arg) + 1;
            if(pos > 0){
                this.filtros.splice(pos, 10);
            }else{
                this.filtros.push(arg);
            }
            this.loadFilter(arg);
        },
        getHumanLabel: function(arg){
            return this.human[arg];
        },
        getHumanFilter: function(arg){
            return (this[arg] == "")? "(En blanco)": this[arg];
        },
        setProvider: function(){
            let tmp = (this.top == 0)? this.providers: this.providers.slice(0, this.top);
            this.$refs.gp_pro.setDatos(tmp.sort((a, b) => {
                if(a.suma == b.suma){
                    return 0;
                }
                return (a.suma < b.suma)? -1: 1;
            }));
        },
        load: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                let tm = {};
                let max = 0;
                let pam = new FormData();
                pam.append('f_point', this.f_point);
                pam.append('vigencia', this.vigencia);
                if(this.month > 0) pam.append('mes', this.month);
                if(this.is_loadini){
                    this.meses.slice(1).forEach((elm, i) => {
                        let ike = i + 1;
                        tm[ike] = {'index': ike, 'mes': elm, 'total': 0, 'suma': 0, 'diff': 0, 'equal': 0, 'px': 0};
                    });
                }
                axios.post(root_path + 'ghg/dataini', pam).then(res => {
                    if(this.is_loadini){
                        res.data[0].periodos.forEach(elm => {
                            let index = parseInt(elm._id);
                            tm[index].suma += elm.suma;
                            tm[index].total += elm.total;
                            max += elm.suma;
                        });
                        this.periodos = Object.values(tm).map(elm => {
                            let aux = (elm.suma == 0)? 0: (elm.suma / max) * 100;
                            elm.px = this.altfixed(aux) + '%';
                            return elm;
                        });
                        this.is_loadini = false;
                    }
                    this.$refs.gp_tmed.setDatos(res.data[0].timedis);
                    this.$refs.gp_tpo.setDatos(res.data[0].tipos);
                    this.$refs.gp_tm.setDatos(res.data[0].moves);
                    this.providers = res.data[0].providers;
                    this.setProvider();
                    this.items = res.data[0].codmed;
                    this.buildTitles();
                    this.$refs.cnt_cant.setValor(res.data[0].cnt_cantidad[0].suma);
                    this.$refs.cnt_cavun.setValor(res.data[0].cnt_costo[0].suma);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        loadFilter: function(filtername){
            if(this.status_filter != this.state.LOADING){
                this.status_filter = this.state.LOADING;
                this.filter_exe = filtername;
                let pam = new FormData();
                pam.append('f_point', this.f_point);
                pam.append('vigencia', this.vigencia);
                if(this.month > 0) pam.append('mes', this.month);
                this.filtros.forEach(elm => {
                    if(this[elm] == ""){
                        pam.append(elm, "-empty-") 
                    }else{
                        pam.append(elm, this[elm]) 
                    }
                });
                axios.post(root_path + 'ghg/dataini', pam).then(res => {
                    ['f_tmed', 'f_tpo', 'f_tm', 'f_pro'].forEach(elm => {
                        if(this.filtros.some(fto => fto == elm)){

                        }else{
                            if(elm == 'f_tmed'){
                                this.$refs.gp_tmed.setDatos(res.data[0].timedis);
                            }else if(elm == 'f_tpo'){
                                this.$refs.gp_tpo.setDatos(res.data[0].tipos);
                            }else if(elm == 'f_tm'){
                                this.$refs.gp_tm.setDatos(res.data[0].moves);
                            }else if(elm == 'f_pro'){
                                this.providers = res.data[0].providers;
                                this.setProvider();
                            }
                        }
                    });
                    this.items = res.data[0].codmed;
                    this.buildTitles();
                    this.$refs.cnt_cant.setValor(res.data[0].cnt_cantidad[0].suma);
                    this.$refs.cnt_cavun.setValor(res.data[0].cnt_costo[0].suma);
                    this.status_filter = this.state.LOADED;
                }).catch(err => {
                    this.status_filter = this.state.FAILED;
                });
            }
        },
        getCode: function(){
            if(this.isEmpty(this.f_code)){
                this.removeFilters('f_code');
            }else{
                this.updateFilters('f_code');
            }
        },
        listen: function(){
            this.$eventBus.$on('evt-tmed', arg => {
                this.f_tmed = arg._id;
                this.updateFilters('f_tmed');
            });
            this.$eventBus.$on('evt-tpo', arg => {
                this.f_tpo = arg._id;
                this.updateFilters('f_tpo');
            });
            this.$eventBus.$on('evt-tm', arg => {
                this.f_tm = arg._id;
                this.updateFilters('f_tm');
            });
            this.$eventBus.$on('evt-pro', arg => {
                this.f_pro = arg._id;
                this.updateFilters('f_pro');
            });
        }
    },
    mounted() {
        this.load();
        this.listen();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .loading {opacity: .45; pointer-events: none !important; user-select: nonse !important}
    .btn-mes {position:relative; border:none; background:linear-gradient(#FFFFFF, #EAEAEA) !important; font-family: Arial; font-size:.75rem; color:#000; letter-spacing: 1px}
    .btn-mes .df-success {position:absolute; top:0; bottom:0; left:0; background:#17B978; z-index: 100}
    .btn-mes .df-tx {position:relative; z-index: 1000}
    .day {background:#000; color:#FFF; padding: .2rem .5rem; font-size:11px; font-family: Verdana; letter-spacing: 2px; text-align: center}
    .df-opaco {opacity: .45}
    .df-filtro {background:#FCFCFC}
    .df-filtro + .df-filtro {border-top:1px solid #FFF}
    .df-label {font-size:10px; font-family: Verdana; letter-spacing: 1px; color:#000 !important}
    .df-subtitle {font-size:.8rem; letter-spacing: 1px; color:#000}
    .loading {opacity: .45; pointer-events: none}
    .loading-static {pointer-events: none !important; user-select: none !important; cursor: wait !important}
    .col-sm-1.df-opaco:hover {opacity: .7}
    .row > .col-sm-1 {padding-left: 5px; padding-right: 5px}
    .row > .col-sm-1:first-child {padding-left: 15px}
    .row > .col-sm-1:last-child {padding-right: 15px}
    .fuse {letter-spacing:2px; font-family: Verdana; font-size:11px; text-align: center; background:#000; border-top:1px solid #000; color:#FFF; padding-top:0.1rem; padding-bottom:0.1rem; user-select: none; cursor: pointer}
    .df-opaco > .fuse {background:#999; border-top-color:#999}
    .df-solid .fuse {background:#F0C541; padding-top:8px; padding-bottom: 8px; color:#000 !important}
    .box-month {border:1px solid #000}
    /* .col-sm-1.df-opaco:hover > .fuse {background: #F0C541; color:#000} */
    .box-filter {border:2px dashed #DDD; background:#FCFCFC}
    .zone-filter {background: #EDEDED; border:1px solid #777; color:#000}
    .zone-filter .zone-title {letter-spacing:2px; font-family: Verdana; font-size:11px; text-align: center; background:#777; color:#FFF; padding-top:0.1rem; padding-bottom:0.1rem; user-select: none}
    .zone-item {border-right:1px solid #777; background: #FFF; user-select:none !important}
    /* .zone-filter .zone-content {} */
</style>
