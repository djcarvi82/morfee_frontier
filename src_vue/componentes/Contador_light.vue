<template>
    <div class="panel panel-default card-view border py-0 px-4">
        <div class="panel-wrapper collapse in">
            <div class="panel-body pt-4 pb-3 vega">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="x1">
                        <div class="fs-4 titulo">
                            <span class="block" :style="{'font-size': fontsize}" v-if="lc_loading">0</span>
                            <span class="block counter" :style="{'font-size': fontsize}" v-else-if="isRun">
                                <span v-for="(dig, ind) in digitos" :key="ind" :class="dig.clase">{{ dig.text }}</span>
                            </span>
                            <span :class="errorMode? 'txt-danger block counter': 'txt-dark block counter'" :style="{'font-size': fontsize}" v-else>{{ pretag + lc_valor }}</span>
                        </div>
                        <div class="subtitulo uppercase-font block">{{ lc_texto }}</div>
                    </div>
                    <div class="x2">
                        <i class="fa fa-spin fa-spinner txt-light-grey fs-1" v-if="lc_loading"></i>
                        <i :class="errorMode? css_err.join(' '): estilos" v-else></i>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        texto: {type: String, default: 'Texto por defecto'},
        valor: {type: String, default: ''},
        icono: {type: String, default: 'icon-layers'},
        duracion: {type: String, default: '3'},
        stack: {type: Boolean, default: false},
        capturarevento: {type: String, default: 'none'},
        loading: {type: Boolean, default: false},
        miles: {type: Boolean, default: false},
        canal: {type: String, default: ''},
        pretag: {type: String, default: ''},
        fontsize: {type: String, default: '24px'},
        warning: {type: Boolean, default: false}
    },
    data() {
        return {
            _duracion: 0,
            iteration: 0,
            intervalId: null,
            lc_valor: '',
            lc_texto: '',
            // css: ['icon-layers', 'data-right-rep-icon', 'txt-light-grey'],
            css: ['icon-layers', 'txt-light-grey', 'fs-1'],
            css_err: ['fa fa-warning', 'fs-1', 'has-error'],
            estilos: '',

            largo: 0,
            digitos: [],
            rawdata: [],
            isRun: false,
            lc_loading: false,
            errorMode: false,
        }
    },
    methods: {
        formatMiles: function(num){
            var regla = /(\d+)(\d{3})/;
            var tmp = String(num);
            if(/\d+\.\d+/.test(tmp)){
                var bis = tmp.split('.');
                var base = String(bis[0]);
                var resto = bis[1];
                while(regla.test(base)){
                    base = base.replace(regla, '$1' + ',' + '$2');
                }
                return base + '.' + resto;
            }else{
                while(regla.test(tmp)){
                    tmp = tmp.replace(regla, '$1' + ',' + '$2');
                }
                return tmp;
            }
        },
        setValor: function(num){
            this.lc_loading = false;
            this.resetData();
            this.lc_valor = String(num);
            if(this.warning){
                this.errorMode = (parseFloat(num) == 0)? false: true;
            }
            if(this.miles) this.lc_valor = this.formatMiles(this.lc_valor);
            this.rawdata = this.lc_valor.split('');
            this.largo = /[0-9]{1}/g.test(this.lc_valor)? this.lc_valor.match(/[0-9]{1}/g).length: 0;
            var intervalo = this._duracion / this.largo;
            if(intervalo <= 0 || intervalo == null) intervalo = 1 * this._duracion;

            this.isRun = true;
            this.extractDigito();
            this.intervalId = window.setInterval(() => {
                if(this.rawdata.length > 0){
                    while(this.extractDigito()){
                        //Empty block
                    }
                }else{
                    window.clearInterval(this.intervalId);
                    this.isRun = false;
                }
            }, intervalo);
        },
        setTexto: function(tx){
            this.lc_texto = tx;
        },
        setIcono: function(arg){
            this.css[0] = arg;
            this.estilos = this.css.join(' ');
        },
        extractDigito: function(){
            if(this.rawdata.length > 0){
                var num = this.rawdata.pop();
                if(/^\d+$/.test(num)){
                    var clase = ((this.iteration++ % 2) == 0)? 'digito': 'digito_desc';
                    //if(!this.stack && this.digitos.length > 0) this.digitos[0].clase = '';
                    this.digitos.unshift({'clase': clase, 'text': '', 'valor': num});
                    return false;
                }else{
                    this.digitos.unshift({'clase': '', 'text': num, 'valor': num});
                    return true;
                }
            }else{
                return false;
            }
        },
        resetData: function(){
            if(this.isRun){
                 window.clearInterval(this.intervalId);
                 this.isRun = false;
            }
            this.digitos = [];
            this.iteration = 0;
        },
        listen: function(){
            if(this.capturarevento != 'none'){
                this.$eventBus.$on(this.capturarevento, arg => {
                    this.setTexto(arg[arg.campo_categoria]);
                    this.setValor(arg[arg.campo_valor]);
                });
            }
        }
    },
    mounted() {
        this._duracion = parseInt(this.duracion) * 1000;
        this.lc_loading = this.loading;
        if(this.canal != '') this.css.push(this.canal);
        this.setTexto(this.texto);
        if(!this.loading) this.setValor(this.valor);
        this.setIcono(this.icono);
        this.listen();
    }
}
</script>
<style scoped>
    @property --num {
        syntax: "<integer>";
        initial-value: 0;
        inherits: false;
    }
    @keyframes contador {
        from {--num: 0}
        to {--num: 9}
    }
    .digito {animation: contador .3s linear infinite; counter-reset: num var(--num)}
    .digito_desc {animation: contador .3s linear infinite reverse; counter-reset: num var(--num)}
    .digito::after, .digito_desc::after {content: counter(num)}
    .titulo {line-height:1; color:#000}
    .subtitulo {font-size: .85rem; letter-spacing: 1px; font-weight: 100 !important}
    @keyframes efecto {
        0% {color:#EEEEEE}
        70% {color:#CC0000}
        100% {color:#EEEEEE}
    }
    .has-error {
        animation-name: efecto;
        animation-duration: 1.2s;
        animation-iteration-count: infinite;
    }
</style>