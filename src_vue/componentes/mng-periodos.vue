<template>
    <div>
        <div class="d-flex align-items-center px-3 pt-0 pb-3" v-if="status == state.LOADING"><i class="fa fa-spin fa-spinner me-2 fs-4"></i> Refrescando datos...</div>
        <div v-else>
            <div v-for="(elm, i) in periodos" :key="i">
                <div class="py-0 px-3 bg-super">{{ (elm.anio == 0)? 'Sin periodo': (elm.anio == -1)? 'Todos los registros': elm.anio }}</div>
                <div :class="periodo == mes.ym? 'py-2 px-3 slot txt-dark active': 'py-2 px-3 slot txt-dark'" v-for="(mes, m) in elm.meses" :key="m" v-on:click="timeSelect(mes.ym, mes.total)">
                    <div class="d-flex justify-content-between align-items-center">
                        <span>{{ mes.tx }}</span><span :class="periodo == mes.ym? 'label label-primary': 'label label-default'">{{ miles(mes.total) }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="py-2 px-2 border-top">
            <button class="btn btn-success btn-block btn-xs" v-on:click="reloadPeriodos()" :disabled="status == state.LOADING"><i class="fa fa-refresh me-2"></i>Refrescar</button>
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
            periodo: 0,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
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
                    this.timeSelect(this.periodos[0].meses[0].ym, this.periodos[0].meses[0].total);
                }
                localStorage.setItem(this.alias, JSON.stringify({'data': this.periodos, 'current': this.periodo, 'update': this.getNow()}));
            }).catch(err => {
                console.log(err);
                this.status = this.state.FAILED;
            });
        },
        reloadPeriodos: function(){
            this.$eventBus.$emit('time-refresh', true);
            this.loadPeriodos();
        },
        timeSelect: function(per, total){
            this.periodo = per;
            this.$eventBus.$emit('time-select', {'periodo': this.periodo, 'total': total});
        },
        getHistory: function(){
            // {'data': [], current: 2022204, update: 'y-m-d', total: 0}
            if(this.alias != ''){
                var tmp = localStorage.getItem(this.alias);
                if(tmp == null){
                    this.loadPeriodos();
                }else{
                    var result = JSON.parse(tmp);
                    this.periodos = result.data;
                    this.status = this.state.LOADED;
                    if(this.periodos.length > 0){
                        this.timeSelect(this.periodos[0].meses[0].ym, this.periodos[0].meses[0].total);
                    }
                }
            }
        }
    },
    mounted() {
        // console.log('Mounted mng-periodo');
    }
}
</script>
<style scoped>
.slot {cursor:pointer}
.slot.active, .slot:hover {background:#F0C54144}
.slot + .slot {border-top:1px solid #DEDEDE}
.bg-super {background: #F0C541 !important; color:#FFF; font-weight: bold; font-family: Arial; letter-spacing: 1px}
</style>