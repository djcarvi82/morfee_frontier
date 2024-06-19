<template>
    <div>
        <div class="table-wrap" v-if="registros.length > 0">
            <div class="table-responsive">
                <table class="table display table-striped table-borderedx table-hover table-sm mb-0">
                    <thead>
                        <tr>
                            <th class="colmin text-center">No.</th>
                            <th>Fecha de importación</th>
                            <th>Base de datos</th>
                            <th class="text-center">Registros importados</th>
                            <th class="text-center">Código de importación</th>
                            <th class="colmin text-center">Acción</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(reg, i) in registros" :key="i">
                            <td class="colmin text-center">{{ (i + 1) * pagina }}</td>
                            <td>{{ reg.created_at }}</td>
                            <td>{{ dbname }}</td>
                            <td class="text-center">{{ formatMiles(reg.total) }}</td>
                            <td class="text-center">CTR-{{ reg.id }}</td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center mx-4">
                                    <a href="javascript:void(0)" class="me-4 d-none" data-toggle="tooltip" data-original-title="Datos" disabled><i class="fa fa-list-alt"></i></a>
                                    <a href="javascript:void(0)" data-toggle="tooltip" data-original-title="Eliminar" v-on:click="preDelete(reg.id)"><i class="fa fa-close text-danger"></i></a>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div><!-- End table-wrap -->
        <div class="bg-light-warning border border-warning txt-dark px-3 py-3" v-else>
            <div class="d-flex align-items-center">
                <i class="fa fa-warning fs-3 me-3 txt-warning"></i>
                <div>Esta base de datos no tiene registros!</div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        coleccion: {type: String, default: ''},
        titulo: {type: String, default: ''},
    },
    data() {
        return {
            registros: [],
            diccionario: [],
            rawdict: null,
            dbname: '',
            pagina: 1,
        }
    },
    methods: {
        setConfig: function(){
            this.dbname = this.titulo;
            this.loadData();
        },
        loadInfo: function(){
            let ruta = root_path + 'users/admin/diccionario/' + this.coleccion + '/';
            axios.get(ruta).then(res => {
                this.rawdict = res.data;
                this.diccionario = this.rawdict.campos.split('|').map(elm => {
                    var tmp = elm.split(':');
                    return {'ref': tmp[0], 'label': tmp[1]};
                });
                this.dbname = this.rawdict.alias;
                this.loadData();
            }).catch(err => {console.log(err)});
        },
        loadData: function(){
            var ruta = root_path + 'users/admin/history/import';
            var param = new FormData();
            param.append('coleccion', this.coleccion);
            axios.post(ruta, param).then(res => {
                this.registros = res.data;
                console.log('Load list import!');
            }).catch(err => {console.log(err)});
        },
        preDelete: function(cid){
            swal({
                title: "¿Está seguro?",
                text: "Confirma que procederá a eliminar todos los registros que hacen parte de esta importación?",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#f0c541",
                confirmButtonText: "Eliminar",
                cancelButtonText: "Cancelar",
                closeOnConfirm: true
            }, () => this.secureDelete(cid));
        },
        secureDelete: function(cx){
            var ruta = root_path + 'users/admin/basic/import/remove';
            let params = new FormData();
            params.append('codex', cx);
            params.append('coleccion', this.coleccion);
            axios.post(ruta, params).then(res => {
                if(res.data.status == 'success'){
                    this.loadData();
                }
            }).catch(err => {console.log(err)});
        },
        formatMiles: function(num){
            var regla = /(\d+)(\d{3})/;
            var tmp = String(num);
            while(regla.test(tmp)){
                tmp = tmp.replace(regla, '$1' + ',' + '$2');
            }
            return tmp;
        },
        listen: function(){
            this.$eventBus.$on('import-success', arg => {
                if(arg == this.coleccion){
                    this.loadData();
                }
            });
        }
    },
    mounted() {
        if(this.titulo == ''){
            this.loadInfo();
        }else{
            this.setConfig();
        }
        this.listen();
    }
}
</script>
