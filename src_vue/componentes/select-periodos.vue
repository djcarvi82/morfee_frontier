<template>
    <div>
        <div class="input-group me-4">
            <select v-model="periodo" class="form-control">
                <option value="">{{ status == state.LOADING? 'Refrescando datos...': '' }}</option>
                <optgroup :label="elm.anio == 0? 'Sin periodo': (elm.anio == -1)? 'Todos los registros': elm.anio" v-for="(elm, i) in periodos" :key="i">
                    <option v-for="(mes, m) in elm.meses" :key="m" :value="mes.ym">{{ mes.tx }}</option>
                </optgroup>
            </select>
            <div class="input-group-btn">
                <button class="btn btn-success" @click="reloadPeriodos" :disabled="status == state.LOADING"><i :class="status == state.LOADING? 'fa fa-refresh fa-spin': 'fa fa-refresh'"></i></button>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        coleccion: {type: String, default: ''},
        alias: {type: String, default: ''}
    },
    data() {
        return {
            meses: {'01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril', '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto', '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'},
            periodos: [],
            periodo: '',
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    watch: {
        periodo: function(val){
            if(this.status == this.state.LOADED){
                this.$eventBus.$emit('time-select', {'periodo': this.periodo});
            }
        },
    },
    methods: {
        pad: function(arg){
            return (`0${arg}`).slice(-2);
        },
        getNow: function(){
            var tod = new Date();
            return tod.getFullYear() + '-' + this.pad(tod.getMonth() + 1) + '-' + this.pad(tod.getDate());
        },
        miles: function(snum){
            var tm = new String(snum);
            return tm.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        loadPeriodos: function(){
            if(this.status != this.state.LOADING){
                var pam = new FormData();
                pam.append('tema', this.coleccion);
                pam.append('action', 'group:crx:1');
                this.status = this.state.LOADING;
                axios.post(root_path + 'reservas/mng/group', pam).then(res => {
                    let tmp = {};
                    let zero = null;
                    let sum = 0;
                    res.data.forEach(elm => {
                        if(elm._id == null){
                            zero = {'anio': 0, 'meses': [{'ym': 0, 'mm': 0, 'tx': 'Sin periodo definido', 'total': elm.total}]};
                        }else{
                            var anio = parseInt(elm._id.toString().slice(0, 4));
                            if(tmp[anio] == undefined){
                                tmp[anio] = {'anio': anio, 'meses': []}
                            }
                            var mes = elm._id.toString().slice(-2);
                            tmp[anio].meses.push({'ym': elm._id, 'mm': mes, 'tx': this.meses[mes], 'total': elm.total});
                        }
                        sum += elm.total;
                    });
                    this.periodos = Object.values(tmp).sort((a, b) => b.anio - a.anio);
                    if(zero != null) this.periodos.push(zero);
                    if(this.periodos.length > 1) this.periodos.push({'anio': -1, 'meses': [{'ym': -1, 'mm': 0, 'tx': 'Total registros', 'total': sum}]});
                    this.status = this.state.LOADED;
                    if(this.periodos.length > 0){
                        this.timeSelect(this.periodos[0].meses[0].ym);
                    }
                    localStorage.setItem(this.alias, JSON.stringify({'data': this.periodos, 'current': this.periodo, 'update': this.getNow()}));
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        loadPeriodosAlt: function(){
            if(this.status != this.state.LOADING){
                var pam = new FormData();
                pam.append('tema', this.coleccion);
                pam.append('campo', 'crx');
                this.status = this.state.LOADING;
                this.timeSelect('');
                axios.post(root_path + 'reservas/mng/distinct', pam).then(res => {
                    let tmp = {};
                    let zero = null;
                    let last = 0;
                    console.log('marquilla');
                    console.log(res.data);
                    res.data.forEach(elm => {
                        if(elm == null){
                            zero = {'anio': 0, 'meses': [{'ym': 0, 'mm': 0, 'tx': 'Sin periodo definido'}]};
                        }else{
                            let anio = parseInt(elm.toString().slice(0, 4));
                            let mes = elm.toString().slice(-2);
                            if(tmp[anio] == undefined) tmp[anio] = {'anio': anio, 'meses': []}
                            tmp[anio].meses.push({'ym': elm, 'mm': mes, 'tx': this.meses[mes]});
                        }
                        last = elm;
                    });
                    this.periodos = Object.values(tmp).sort((a, b) => b.anio - a.anio);
                    if(zero != null) this.periodos.push(zero);
                    // if(this.periodos.length > 1) this.periodos.push({'anio': -1, 'meses': [{'ym': -1, 'mm': 0, 'tx': 'Total registros'}]});
                    this.timeSelect(last);
                    this.$eventBus.$emit('time-refresh', {'periodo': this.periodo});
                    this.status = this.state.LOADED;
                    localStorage.setItem(this.alias, JSON.stringify({'data': this.periodos, 'current': this.periodo, 'update': this.getNow()}));
                }).catch(err => {
                    console.log(err);
                    this.status = this.state.FAILED;
                });
            }
        },
        reloadPeriodos: function(){
            this.loadPeriodosAlt();
        },
        timeSelect: function(per){
            this.periodo = per;
        },
        getHistory: function(){
            // {'data': [], current: 2022204, update: 'y-m-d', total: 0}
            if(this.alias != ''){
                var tmp = localStorage.getItem(this.alias);
                if(tmp == null){
                    this.loadPeriodosAlt();
                }else{
                    var result = JSON.parse(tmp);
                    this.periodos = result.data;
                    this.status = this.state.LOADED;
                    if(this.periodos.length > 0){
                        // this.timeSelect(this.periodos[0].meses[0].ym);
                        this.timeSelect(this.periodos.at(-1).meses.at(-1).ym);
                    }
                }
            }
        }
    },
    mounted() {
        this.getHistory();
    }
}
</script>
<style scoped>
.slot {cursor:pointer}
.slot.active, .slot:hover {background:#F0C54144}
.slot + .slot {border-top:1px solid #DEDEDE}
.bg-super {background: #F0C541 !important; color:#FFF; font-weight: bold; font-family: Arial; letter-spacing: 1px}
</style>