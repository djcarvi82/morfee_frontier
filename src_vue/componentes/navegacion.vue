<template>
    <ul class="nav navbar-nav side-nav nicescroll-bar">
        <li class="navigation-header">
            <span>Módulos</span> 
            <i class="zmdi zmdi-more"></i>
        </li>
        <li v-for="(item, indice) in rutas" :key="indice">
            <a :class="getClassMod(item.key)" href="javascript:void(0);" :data-target="'#ui_' + item.key" v-on:click="selectMod(item.key)">
                <div class="pull-left">
                    <i :class="item.icono"></i>
                    <span class="right-nav-text">{{ item.modulo }}</span>
                </div>
                <div class="pull-right">
                    <i class="zmdi zmdi-caret-down"></i>
                </div>
                <div class="clearfix"></div>
            </a>
            <ul :id="'ui_' + item.key" :class="getClassExpand(item.key)">
                <li v-for="(pag, ind) in item.pages" :key="ind">
                    <a :class="(iPage == pag.key)? 'active-page': ''" v-on:click="select(pag.key)" href="#pag.ruta">{{ pag.nombre }}</a>
                </li>
            </ul>
        </li>
    </ul>
</template>
<script>
export default {
    props: {
        texto: {type: String, default: 'Texto por defecto'},
    },
    data(){
        return {
            lc_valor: '',
            rutas: [],
            iMod: -1,
            iPage: '',
            iExpand: false,
        }
    },
    methods: {
        setValor: function(num){

        },
        config: function(){
            /*
                        {"ruta": "", "nombre": "", "active": false},
            */
            this.rutas = [
                {
                    'icono': 'zmdi zmdi-collection-plus mr-20',
                    'modulo': 'Aseguramiento', 
                    'pages': [
                        {"ruta": "{% url 'consolidado' %}", "nombre": "Consolidado"},
                        {"ruta": "{% url 'tema2' %}", "nombre": "Régimen Subsidiado"},
                        {"ruta": "{% url 'tema3' %}", "nombre": "Régimen Contributivo"},
                        {"ruta": "{% url 'tema4' %}", "nombre": "Consulta individual"},
                        {"ruta": "{% url 'caracterizacionvac' %}", "nombre": "Caracterización Vacunación"}
                    ]
                },
                {
                    'icono': 'zmdi zmdi-eyedropper mr-20',
                    'modulo': 'Salud Pública', 
                    'pages': [
                        {"ruta": "form-element.html", "nombre": "Opción 1"},
                        {"ruta": "form-layout.html", "nombre": "Opción 2"}
                    ]
                },
                {
                    'icono': 'zmdi zmdi-hotel mr-20',
                    'modulo': 'P. Servicios', 
                    'pages': [
                        {"ruta": "flot-chart.html", "nombre": "Opción 1"},
                        {"ruta": "morris-chart.html", "nombre": "Opción 2"}
                    ]
                },
                {
                    'icono': 'zmdi zmdi-shopping-cart-plus mr-20',
                    'modulo': 'CRUE', 
                    'pages': [
                        {"ruta": "flot-chart.html", "nombre": "Opción 1"},
                        {"ruta": "morris-chart.html", "nombre": "Opción 2"}
                    ]
                },
                {
                    'icono': 'zmdi zmdi-search-in-file mr-20',
                    'modulo': 'Auditoría', 
                    'pages': [
                        {"ruta": "flot-chart.html", "nombre": "Opción 1"},
                        {"ruta": "morris-chart.html", "nombre": "Opción 2"}
                    ]
                },
                {
                    'icono': 'zmdi zmdi-memory mr-20',
                    'modulo': 'S. Información', 
                    'pages': [
                        {"ruta": "flot-chart.html", "nombre": "Opción 1"},
                        {"ruta": "morris-chart.html", "nombre": "Opción 2"}
                    ]
                },
                {
                    'icono': 'zmdi zmdi-bug mr-20',
                    'modulo': 'Covid-19', 
                    'pages': [
                        {"ruta": "flot-chart.html", "nombre": "Opción 1"},
                        {"ruta": "morris-chart.html", "nombre": "Opción 2"}
                    ]
                },
            ];
            this.rutas.forEach((elm, imod) => {
                elm.key = imod;
                elm.pages.forEach((pg, ipg) => {
                    pg.key = imod + '.' + ipg;
                });
            });
        },
        getClassMod: function(arg){
            if(this.iMod === arg){
                return this.iExpand? 'active': 'active collapsed';
            }else{
                return '';
            }
        },
        coreExpand: function(arg){
            if(this.iMod === arg){
                return this.iExpand;
            }else{
                return false;
            }
        },
        getClassExpand: function(arg){
            if(this.iMod === arg){
                return this.iExpand? 'collapsex collapse-level-1 two-col-list': 'collapsex collapse-level-1 two-col-list collapse';
            }else{
                return 'collapsex collapse-level-1 two-col-list collapse';
            }
        },
        selectMod: function(arg){
            this.iExpand = (this.iMod == arg)? !this.iExpand: true;
            this.iMod = arg;
        },
        select: function(arg){
            //this.iMod = arg.replace(/\.\d+$/, '');
            this.iPage = arg;
        }
    },
    mounted(){
        console.log('Is navegation system activate! daniel');
        this.config();
    }
}
</script>