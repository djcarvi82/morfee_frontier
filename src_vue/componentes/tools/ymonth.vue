<template>
    <div>
        <div :class="(meses == 'on')? 'input-group mb-10': 'input-group'">
            <span class="input-group-btn">
                <button type="button" class="btn btn-square btn-default" v-on:click="remYear()"><i class="fa fa-chevron-left"></i></button>
            </span>
            <input type="text" class="form-control text-center" readonly v-model="anio">
            <span class="input-group-btn">
                <button type="button" class="btn btn-square btn-default" v-on:click="addYear()" :disabled="anio == limite"><i class="fa fa-chevron-right"></i></button>
            </span>
        </div>
        <div :class="vertical? 'btn-group btn-group-vertical btn-block': 'btn-group btn-group-justified'" v-if="meses == 'on'">
            <div :class="getClass(i)" v-for="(m, i) in getMonthArray()" :key="i" v-on:click="changeMonth(i)" :disabled="getDisabled(i)">{{ m }}</div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        vertical: {type: Boolean, default: false},
        meses: {type: String, default: 'on'},
        futuro: {type: String, default: 'normal'},
        manual: {type: Boolean, default: false},
        predata: {type: String, default: ''}
    },
    data(){
        return {
            limite: 0,
            limonth: 0,
            anio: 0,
            mes: 0,
            lc_meses: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            mesesMin: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            info: [false, false, false, false, false, false, false, false, false, false, false, false, false],
            isRun: false
        }
    },
    methods: {
        getDisabled: function(indice){
            return (this.futuro == 'disabled')? (this.anio == this.limite && ++indice > this.limonth): false;
        },
        getClass: function(indice){
            var kix = indice + 1;
            if(this.mes == kix){
                return 'btn btn-success';
            }else{
                return this.info[kix]? 'btn btn-warning': 'btn btn-default btn-outline';
            }
        },
        getMonthArray: function(){
            return this.vertical? this.lc_meses: this.mesesMin;
        },
        addYear: function(){
            if(this.anio < this.limite){
                this.anio++;
                this.mes = 0;
                this.setPredata([]);
                this.dispatchDate('year');
            }
        },
        remYear: function(){
            this.anio--;
            this.mes = 0;
            this.setPredata([]);
            this.dispatchDate('year');
        },
        changeMonth: function(indice){
            if(this.getDisabled(indice) == false){
                this.mes = indice + 1;
                this.dispatchDate('month');
            }
        },
        dispatchDate: function(arg){
            this.$eventBus.$emit('mf-change-date', this.getDate(arg));
        },
        getDate: function(ch = 'none'){
            var kmes = (this.mes < 10)? '0' + this.mes: this.mes;
            var code = this.anio + '' + kmes;
            var txmes = (this.mes > 0)? this.lc_meses[this.mes - 1]: '';
            return {'year': this.anio, 'month': this.mes, 'periodo': code, 'txmes': txmes, 'change': ch};
        },
        setPredata: function(arr, cls = true){
            var tmp = 0;
            if(cls) this.info.forEach((arg, i) => this.info[i] = false);
            arr.forEach(elm => {
                tmp = (elm.toString().length > 2)? parseInt(elm.toString().substr(-2)): parseInt(elm);
                if(tmp > 0 && tmp < 13){
                    this.info[tmp] = true;
                }
            });
            this.$forceUpdate();
        }
    },
    mounted(){
        console.log('Is caja-component is mounted!');
        var time = new Date();
        this.limite = time.getFullYear();
        this.anio = this.limite;
        this.limonth = time.getMonth() + 1;
        if(!this.manual){
            this.mes = this.limonth;
        }
        if(this.predata != ''){
            this.setPredata(this.predata.split(','));
        }
    }
}
</script>
<style scoped>
    input.form-control[readonly] {background:#FFF}
    .downborde {border-bottom:none !important}
    .btn-warning + .btn-warning {border-left-color:#F9EBBD}
</style>