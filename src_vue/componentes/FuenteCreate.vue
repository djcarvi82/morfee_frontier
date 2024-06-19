
<template>
    <div>
        <div class="row">
            <div class="col-sm-5 col-md-5">
                <label for="" class="control-label">Nombre de la fuente de información:</label>
                <input type="text" class="form-control" v-model="f_nombre" required>
            </div>
            <div class="col-sm-3 col-md-3">
                <label for="" class="control-label">Alias:</label>
                <input type="text" class="form-control" v-model="f_alias" required v-on:keydown="filtro">
                <p class="font-10 text-success">Nombre único sin espacios</p>
            </div>
            <div class="col-sm-2 col-md-2">
                <label for="" class="control-label">&nbsp;</label>
                <div><button type="button" class="btn btn-success btn-block" :disabled="f_nombre == '' || f_alias == ''" v-on:click="saveData">Guardar</button></div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        searchpath: {type: String, default: ''},
        savepath: {type: String, default: ''},
        user: {type: String, default: ''}
    },
    data(){
        return {
            teclas: [8,9,13,37,39,46,109,189],
            f_nombre: '',
            f_alias: '',
            f_campos: [],
            box_names: [],
        }
    },
    methods: {
        loadData: function(){
            this.box_names = [];
            axios.post(this.searchpath).then(res => {
                res.data.forEach(elm => this.box_names.push(elm.alias));
            }).catch(err => {console.log(err)});
        },
        filtro: function(e){
            if(/^[A-Z]$/i.test(e.key)){
                return true;
            }else if(this.teclas.indexOf(e.keyCode) >= 0){
                if(e.keyCode == 13){
                    //this.loadData();
                }
                return true;
            }else{
                e.preventDefault();
                return false;
            }
        },
        saveData: function(){
            let clearname = this.f_nombre.replace(/(^\s+|\s+$)/g, '').replace(/\s{2,}/g, ' ')
            if(clearname != '' && this.f_alias != ''){
                if(this.box_names.indexOf(this.f_alias) == -1){
                    var info = new FormData();
                    info.append('nombre', clearname);
                    info.append('alias', this.f_alias);
                    info.append('user_id', this.user);
                    console.log('enviando');
                    axios.post(this.savepath, info).then(res => {
                        alert(res.data);
                        console.log(res.data);
                    }).catch(err => {console.log(err)});
                }else{
                    alert('Ya existe una fuente de información llamada: ' + this.f_alias);
                }
            }
        }
    },
    mounted(){
        this.loadData();
    }
}
</script>