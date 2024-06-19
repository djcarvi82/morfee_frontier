<template>
    <div>
        <div class="panel panel-default card-view border">
            <div class="panel-heading">
                <div>
                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">TÍTULO PERSONALIZADO</h6>
                    <span class="txt-dark">Periodo</span>
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <amchart-barra muestra multicolor etiquetas></amchart-barra>
                </div>
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
			datos: [],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        loadData: function(){
            let pam = {};
            this.status = this.state.LOADING;
            axios.post(this.pathdata, pam).then(res => {
                this.datos = res.data;
                this.status = this.state.LOADED;
            }).catch(err => {
                this.status = this.state.FAILED;
                console.log(err);
            });
        }
    },
    mounted() {
        // alert('some');
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
</style>