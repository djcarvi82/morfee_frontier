<template>
    <div style="min-height:200px">
        <div :class="(lc_filter_len > 0)? 'row mb-0 pb-0': 'd-none'" style="padding-bottom:0 !important; margin-bottom:0 !important">
            <div :class="lc_css[lc_filter_len]" v-for="(fo, i) in lc_filters" :key="i">
                <div :class="isEmpty(lc_data[fo.key + '_' + i])? 'form-group mb-0': 'form-group mb-0 has-success'" v-if="i == (lc_filter_len - 1)">
                    <label class="control-label">{{ fo.label }}</label>
                    <div class="input-group mb-0">
                        <input type="text" class="form-control" autocomplete="off" v-model="lc_data[fo.key + '_' + i]" @change="cambio($event, fo.key + '_' + i)">
                        <span class="input-group-btn">
                            <button class="btn btn-success" type="button" v-on:click="loadData"><i class="fa fa-search"></i></button>
                        </span>
                    </div>
                </div>
                <div :class="isEmpty(lc_data[fo.key + '_' + i])? 'form-group mb-0': 'form-group mb-0 has-success'" v-else>
                    <label class="control-label">{{ antiManager(fo.label) }}</label>
                    <input type="text" class="form-control" autocomplete="off" v-model="lc_data[fo.key + '_' + i]" @change="cambio($event, fo.key + '_' + i)">
                </div>
            </div>
        </div>
        <div class="row mt-1" v-if="lc_filter_len > 0">
            <div class="col-sm-12">
                <div class="form-group">
                    <div class="checkbox checkbox-success">
                        <input id="xd_x" type="checkbox" v-model="wspace">
                        <label for="xd_x" :class="wspace? 'font-12 text-success': 'font-12'" style="font-style:italic">Limpiar espacios</label>
                    </div>
                </div>
            </div>
        </div>
        <div :class="css_config" style="background:linear-gradient(#FFFFFF, #EAEAEA)">
            <div class="border-start border-top border-end px-4 py-4">
                <ul class="nav nav-pills mb-4 border-bottom">
                    <li :class="txconfig == 'Filtros'? 'active': 'border-top border-start border-end'" v-on:click="txconfig = 'Filtros'"><a href="javascript:void(0)" >Filtros</a></li>
                    <li :class="txconfig == 'Columnas'? 'active': 'border-top border-start border-end'" v-on:click="txconfig = 'Columnas'"><a href="javascript:void(0)">Columnas</a></li>
                </ul>
                <div v-if="txconfig == 'Filtros'">
                    <a href="javascript:void(0)" class="btn btn-warning btn-xs" v-on:click="selectAllFilters(false)">Deseleccionar todos</a>
                    <div class="row mt-3">
                        <div class="col-sm-3" v-for="(cm, i) in allFields" :key="i">
                            <div class="checkbox checkbox-primary">
                                <input :id="'xd_' + i" type="checkbox" :value="cm.key" :checked="cm.filter" :disabled="cm.filter == false && lc_filter_len > 5" v-on:click="selectFilterFactory($event, cm.key)">
                                <label :for="'xd_' + i" :title="cm.key">{{ cm.label }}</label>
                            </div>
                        </div>
                    </div>
                    <div class="alert alert-warning d-flex justify-content-start mt-3">
                        <i class="zmdi zmdi-info-outline me-2"></i>
                        <p>Puede seleccionar un máximo de 6 filtros.</p>
                    </div>
                </div>
                <div v-else>
                    <a href="javascript:void(0)" class="btn btn-warning btn-xs" v-on:click="selectAllColumns(true)">Seleccionar todos</a>
                    <a href="javascript:void(0)" class="btn btn-warning btn-xs" v-on:click="selectAllColumns(false)">Deseleccionar todos</a>
                    <div class="row mt-3">
                        <div class="col-sm-3" v-for="(cm, i) in allFields" :key="i">
                            <div class="checkbox checkbox-primary">
                                <input :id="'xz_' + i" type="checkbox" :value="cm.key" :checked="cm.column" v-on:click="selectColumn($event, cm.key)">
                                <label :for="'xz_' + i" :title="cm.key">{{ cm.label }}</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mb-4 text-center border-top" style="position:relative">
            <span class="badge" style="position:absolute; top:-0.7rem; cursor:pointer; border:1px solid #FFF" v-on:click="css_config = (css_config == 'fx-panel hide-panel')? 'fx-panel show-panel': 'fx-panel hide-panel'"><i :class="(css_config == 'fx-panel hide-panel')? 'fa fa-chevron-down': 'fa fa-chevron-up'"></i> {{ txconfig }}</span>
        </div>
        <!-- END SECTION FILTERS -->
        <div class="d-flex justify-content-between align-items-center" v-if="paginas > 0">
            <div>
                <div v-if="status == 'loading'"><i class="fa fa-spin fa-spinner fs-5 me-2"></i> Cargando ...</div>
                <div class="summary" v-else>
                    <div style="letter-spacing:1px">Página <span class="fw-bold">{{ miles(pagina) }}</span> de <span class="fw-bold">{{ miles(paginas) }}</span></div>
                    <div style="letter-spacing:1px">Total registros: <span class="fw-bold">{{ miles(total) }}</span></div>
                </div>
            </div>
            <div>
                <div class="btn-group" v-if="paginas > 5">
                    <button class="btn btn-default btn-outline" type="button" v-on:click="setPagina(1)"><i class="icon-control-start"></i></button>
                    <button class="btn btn-default btn-outline" type="button" v-on:click="setPagina(pagina - 1)"><i class="icon-arrow-left"></i></button>
                </div>
                <div :class="(paginas > 5)? 'btn-group mx-4': 'btn-group'">
                    <button :class="(pagina == p)? 'btn btn-success': 'btn btn-default btn-outline'" v-for="p in rango" :key="p" v-on:click="setPagina(p)">{{ miles(p) }}</button>
                </div>
                <div class="btn-group" v-if="paginas > 5">
                    <button class="btn btn-default btn-outline" type="button" v-on:click="setPagina(pagina + 1)"><i class="icon-arrow-right"></i></button>
                    <button class="btn btn-default btn-outline" type="button" v-on:click="setPagina(paginas)"><i class="icon-control-end"></i></button>
                </div>
            </div>
        </div>
        <div class="text-center pt-5" v-else-if="status == 'loading' || status == 'build'">
            <i class="fa fa-spin fa-spinner fs-4 me-2"></i> Cargando ...
        </div>
        <div class="table-wrap mt-4">
            <div class="table-responsive" v-if="status != 'build'">
                <table :class="(status == 'loading')? 'table table-bordered loading': 'table table-bordered table-customx'">
                    <thead>
                        <tr v-if="keys" style="background:#F0C542" class="bg-gradient">
                            <th>--</th>
                            <th v-for="(cam, i) in columns" :key="i">{{ cam.key }}</th>
                        </tr>
                        <tr>
                            <th class="colmin">No.</th>
                            <th v-for="(cam, i) in columns" :key="i">{{ cam.label }}</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, i) in registros" :key="i">
                            <td class="colmin">{{ getCountRow(i + 1) }}</td>
                            <td v-for="(cam, l) in columns" :key="l">{{ item[cam.key] }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        coleccion: {type: String, default: ''},
        configuracion: {type: String, default: ''},
        keys: {type: Boolean, default: false},
        exclude: {type: String, default: 'no-apply'},
        only: {type: String, default: 'no-apply'},
        filtros: {type: String, default: 'no-apply'}
    },
    data() {
        return {
            memory: '',
            lc_coleccion: '',
            diccionario: null,
            wspace: true,
            campos: [],
            allFields: [],
            keyFields: {},
            columns: [],

            onlyFields: {},
            registros: [],
            plantilla: '',
            fun_action: null,
            total: -1,
            paginas: -1,
            pagina: 1,
            rango: [],
            lim_a: 0,
            lim_b: 0,
            bambu_base: {},
            bambu: {},
            /* FILTERS VARS */
            lc_css: ['', 'col-md-4 col-sm-4', 'col-md-3 col-sm-3', 'col-md-3 col-sm-3', 'col-md-3 col-sm-3', 'col-md-2 col-sm-2', 'col-md-2 col-sm-2'],
            lc_filters: [],         // {key: '', label: ''}
            lc_filter_len: 0,
            lc_data: {},
            lc_filter_key: [],
            params: null,
            css_config: 'fx-panel hide-panel',
            status: 'build',
            txconfig: 'Filtros'
        }
    },
    methods: {
        setCollection: function(collec){
            this.status = 'build';
            this.lc_coleccion = collec;
            this.memory = this.lc_coleccion + '_cfg';
            this.diccionario = null;
            this.allFields = [];
            this.keyFields = {};
            this.columns = [];
            this.lc_filters = [];
            this.lc_filter_len = 0;
            this.lc_filter_key = [];
            if(this.configuracion == ''){
                this.loadInfo();
            }else{
                this.setConfig();
            }
        },
        cambio: function(evt, llave){
            if(this.wspace){
                this.lc_data[llave] = evt.target.value.replace(/\s{2,}/g, ' ').replace(/(^\s+|\s+$)/g, '');
            }
        },
        isEmpty: function(arg){
            return (arg == '' || arg == undefined)? true: false;
        },
        miles: function(num){
            var regla = /(\d+)(\d{3})/;
            var tmp = String(num);
            while(regla.test(tmp)){
                tmp = tmp.replace(regla, '$1' + ',' + '$2');
            }
            return tmp;
        },
        antiManager: function(arg){
            // return arg.replace('O', "&#79;");
            return arg;
        },
        disableCheck: function(mode){
            if(mode == 'on'){
                return false;
            }else if(this.campos.filter(elm => elm.active == 'on').length > 5){
                return true;
            }else{
                return false;
            }
        },
        makeFiltersFactory: function(){
            this.lc_filters = this.allFields.filter(elm => elm.filter);
            this.lc_filter_len = this.lc_filters.length;
            this.lc_filter_key = this.lc_filters.map(elm => elm.key);
        },
        selectFilterFactory: function(evt, col){
            if(this.keyFields[col] != undefined && this.allFields[this.keyFields[col]].key == col){
                this.allFields[this.keyFields[col]].filter = evt.target.checked? true: false;
            }
            this.makeFiltersFactory();
        },
        selectAllFilters: function(bool){
            this.allFields.forEach(elm => elm.filter = bool);
            this.makeFiltersFactory();
        },
        selectAllColumns: function(bool){
            this.allFields.forEach(elm => elm.column = bool);
            this.refreshColumns();
            var cols = this.allFields.filter(elm => elm.column).map(elm => elm.key).join(',');
            localStorage.setItem(this.memory, cols);
        },
        selectColumn: function(evt, col){
            if(this.keyFields[col] != undefined && this.allFields[this.keyFields[col]].key == col){
                this.allFields[this.keyFields[col]].column = evt.target.checked? true: false;
            }
            this.refreshColumns();
            var cols = this.allFields.filter(elm => elm.column).map(elm => elm.key).join(',');
            localStorage.setItem(this.memory, cols);
        },
        addBambu: function(name, value, first=false){
            if(first) this.bambu = {};
            this.bambu[name] = value;
            return value;
        },
        isChangeBambu: function(){
            var k0 = Object.keys(this.bambu_base);
            var k1 = Object.keys(this.bambu);
            if(k0.length != k1.length){
                this.bambu_base = this.bambu;
                return true;
            }else{
                let pass = false;
                for(var key of k1){
                    if(key != 'pagina' && key != 'makles' && this.bambu_base[key] != this.bambu[key]){
                        pass = true;
                        break;
                    }
                }
                this.bambu_base = this.bambu;
                return pass;
            }
        },
        extractData: function(){
            let tmp = [];
            for(var i in this.lc_data){
                let axu = i.split('_');
                var key = (axu.length > 2)? axu.slice(0, -1).join('_'): axu[0];
                console.log('Key: ' + key);
                if(this.lc_filter_key.indexOf(key) >= 0){
                    var valor = this.lc_data[i];
                    if(this.wspace && valor != undefined){
                        valor = valor.replace(/\s{2,}/g, ' ').replace(/(^\s+|\s+$)/g, '');
                    }
                    if(valor != '' && valor != undefined){
                        tmp.push(key);
                        this.params.append(key, this.addBambu(key, valor, false));
                    }
                }else{
                    console.log('Desaprobado');
                }
            }
            if(tmp.length > 0){
                var makles = tmp.join('|');
                let mkl = this.addBambu('makles', makles, false);
                console.log('Mkl');
                console.log(mkl);
                this.params.append('makles', mkl);
            }
        },
        loadInfo: function(){
            var ruta = root_path + 'users/admin/diccionario/' + this.lc_coleccion + '/';
            axios.get(ruta).then(res => {
                this.diccionario = res.data;
                this.allFields = this.diccionario.campos.split('|').map((elm, i) => {
                    var bis = elm.split(':');
                    var tx = (bis.length == 3 && bis[2] != '')? bis[2]: bis[1];
                    this.keyFields[bis[0]] = i;
                    return {'key': bis[0], 'label': tx, 'filter': i < 4, 'column': true};
                });
                this.applyOptionsFactory();
                this.makeFiltersFactory();
                this.loadData();
            }).catch(err => {console.log(err)});
        },
        setConfig: function(){
            this.allFields = this.configuracion.split('|').map((elm, i) => {
                var bis = elm.split(':');
                var tx = (bis.length == 3 && bis[2] != '')? bis[2]: bis[1];
                this.keyFields[bis[0]] = i;
                return {'key': bis[0], 'label': tx, 'filter': i < 4, 'column': true};
            });
            this.applyOptionsFactory();
            this.makeFiltersFactory();
            this.loadData();
        },
        loadData: function(){
            var ruta = root_path + 'users/admin/reader';
            this.params = new FormData();
            this.params.append('coleccion', this.addBambu('coleccion', this.lc_coleccion, true));
            this.params.append('pagina', this.addBambu('pagina', this.pagina, false));
            this.extractData();
            var calcmode = this.isChangeBambu()? 'on': 'off';
            console.log(`Calcmode: ${calcmode}`);
            this.params.append('calcpages', calcmode);
            if(this.status != 'build') this.status = 'loading';
            axios.post(ruta, this.params).then(res => {
                this.registros = res.data.datos;
                this.buildPagination(res.data.calculado, res.data.paginas, res.data.pagina_actual, res.data.total);
                this.status = 'loaded';
            }).catch(err => {
                this.status = 'failed';
                console.log(err);
            });
        },
        buildPagination: function(calc, pgs, pg, total){
            if(calc == 'yes'){
                this.paginas = pgs;
                this.pagina = pg;
                this.total = total;
                this.lim_a = 1;
                this.lim_b = Math.min(this.pagina + 4, this.paginas);
                this.rango = this.filled(this.lim_a, this.lim_b);
            }
        },
        applyOptionsFactory: function(){
            if(localStorage.getItem(this.memory) != null){
                var tmp = localStorage.getItem(this.memory);
                this.allFields.forEach(elm => elm.column = false);
                tmp.split(',').forEach(elm => {
                    if(this.keyFields[elm] != undefined && this.allFields[this.keyFields[elm]].key == elm){
                        this.allFields[this.keyFields[elm]].column = true;
                    }
                });
            }else if(this.only != 'no-apply'){
                this.allFields.forEach(elm => elm.column = false);
                this.only.split(',').forEach(elm => {
                    if(this.keyFields[elm] != undefined && this.allFields[this.keyFields[elm]].key == elm){
                        this.allFields[this.keyFields[elm]].column = true;
                    }
                });
            }else if(this.exclude != 'no-apply'){
                this.allFields.forEach(elm => elm.column = true);
                this.exclude.split(',').forEach(elm => {
                    if(this.keyFields[elm] != undefined && this.allFields[this.keyFields[elm]].key == elm){
                        this.allFields[this.keyFields[elm]].column = false;
                    }
                });
            }
            this.refreshColumns();
        },
        getRango: function(){
            var a = Math.min(Math.max(this.pagina - 2, 1), this.lim_b);
            var b = Math.min(this.pagina + 4, this.paginas);
            var arr = [];
            for(a; a <= b; a++){
                arr.push(a);
            }
            return arr;
        },
        setPagina: function(num){
            if(num > 0 && num <= this.paginas){
                if(num >= this.lim_a && num <= this.lim_b){
                    // Nafen
                }else if(num == (this.lim_b + 1)){
                    this.lim_a++;
                    this.lim_b++;
                    this.rango = this.filled(this.lim_a, this.lim_b);
                }else if(num == (this.lim_a - 1)){
                    this.lim_a--;
                    this.lim_b--;
                    this.rango = this.filled(this.lim_a, this.lim_b);
                }else{
                    this.lim_a = num;
                    this.lim_b = Math.min(num + 4, this.paginas);
                    if((this.lim_b - this.lim_a) < 4){
                        this.lim_a = Math.max(1, this.lim_b - 4);
                    }
                    this.rango = this.filled(this.lim_a, this.lim_b);
                }
                this.pagina = num;
                this.loadData();
            }
        },
        filled: function(from, to){
            var arr = [];
            for(from; from <= to; from++){
                arr.push(from);
            }
            return arr;
        },
        getCountRow: function(row){
            var n = row + (100 * (this.pagina - 1));
            return this.miles(n);
        },
        refreshColumns: function(){
            this.columns = this.allFields.filter(elm => elm.column);
        }
    },
    mounted() {
        this.setCollection(this.coleccion);
    }
}
</script>
<style scoped>
    .table-custom th {font-size:.75rem; padding-left:5px; padding-right:5px}
    .table.table-bordered tbody td {padding-top:7px; padding-bottom:7px}
    .loading {opacity: 0.4}
    .fw-bold {font-weight: bold}
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .summary {font:11px Verdana}
    .fx-panel {transition: max-height .7s ease-out; overflow: hidden}
    .show-panel {max-height:94vh}
    .hide-panel {max-height:0vh}
    .nav.nav-pills > li.active {border-top:1px solid transparent}
</style>