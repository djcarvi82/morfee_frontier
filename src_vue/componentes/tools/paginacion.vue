<template>
    <div>
        <div class="pull-left">
            <div class="btn-group mr-15">
                <a v-on:click="clickPage('first')" :class="has_previous? 'btn btn-default btn-outline page-link': 'btn btn-default btn-outline page-link disabled'" href="javascript:void(0)">Primera</a>
            </div>
            <div class="btn-group">
                <a v-on:click="clickPage('previous')" :class="has_previous? 'btn btn-default btn-outline page-link': 'btn btn-default btn-outline page-link disabled'" href="javascript:void(0)"><i class="fa fa-chevron-left"></i></a>

                <a v-for="(pg, i) in rango" :key="i" :class="(pg == lc_number)? 'btn btn-success page-link': 'btn btn-default btn-outline page-link'" href="javascript:void(0)" v-on:click="clickPage(pg)">{{ pg }}</a>

                <a v-if="lc_number < num_pages" v-on:click="clickPage('next')" :class="has_next? 'btn btn-default btn-outline page-link': 'btn btn-default btn-outline page-link disabled'" href="javascript:void(0)"><i class="fa fa-chevron-right"></i></a>
            </div>
            <div class="btn-group ml-15" v-if="lc_number < num_pages">
                <a v-on:click="clickPage('last')" :class="has_next? 'btn btn-default btn-outline page-link': 'btn btn-default btn-outline page-link disabled'" href="javascript:void(0)">Última {{ num_pages }}</a>
            </div>
        </div>
        <div class="pull-right" v-if="!sintotal">
            <div style="padding-top:10px; padding-bottom:10px"><b>{{ formatMiles(total) }}</b> REGISTROS</div>
        </div>
        <div class="clearfix"></div>
    </div>
</template>
<script>
export default {
    props: {
        url_main: {type: String, default: 'none'},
        url_count: {type: String, default: 'none'},
        sintotal: {type: Boolean, default: false}
    },
    data(){
        return {
            lc_number: 1,
            slicePages: 10,
            pagination: 50,
            salto: 0,
            total: 0,
            num_pages: 1,
            has_previous: false,
            has_next: false,
            rango: [],
            isLoad: false,
        }
    },
    methods: {
        formatMiles: function(num){
            var regla = /(\d+)(\d{3})/;
            var tmp = String(num);
            while(regla.test(tmp)){
                tmp = tmp.replace(regla, '$1' + ',' + '$2');
            }
            return tmp;
        },
        buildRange: function(ignitio = 1){
            this.lc_number = ignitio;
            var from = (this.lc_number > (this.num_pages - this.slicePages))? Math.max(1, (this.num_pages - this.slicePages) + 1): this.lc_number;
            var to = (this.lc_number > (this.num_pages - this.slicePages))? this.num_pages + 1: Math.min(this.lc_number + this.slicePages, this.num_pages + 1);
            this.rango = [];
            for(var i = from; i < to; i++){
                this.rango.push(i);
            }
            return this.setPage(this.lc_number);
        },
        setTotal: function(arg){
            this.total = parseInt(arg);
            this.num_pages = Math.ceil(this.total / this.pagination);
            this.buildRange();
        },
        clickPage: function(page){
            var pass = false;
            if('previous' == page){
                pass = this.previousPage();
            }else if('next' == page){
                pass = this.nextPage();
            }else if('first' == page){
                pass = this.buildRange(1);
            }else if('last' == page){
                pass = this.buildRange(this.num_pages);
            }else{
                pass = this.setPage(page);
            }

            if(pass){
                this.$eventBus.$emit('mf-select-page', this.lc_number);
            }
        },
        setPage: function(page, dispatch = true){
            if(page <= this.num_pages){
                this.lc_number = page;
                this.has_previous = (this.lc_number > 1)? true: false;
                this.has_next = (this.lc_number < this.num_pages)? true: false;
                return true;
            }else{
                return false;
            }
        },
        previousPage: function(){
            var newpage = Math.max(1, this.lc_number - 1);
            if(this.setPage(newpage)){
                if(this.rango[0] == (this.lc_number + 1)){
                    this.rango.pop();
                    this.rango.unshift(this.lc_number);
                }
                return true;
            }else{
                return false;
            }
        },
        nextPage: function(){
            var newpage = this.lc_number + 1;
            if(this.setPage(newpage)){
                if(this.rango[this.rango.length - 1] == (this.lc_number - 1)){
                    this.rango.shift();
                    this.rango.push(this.lc_number);
                }
                return true;
            }else{
                return false;
            }
        },
        listen: function(){
            //Here listen code
        }
    },
    mounted(){
        this.listen();
        this.setTotal(1340);
        //alert('urias');
    }
}
</script>
<style scoped>
    .btn-group > .btn {padding-left: 1rem; padding-right: 1rem !important; min-width:54px}
</style>