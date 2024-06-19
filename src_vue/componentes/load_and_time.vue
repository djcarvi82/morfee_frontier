<template>
    <div>
        <div class="input-group me-4" v-if="clock != null">
            <div class="input-group-addon" style="background:#FFF">
                <i class="icon-clock"></i>
            </div>
            <input type="text" class="form-control" :value="clock_human">
        </div>
    </div>
</template>
<script>
export default {
    props: {
        pathsearch: {type: String, default: ''},
    },
    data() {
        return {
            keycode: '',
            clock: null,
            clock_human: '',
            seg: 0,
            runsearch: false,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        clock_up: function(){
            if(this.clock != null){
                clearInterval(this.clock);
                this.clock = null;
            }
            this.seg = 0;
            this.clock = setInterval(() => {
                this.seg++;
                this.clock_human = this.getTime();
            }, 1000);
        },
        clock_down: function(){
            if(this.clock != null){
                clearInterval(this.clock);
            }
            this.clock = null;
            this.seg = 0;
        },
        getTime: function(){
            let mn = Math.floor(this.seg / 60).toString().padStart(2, '0');
            let rs = (this.seg % 60).toString().padStart(2, '0');
            return `${mn}:${rs} segundos`
        },
        getTimestamp: function(){
            return (new Date()).toString().slice(11, 24);
        },
        makeToken: function(){
            let str = '';
            for(var i = 0; i < 5; i++){
                let num = Math.round(Math.random() * 25 + 65);
                str += String.fromCharCode(num);
            }
            str += Math.round(Math.random() * 999 + 1000);
            return str;
        },
        getFormdata: function(params, extra=null){
            let param = new FormData();
            Object.entries(params).forEach(par => param.append(par[0], par[1]));
            if(extra != null){
                Object.entries(extra).forEach(par => param.append(par[0], par[1]));
            }
            return param;
        },
        loadData: function(consulta, origen, writepath, params, force){
            console.log('La consulta es: ' + consulta);
            console.log('Origen: ' + origen);
            this.asyncRequest(
                consulta, // cliente_try_aut_ymd | cliente_try_fac_ymd | cliente_try_pag_ymd
                origen,
                writepath,
                params,
                true,   // first param
                '',     // kcode param
                force   // force param
            );
        },
        verifyWrite: function(clave, consulta){
            let pam = new FormData();
            pam.append('clave', kcode);
            pam.append('consulta', consulta);
            axios.post(this.pathsearch, pam).then(res => {
                if(res.data.estado == 'close'){
                    console.log(`Consulta finalizada, con clave: '${kcode}'`);
                    console.log(res.data);
                    this.$eventBus.$emit('end-load', {'origen': origen, 'contenido': res.data.contenido})
                    this.runsearch = false;
                    this.status = this.state.LOADED;
                    this.clock_down();
                }
            }).catch(err => {
                console.log(err);
            });
        },
        asyncRequest: function(consulta, origen, writepath, params, first=true, kcode='', force=false){
            let initial = first;
            if(this.runsearch == false || first == false){
                if(this.runsearch == false && first){
                    this.runsearch = true;
                    this.status = this.state.LOADING;
                    this.clock_up();
                    console.log('Se inicia proceso de asyncRequest!');
                }
                if(force === true){
                    console.log('Se mandó a crear la consulta mongodb por la fuerza, con la clave: ' + this.keycode);
                    this.keycode = generatorKey();
                    let fdata = this.getFormdata(params, {'consulta': consulta, 'clave': this.keycode});
                    customPostBlind(writepath, fdata).then(arg => {console.log('Return async write request! (CustomPost)')}).catch(err => {console.log(err)});
                    setTimeout(() => this.asyncRequest(consulta, origen, writepath, params, false, this.keycode, false), 4000);
                    // axios.post(writepath, param).then(arg => {console.log('Return async write request!')}).catch(err => {console.log(err)});
                }else{
                    let pam = this.getFormdata({'consulta': consulta, 'clave': kcode});
                    axios.post(this.pathsearch, pam).then(res => {
                        if(res.data.estado == 'void'){
                            if(initial){
                                this.keycode = generatorKey();
                                let fdata = this.getFormdata(params, {'consulta': consulta, 'clave': this.keycode});
                                customPostBlind(writepath, fdata).then(arg => {console.log('Return async write request! (CustomPost)')}).catch(err => {console.log(err)});
                                setTimeout(() => this.asyncRequest(consulta, origen, writepath, params, false, this.keycode, false), 4000);
                                // axios.post(writepath, param).then(arg => {console.log('Return async write request!')}).catch(err => {console.log(err)});
                                console.log('Se mandó a crear la consulta mongodb porque se encontró void, con la clave: ' + this.keycode);
                            }
                        }else if(res.data.estado == 'close'){
                            console.log(`Consulta finalizada, con clave: '${kcode}'`);
                            console.log(res.data);
                            this.$eventBus.$emit('end-load', {'origen': origen, 'contenido': res.data.contenido})
                            this.runsearch = false;
                            this.status = this.state.LOADED;
                            this.clock_down();
                        }else if(res.data.estado == 'failed'){
                            console.log(`La creación de consulta mongo falló, con clave: '${kcode}'`);
                            this.runsearch = false;
                            this.status = this.state.FAILED;
                            this.clock_down();
                        }else{
                            console.log(`El estado de la consulta es: '${res.data.estado}', se verifica dentro de 4 segundos!`);
                            setTimeout(() => this.asyncRequest(consulta, origen, writepath, {}, false, kcode), 4000);
                        }
                    }).catch(err => {
                        console.log(err);
                        console.log(`asyncRequest falló, se verifica dentro de 4 segundos!`);
                        setTimeout(() => this.asyncRequest(consulta, origen, writepath, {}, false, kcode, false), 4000);
                    });
                }
            }else{
                console.log('Se desechó la invocación de asyncRequest, porque ya hay un hilo ejecutándose!');
            }
        },        
    },
    mounted() {
        // alert('daniel');
    }
}
</script>