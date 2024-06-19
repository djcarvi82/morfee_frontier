<template>
    <div>
        <table :class="css_table" v-if="counter">
            <thead>
                <tr>
                    <th class="colmin">No.</th>
                    <th v-for="(elm, i) in columns" :key="i" :class="i > 0? 'colmin px-4': ''">{{ elm.alias }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, r) in registros" :key="r">
                    <td class="text-center">{{ r + 1 }}</td>
                    <td v-for="(elm, e) in columns" :key="e" :class="isNumeric(row[elm.field])? 'text-right colmin px-3': ''">{{ elm.pretag + getValue(row[elm.field]) }}</td>
                </tr>
                <tr v-if="sumar != ''" class="txt-dark">
                    <th :colspan="columns.length">Total</th><th class="colmin px-3">{{ getPretag() + miles(total) }}</th>
                </tr>
            </tbody>
        </table>
        <table :class="css_table" v-else>
            <thead>
                <tr>
                    <th v-for="(elm, i) in columns" :key="i" :class="i > 0? 'colmin px-4': ''">{{ elm.alias }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(row, r) in registros" :key="r">
                    <td v-for="(elm, e) in columns" :key="e" :class="isNumeric(row[elm.field])? 'text-right colmin px-3': ''">{{ elm.pretag + getValue(row[elm.field]) }}</td>
                </tr>
                <tr v-if="sumar != ''" class="txt-dark text-bold">
                    <th :colspan="columns.length - 1">Total</th><th class="colmin px-3">{{ getPretag() + miles(total) }}</th>
                </tr>
            </tbody>
        </table>
    </div>
</template>
<script>
export default {
    props: {
        cols: {type: String, default: 'void'},
        border: {type: Boolean, default: false},
        striped: {type: Boolean, default: false},
        compact: {type: Boolean, default: false},
        counter: {type: Boolean, default: false},
        hover: {type: Boolean, default: false},
        lastcenter: {type: Boolean, default: false}, 
        lastright: {type: Boolean, default: false},
        sumar: {type: String, default: ''},
    },
    data() {
        return {
            css_table: 'my-0 table',
            columns: [],
            registros: [],
            total: 0,
        }
    },
    methods: {
        miles: function(snum){
            var tm = new String(snum);
            return tm.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        },
        setDatos: function(arr){
            this.registros = arr;
            if(this.sumar != ''){
                this.total = 0;
                this.registros.forEach(elm => this.total += elm[this.sumar]);
            }
            if(this.cols == 'void' && this.registros.length > 0){
                this.columns = Object.entries(this.registros[0]).map(elm => {
                    return {'field': elm[0], 'alias': elm[0]};
                });
            }
        },
        getValue: function(arg){
            if(this.isNumeric(arg)){
                if(arg % 1 == 0){
                    return this.miles(arg);
                }else{
                    let nx = parseFloat(arg).toFixed(2);
                    return this.miles(nx);
                }
            }else{
                return arg;
            }
        },
        isNumeric: function(arg){
            return /^(\d+|\d+\.\d+)$/.test(arg.toString())? true: false;
        },
        getPretag: function(){
            let tmp = this.columns.find(elm => elm.field == this.sumar);
            return (tmp == undefined)? '': tmp.pretag;
        }
    },
    mounted() {
        if(this.border) this.css_table += ' table-bordered';
        if(this.striped) this.css_table += ' table-striped';
        if(this.hover) this.css_table += ' table-hover';
        if(this.compact) this.css_table += ' table-compact';
        if(this.lastcenter) this.css_table += ' table-center';
        if(this.lastright) this.css_table += ' table-right';
        if(this.cols != 'void'){
            this.columns = this.cols.split(',').map(elm => {
                var bi = elm.split(':');
                return {'field': bi[0], 'alias': bi[1] ?? bi[0], 'pretag': bi[2] ?? ''};
            });
        }
    }
}
</script>
<style scoped>
.table.table-compact th {padding-bottom: .5rem}
.table.table-compact td {padding-top:.4rem; padding-bottom: .4rem}
.table.table-center th:last-child, .table.table-center td:last-child {text-align: center}
.table.table-right th:last-child, .table.table-right td:last-child {text-align: right}
.colmin {width: 1%; white-space: nowrap; text-align: center}
</style>