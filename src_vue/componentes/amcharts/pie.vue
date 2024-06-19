<template>
    <div>
        <div v-if="preloading != 'none' && !hasData" :style="{height: altura + 'px'}">
            <div class="text-center font-24 vertical-align-middle" :style="{'margin-top': halfsize + 'px'}">
                <i class="fa fa-spinner fa-spin"></i> {{ (preloading == '')? "Cargando datos ...": preloading }}
            </div>
        </div>
        <div :id="keyname" ref="chartdiv" :class="(preloading != 'none' && !hasData)? 'hide': ''" :style="{height: altura + 'px'}"></div>
        <div class="alert alert-warning mt-2" v-if="overload">
            <div class="d-flex">
                <i class="fa fa-warning me-2"></i>
                <span>Hay demasiados datos para visualizar en un gráfico de torta! (Más de 30).</span>
            </div>
        </div>
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        altura: {type: String, default: "150"},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        campo_color: {type: String, default: ''},
        lanzarevento: {type: String, default: 'none'},
        multitamaño: {type: Boolean, default: false},
        etiquetas: {type: String, default: 'none'},
        leyenda: {type: String, default: 'none'},
        compact: {type: Boolean, default: false},
        radio: {type: String, default: "0"},
        esquinaredonda: {type: Boolean, default: false},
        efecto: {type: Boolean, default: false},
        alfa: {type: String, default: '1'},
        paleta: {type: String, default: "basica"},
        muestra: {type: Boolean, default: false},
        preloading: {type: String, default: 'none'},
        totalizar: {type: String, default: 'none'},
        label_align: {type: Boolean, default: false},
        angulo: {type: String, default: ''},
        area: {type: String, default: ''},
        enfocar: {type: Boolean, default: false},
        custom: {type: String, default: ''},
        empty_category: {type: String, default: ''},
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            chart: null,
            datos: [],
            ejeCategorias: null,
            ejeValores: null,
            listSeries: [],
            label: null,
            paletas: {
                basica: ["#67b7dc", "#6794dc", "#6771dc", "#8067dc", "#a367dc", "#c767dc", "#dc67ce", "#dc67ab", "#dc6788", "#dc6967", "#dc8c67", "#dcaf67", "#dcd267", "#c3dc67", "#a0dc67", "#7ddc67", "#67dc75", "#67dc98", "#67dcbb", "#67dadc"],
                material: ["#f44336", "#e91e63", "#9c27b0", "#673ab7", "#3f51b5", "#2196f3", "#03a9f4", "#00bcd4", "#009688", "#4caf50", "#8bc34a", "#cddc39", "#ffeb3b", "#ffc107", "#ff9800", "#ff5722", "#795548", "#9e9e9e", "#607d8b"],
                dataviz: ["#283250", "#902c2d", "#d5433d", "#f05440", "#f05440", "#f26958", "#f47e6f", "#f69487", "#f7a99f", "#f9beb6", "#fbd3ce", "#d32711", "#eb2b12", "#741509", "#8c1a0b", "#a41e0d", "#bb220f", "#741509", "#8c1a0b", "#a41e0d", "#bb220f", "#d32711", "#eb2b12", "#ee3f28"],
                kelly: ["#f3c300", "#875692", "#f38400", "#a1caf1", "#be0032", "#c2b280", "#848482", "#008856", "#e68fac", "#0067a5", "#f99379", "#604e97", "#f6a600", "#b3446c", "#dcd300", "#882d17", "#8db600", "#654522", "#e25822", "#2b3d26", "#f2f3f4", "#222222"],
                frozen: ["#bec4f8", "#a5abee", "#6a6dde", "#4d42cf", "#713e8d", "#a160a0", "#eb6eb0", "#f597bb", "#fbb8c9", "#f8d4d8"],
                moonrise: ["#3a1302", "#601205", "#8a2b0d", "#c75e24", "#c79f59", "#a4956a", "#868569", "#756f61", "#586160", "#617983"],
                custom: [],
            },
            themePaleta: '',
            _accion: null,
            hasData: false,
            halfsize: 0,
            isCreated: false,
            overload: false,
        }
    },
    methods: {
        formatMiles: function(num){
            let regla = /(\d+)(\d{3})/;
            let tmp = String(num);
            while(regla.test(tmp)){
                tmp = tmp.replace(regla, '$1' + ',' + '$2');
            }
            return tmp;
        },
        preview: function(){
            let dt = [];
            ['Montería', 'Bogotá', 'Medellín', 'Cali', 'Cartagena'].forEach(elm => {
                dt.push({'categoria': elm, 'valor': Math.round(Math.random() * 20 + 10)});
            });
            this.setDatos(dt);
        },
        loadRuta: function(){
            if(this.ruta != 'none'){
                axios.get(this.ruta).then(response => {
                    this.setDatos(response.data[this.contexto]);
                }).catch(err => {console.log(err)});
            }
        },
        setFocusBar: function(index){
            let opaque = (index == -1)? 1: 0.3;
            console.log('dimitrie');
            console.log(this.chart);
            // this.chart.series.values[0].columns.values.forEach((elm, i) => {
            //     elm.fillOpacity = (index == i)? 1: opaque;
            // });

            // pieSeries.slices.template.adapter.add("fill", function (fill, target) {
            //     return target.dataItem.dataContext["color"];
            // });            
        },
        setDatos: function(arg){
            if(Array.isArray(arg)){
                let aux = ['', undefined, null];
                let txs = ['(Vacío)', '(undefined)', '(null)'];
                this.datos = arg;
                if(arg.length > 30){
                    this.overload = true;
                    this.datos = (this.empty_category == '')? arg.slice(0, 30): arg.slice(0, 30).map(elm => {
                        if(aux.includes(elm[this.campo_categoria])){
                            let ind = aux.findIndex(a => elm[this.campo_categoria] === a);
                            elm[this.campo_categoria] = txs[ind];
                        }
                        return elm;
                    });
                }else{
                    this.overload = false;
                    this.datos = (this.empty_category == '')? arg: arg.map(elm => {
                        if(aux.includes(elm[this.campo_categoria])){
                            let ind = aux.findIndex(a => elm[this.campo_categoria] === a);
                            elm[this.campo_categoria] = txs[ind];
                        }
                        return elm;
                    });
                }
                if(this.isCreated){
                    this.chart.data = this.datos;
                    if(this.totalizar != "none"){
                        let rs = this.datos.reduce((acum, elm) => acum + parseInt(elm[this.listSeries[0]]), 0);
                        this.label.text = this.formatMiles(rs);
                    }
                }
                this.hasData = true;
            }else{
                console.log('Esto no es un array:');
                console.log(arg);
            }
        },
        loadingStatus: function(){
            this.setDatos([]);
            this.hasData = false;
        },
        setAccion: function(arg){
            this._accion = arg;
        },
        setPaleta: function(arg){
            if(arg == '' || arg == undefined){
                this.themePaleta = 'basica';
            }else if(['basica', 'material', 'dataviz', 'kelly', 'frozen', 'moonrise'].indexOf(arg) > -1){
                this.themePaleta = arg;
            }else if(/^\d+$/.test(arg)){
                let plt = ['basica', 'basica', 'material', 'dataviz', 'kelly', 'frozen', 'moonrise'];
                let num = parseInt(arg);
                this.themePaleta = (num > 0 && num < 7)? plt[num]: 'basica';
            }else if(/#/.test(arg)){
                this.paletas.custom = arg.split(',');
                this.themePaleta = 'custom';
            }else{
                this.themePaleta = 'basica';
            }
        },
        getPaleta: function(){
            return this.paletas[this.themePaleta];
        },
        createChart: function(){
            let colorSet = new am4core.ColorSet();
            colorSet.list = this.getPaleta().map(col => new am4core.color(col));
            this.chart = this.efecto? am4core.create(this.$refs.chartdiv, am4charts.PieChart3D): am4core.create(this.$refs.chartdiv, am4charts.PieChart);
            this.chart.hiddenState.properties.opacity = 0;
            if(this.area != ''){
                this.chart.radius = am4core.percent(parseInt(this.area));
            }
            if(this.angulo != ''){
                if(this.angulo == 'semi'){
                    this.chart.startAngle = 180;
                    this.chart.endAngle = 360;
                }else{
                    let tm = this.angulo.split(':').map(tx => parseInt(tx));
                    this.chart.startAngle = tm[0];
                    this.chart.endAngle = (tm.length > 1)? tm[1]: tm[0] + 360;
                }
            }
            // alert(this.chart.startAngle + ':' + this.chart.endAngle);
            if(this.efecto){
                //this.chart.innerRadius = 50;
            }
            if(this.totalizar != "none"){
                if(this.radio == "0"){
                    this.chart.innerRadius = 100;
                }
                let bis = this.totalizar.split('|');
                let tam = (this.totalizar == '')? 50: parseInt(bis[0]);
                this.label = this.chart.seriesContainer.createChild(am4core.Label);
                this.label.horizontalCenter = "middle";
                this.label.verticalCenter = "middle";
                this.label.fontSize = tam;
                if(bis.length > 1){
                    let subtx = this.chart.seriesContainer.createChild(am4core.Label);
                    subtx.horizontalCenter = "middle";
                    subtx.verticalCenter = "middle";
                    subtx.fontSize = (bis.length == 3)? parseInt(bis[2]): 14;
                    subtx.dy = parseInt(tam / 2 + 7);
                    subtx.text = bis[1];
                }
            }
            this.listSeries.forEach(elm => {
                let serie = this.efecto? this.chart.series.push(new am4charts.PieSeries3D()): this.chart.series.push(new am4charts.PieSeries());
                if(this.campo_color != ''){
                    serie.slices.template.propertyFields.fill = this.campo_color;
                }else{
                    serie.colors = colorSet;
                }
                if(this.label_align == false) serie.alignLabels = false;
                serie.dataFields.category = this.campo_categoria;
                serie.dataFields.value = elm;
                // Funcionalidad pendiente...
                // serie.slices.template.states.getKey('hover').properties.scale = 1;
                serie.slices.template.states.getKey('active').properties.shiftRadius = 0;
                if(this.custom != ''){
                    // serie.slices.template.tooltipText = this.custom;
                    serie.slices.template.tooltipHTML = this.custom;
                }
                /*  Efecto interesante de labels plegados al borde
                serie.alignLabels = false;
                serie.labels.template.bent = true;
                serie.labels.template.radius = 3;
                serie.labels.template.padding(0,0,0,0);
                */
                if(this.multitamaño) serie.dataFields.radiusValue = elm;
                if(parseInt(this.radio) > 0) serie.innerRadius = am4core.percent(parseInt(this.radio));
                if(this.esquinaredonda) serie.slices.template.cornerRadius = 6;
                serie.slices.template.stroke = am4core.color("#FFF");
                serie.slices.template.strokeWidth = .5;
                serie.slices.template.strokeOpacity = 1;
                serie.slices.template.fillOpacity = 1;
                // serie.slices.template.propertyFields.isActive = "isActive";
                if(this.etiquetas == 'none') serie.labels.template.disabled = true;
                if(this.etiquetas == 'value'){
                    serie.labels.template.text = "{value.percent.formatNumber('#.0')}%";
                }
                serie.slices.template.events.on("hit", ev => {
                    let contexto = ev.target.dataItem.dataContext;
                    if(this._accion != null){
                        this._accion(contexto);
                    }
                    if(this.lanzarevento != 'none'){
                        let aux = ['', undefined, null];
                        let txs = ['(Vacío)', '(undefined)', '(null)'];
                        let tm = contexto;
                        tm.campo_categoria = this.campo_categoria;
                        tm.campo_valor = elm;
                        if(this.empty_category != '' && txs.includes(tm[this.campo_categoria])){
                            // tm[this.campo_categoria] = "";
                            let ind = txs.findIndex(ac => tm[this.campo_categoria] === ac);
                            tm[this.campo_categoria] = aux[ind];
                        }
                        this.$eventBus.$emit(this.lanzarevento, tm);
                    }
                    if(this.enfocar){
                        console.log('domona');
                        // serie.slices._values.forEach(sl => {
                        //     console.log('into sl');
                        //     console.log(sl);
                        // });
                        // this.setFocusBar(ev.target.dataItem.index);
                    }
                });
            });
            if(this.leyenda != 'none'){
                this.chart.legend = new am4charts.Legend();
                this.chart.legend.position = this.leyenda;
                if(this.compact){
                    this.chart.legend.markers.template.height = 16;
                    this.chart.legend.itemContainers.template.paddingTop = 5;
                    this.chart.legend.itemContainers.template.paddingBottom = 5;
                }
                if(this.leyenda == 'bottom'){
                    this.chart.legend.itemContainers.template.paddingTop = 24;
                    this.chart.legend.itemContainers.template.paddingBottom = 0;
                }
                // this.chart.legend.useDefaultMarker = true;
            }
            this.isCreated = true;
        }
    },
    mounted(){
        this.halfsize = parseInt(this.altura)  * 0.5;
        this.setPaleta(this.paleta);
        this.listSeries = this.campo_valor.split(',');
        this.createChart();
        this.loadRuta();
        if(this.muestra){
            this.preview();
        }
    }
}
</script>