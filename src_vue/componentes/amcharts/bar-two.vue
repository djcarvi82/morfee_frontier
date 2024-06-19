<template>
    <div>
        <div v-if="preloading != 'none' && !hasData" :style="{height: altura + 'px'}">
            <div class="text-center font-24 vertical-align-middle" :style="{'margin-top': halfsize + 'px'}">
                <i class="fa fa-spinner fa-spin"></i> {{ (preloading == '')? "Cargando datos ...": preloading }}
            </div>
        </div>
        <div :id="keyname" ref="chartdiv" :class="(preloading != 'none' && !hasData)? 'hide': ''" :style="{height: lc_altura + 'px'}"></div>
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        altura: {type: String, default: "300"},
        unidad: {type: String, default: ''},
        multicolor: {type: Boolean, default: false},
        ordenado: {type: Boolean, default: false},
        redondeado: {type: Boolean, default: false},
        apilado: {type: Boolean, default: false},
        leyenda: {type: String, default: 'none'},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        alfa: {type: String, default: '1'},
        etiquetas: {type: Boolean, default: false},
        lanzarevento: {type: String, default: 'none'},
        muestra: {type: Boolean, default: false},
        titulo_eje: {type: String, default: 'none'},
        titulo_categoria: {type: String, default: 'none'},
        preloading: {type: String, default: 'none'},
        min: {type: String, default: "none"},
        max: {type: String, default: "none"},
        paleta: {type: String, default: "basica"},
        grosor: {type: String, default: "none"},
        suave: {type: Boolean, default: false},
        puntos: {type: Boolean, default: false},
        rotar: {type: Boolean, default: false},
        cursor: {type: Boolean, default: false},
        grilla: {type: String, default: '0.1'},
        horizontal: {type: Boolean, default: false},
        sin_valores: {type: Boolean, default: false},
        tooltip: {type: Boolean, default: false},
        custom: {type: String, default: ''},
        pretag: {type: String, default: ''},
        // empty_data: {type: String, default: ''},
        empty_category: {type: String, default: ''},
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            lc_altura: 0,
            lc_unidad: this.unidad == ''? 30: parseInt(this.unidad),
            lc_grilla: 0.1,
            lc_custom: this.custom,
            chart: null,
            datos: [],
            ejeCategorias: null,
            ejeValores: null,
            listSeries: [],
            boxSeries: [],
            txleyendas: [],
            boxTypes: [],
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
            isCreated: false
        }
    },
    methods: {
        exportar: function(){
            if(this.chart != null){
                this.chart.exporting.export("png");
            }
        },
        getTypeSerie: function(arg){
            return (["columna", "linea"].indexOf(arg) > -1)? arg: "columna";
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
                var plt = ['basica', 'basica', 'material', 'dataviz', 'kelly', 'frozen', 'moonrise'];
                var num = parseInt(arg);
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
        setDatos: function(arg){
            // this.datos = arg;
            this.datos = (this.empty_category == '')? arg: arg.map(elm => {
                if(elm[this.campo_categoria] === ''){
                    elm[this.campo_categoria] = this.empty_category;
                }
                return elm;
            });
            let ckey = this.listSeries[0];
            if(this.ordenado){
                this.datos = this.datos.sort((a, b) => b[ckey] - a[ckey]);
            }
            this.lc_altura = (this.datos.length > 0)? this.datos.length * this.lc_unidad + 60: 200;
            if(this.isCreated){
                this.chart.data = this.datos;
            }
            this.hasData = true;
        },
        createChart: function(){
            var colorSet = new am4core.ColorSet();
            colorSet.list = this.getPaleta().map(col => new am4core.color(col));
            
            this.chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
            this.chart.colors = colorSet;
            this.chart.data = this.datos;

            if(this.leyenda != 'none'){
                this.chart.legend = new am4charts.Legend();
                this.chart.legend.position = (this.leyenda == '')? 'top': this.leyenda;
            }else if(this.listSeries.length > 1){
                this.chart.legend = new am4charts.Legend();
                this.chart.legend.position = 'top';
            }

            this.ejeCategorias = this.chart.yAxes.push(new am4charts.CategoryAxis());
            this.ejeCategorias.dataFields.category = this.campo_categoria;
            // this.ejeCategorias.numberFormatter.numberFormat = "#";
            this.ejeCategorias.renderer.inversed = true;
            this.ejeCategorias.renderer.grid.template.location = 0;
            this.ejeCategorias.renderer.cellStartLocation = 0.1;
            this.ejeCategorias.renderer.cellEndLocation = 0.9;
            // this.ejeCategorias.fontFamily = 'Arial';

            this.ejeValores = this.chart.xAxes.push(new am4charts.ValueAxis());
            this.ejeValores.renderer.opposite = true;
            this.ejeValores.fontFamily = 'Arial';
            this.ejeValores.renderer.labels.template.disabled = true;

            this.listSeries.forEach((elm, indice) => {
                let field = elm;
                let name = this.txleyendas[indice];
                let series = this.chart.series.push(new am4charts.ColumnSeries());

                // series.columns.template.tooltipText = this.lc_custom == ''? this.txleyendas[indice] + ": {valueY}": this.lc_custom;
                series.columns.template.tooltipText = this.txleyendas[indice] + ": {valueY}";
                series.columns.template.tooltipY = am4core.percent(50);
                series.columns.template.tooltipX = am4core.percent(100);
                // series.columns.template.width = am4core.percent(90);

                series.dataFields.valueX = field;
                series.dataFields.categoryY = this.campo_categoria;
                series.name = name;
                series.columns.template.tooltipText = "{name}: [bold]{valueX}[/]";
                series.columns.template.height = am4core.percent(90);
                series.sequencedInterpolation = true;

                series.columns.template.events.on("hit", ev => {
                    var contexto = ev.target.dataItem.dataContext;
                    if(this.lanzarevento != 'none'){
                        var tm = contexto;
                        tm.campo_categoria = this.campo_categoria;
                        tm.campo_valor = elm;
                        if(this.empty_category != '' && tm[this.campo_categoria] == this.empty_category){
                            tm[this.campo_categoria] = "";
                        }
                        this.$eventBus.$emit(this.lanzarevento, tm);
                    }
                });

                let valueLabel = series.bullets.push(new am4charts.LabelBullet());
                valueLabel.label.text = "{valueX}";
                valueLabel.label.horizontalCenter = "left";
                valueLabel.label.dx = 10;
                valueLabel.label.hideOversized = false;
                valueLabel.label.truncate = false;

                let categoryLabel = series.bullets.push(new am4charts.LabelBullet());
                categoryLabel.interactionsEnabled = false;
                categoryLabel.label.text = "{name}";
                categoryLabel.label.horizontalCenter = "right";
                categoryLabel.label.dx = -10;
                categoryLabel.label.fill = am4core.color("#fff");
                categoryLabel.label.hideOversized = false;
                categoryLabel.label.truncate = false;
                this.boxSeries.push(series);
            });

            if(this.titulo_categoria != 'none'){
                this.ejeCategorias.title.text = this.titulo_categoria;
            }

            if(this.sin_valores) this.ejeValores.renderer.labels.template.disabled = true;
            if(this.min != "none") this.ejeValores.min = parseInt(this.min);
            if(this.max != "none"){
                this.ejeValores.max = parseInt(this.max);
            }else{
                this.ejeValores.extraMax = 0.2;
            }
            if(this.titulo_eje != 'none'){
                this.ejeValores.title.text = this.titulo_eje;
            }
            // let cursor = new am4charts.XYCursor();
            // this.chart.cursor = cursor;
            // cursor.lineX.disabled = true;
            // cursor.lineY.disabled = true;
            // cursor.behavior = "none";
            this.isCreated = true;
        },
    },
    mounted(){
        this.setPaleta(this.paleta);
        this.lc_grilla = parseFloat(this.grilla);
        this.halfsize = this.lc_altura * 0.5;
        this.campo_valor.split(',').forEach(elm => {
            var tm = elm.split(':');
            this.listSeries.push(tm[0]);
            (tm.length > 1)? this.txleyendas.push(tm[1]): this.txleyendas.push(tm[0]);
            (tm.length > 2)? this.boxTypes.push(this.getTypeSerie(tm[2])): this.boxTypes.push(this.getTypeSerie("columna"));
        });
        this.createChart();
    }
}
</script>