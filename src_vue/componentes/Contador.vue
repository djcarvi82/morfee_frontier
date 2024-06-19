<template>
    <div class="panel panel-default card-view pa-0">
        <div class="panel-wrapper collapse in">
            <div class="panel-body pa-0">
                <div class="sm-data-box">
                    <div class="container-fluid ps-4 py-3">
                        <div class="row d-flex justify-content-between my-0">
                            <div class="col-xs-6 text-center px-0">
                                <span class="txt-dark block" v-if="lc_loading">
                                    <span style="font-size:24px">0</span>
                                </span>
                                <span class="txt-dark block counter" v-else-if="isRun">
                                    <span v-for="(dig, ind) in digitos" :key="ind" :class="dig.clase">{{ dig.text }}</span>
                                </span>
                                <span class="txt-dark block counter" v-else>{{ lc_valor }}</span>
                                <span class="weight-500 uppercase-font block">{{ lc_texto }}</span>
                            </div>
                            <div class="col-xs-6 text-center px-0 fs-1">
                                <i class="fa fa-spin fa-spinner data-right-rep-icon txt-light-grey" v-if="lc_loading"></i>
                                <i :class="estilos" v-else></i>
                            </div>
                        </div>	
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
        loading: {type: Boolean, default: false}
    },
    data(){
        return {
            _duracion: 0,
            iteration: 0,
            intervalId: null,
            lc_valor: '',
            lc_texto: '',
            css: ['icon-layers', 'data-right-rep-icon', 'txt-light-grey'],
            estilos: '',

            largo: 0,
            digitos: [],
            rawdata: [],
            isRun: false,
            lc_loading: false,
        }
    },
    methods: {
        setValor: function(num){
            this.lc_loading = false;
            this.resetData();
            this.lc_valor = String(num);
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
    mounted(){
        console.log('Is caja-component is mounted!');
        this._duracion = parseInt(this.duracion) * 1000;
        this.lc_loading = this.loading;
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
</style>