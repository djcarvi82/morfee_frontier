<template>
    <span>
        <span class="font-14 vertical-align-middle" v-if="preloading != 'none' && !hasData">
            <i class="fa fa-spinner fa-spin"></i>
        </span>
        <div :id="keyname" ref="chartdiv" :class="(preloading != 'none' && !hasData)? 'hide': ''" :style="{width: ancho + 'px', height: altura + 'px', display: 'inline-block'}"></div>
    </span>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        multicolor: {type: Boolean, default: false},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        paleta: {type: String, default: "basica"},
        grosor: {type: String, default: "none"},
        puntos: {type: Boolean, default: false},
        preloading: {type: String, default: 'none'},
        items: {type: String, default: 'none'},
        tipo: {type: String, default: 'barra'},
        titulo: {type: String, default: 'none'},
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            ancho: 0,
            altura: 50,
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
            colors: null,
            chart: null,
            datos: [],
            hasData: false,
            halfsize: 0,
            isCreated: false
        }
    },
    methods: {
        iniConfig: function(){
            this.colors = new am4core.ColorSet();
            this.colors.list = this.getPaleta().map(col => new am4core.color(col));
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
            this.datos = arg;
            if(this.isCreated){
                this.chart.data = this.datos;
            }
            this.hasData = true;
        },
        createLineChart: function(title, data){
            this.setAncho(data.length);
            this.chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);            
            this.chart.colors = this.colors;
            //this.chart.width = am4core.percent(45);
            //this.chart.height = 70;
            this.chart.data = data;
            if(this.titulo != 'none'){
                this.chart.titles.template.fontSize = 10;
                this.chart.titles.template.textAlign = "left";
                this.chart.titles.template.isMeasured = false;
                this.chart.titles.create().text = title;
            }
            this.chart.padding(20, 5, 2, 5);

            let dateAxis = this.chart.xAxes.push(new am4charts.DateAxis());
            dateAxis.renderer.grid.template.disabled = true;
            dateAxis.renderer.labels.template.disabled = true;
            dateAxis.startLocation = 0.5;
            dateAxis.endLocation = 0.7;
            dateAxis.cursorTooltipEnabled = false;

            let valueAxis = this.chart.yAxes.push(new am4charts.ValueAxis());
            valueAxis.min = 0;
            valueAxis.renderer.grid.template.disabled = true;
            valueAxis.renderer.baseGrid.disabled = true;
            valueAxis.renderer.labels.template.disabled = true;
            valueAxis.cursorTooltipEnabled = false;

            this.chart.cursor = new am4charts.XYCursor();
            this.chart.cursor.lineY.disabled = true;
            this.chart.cursor.behavior = "none";

            let series = this.chart.series.push(new am4charts.LineSeries());
            series.tooltipText = "{date}: [bold]{value}";
            series.dataFields.dateX = this.campo_categoria;
            series.dataFields.valueY = this.campo_valor;
            //series.tensionX = 0.8;
            series.strokeWidth = 1;
            //series.stroke = color;

            // render data points as bullets
            let bullet = series.bullets.push(new am4charts.CircleBullet());
            bullet.circle.opacity = 0;
            //bullet.circle.fill = color;
            bullet.circle.propertyFields.opacity = "opacity";
            bullet.circle.radius = 3;            
        },
        createColumnChart: function(title, data){
            this.setAncho(data.length);
            this.chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
            this.chart.colors = this.colors;
            //this.chart.width = am4core.percent(45);
            //this.chart.height = 70;
            this.chart.data = data;
            if(this.titulo != 'none'){
                this.chart.titles.template.fontSize = 10;
                this.chart.titles.template.textAlign = "left";
                this.chart.titles.template.isMeasured = false;
                this.chart.titles.create().text = title;
            }
            this.chart.padding(20, 0, 0, 0);

            let dateAxis = this.chart.xAxes.push(new am4charts.DateAxis());
            dateAxis.renderer.grid.template.disabled = true;
            dateAxis.renderer.labels.template.disabled = true;
            dateAxis.cursorTooltipEnabled = false;

            let valueAxis = this.chart.yAxes.push(new am4charts.ValueAxis());
            valueAxis.min = 0;
            valueAxis.renderer.grid.template.disabled = true;
            valueAxis.renderer.baseGrid.disabled = true;
            valueAxis.renderer.labels.template.disabled = true;
            valueAxis.cursorTooltipEnabled = false;

            this.chart.cursor = new am4charts.XYCursor();
            this.chart.cursor.lineY.disabled = true;

            let series = this.chart.series.push(new am4charts.ColumnSeries());
            //series.tooltipText = "{date}: [bold]{value}";
            series.dataFields.dateX = this.campo_categoria;
            series.dataFields.valueY = this.campo_valor;
            series.strokeWidth = 0;
            series.fillOpacity = 0.5;
            series.columns.template.propertyFields.fillOpacity = "opacity";
            if(this.multicolor){
                series.columns.template.adapter.add('fill', (fill, target) => this.chart.colors.getIndex(target.dataItem.index));
            }
            //series.columns.template.fill = color;
        },
        createPieChart: function(title, data){
            this.setAncho(data.length);
            this.chart = am4core.create(this.$refs.chartdiv, am4charts.PieChart);
            this.chart.colors = this.colors;
            this.chart.width = am4core.percent(100);
            //this.chart.height = 70;
            //this.chart.width = this.ancho;
            this.chart.height = this.altura;
            //this.chart.padding(20, 0, 2, 0);
            this.chart.data = data;

            // Add and configure Series
            let pieSeries = this.chart.series.push(new am4charts.PieSeries());
            pieSeries.dataFields.value = this.campo_valor;
            pieSeries.dataFields.category = this.campo_categoria;
            pieSeries.labels.template.disabled = true;
            pieSeries.ticks.template.disabled = true;
            //pieSeries.slices.template.fill = color;
            //pieSeries.slices.template.adapter.add("fill", (fill, target) => fill.lighten(0.1 * target.dataItem.index));
            pieSeries.slices.template.stroke = am4core.color("#fff");
            // chart.chartContainer.minHeight = 40;
            // chart.chartContainer.minWidth = 40;
        },
        setAncho: function(num){
            if(this.tipo == 'barra'){
                this.ancho = (this.titulo == 'none')? num * 40: num * 40 + 50;
            }else if(this.tipo == 'linea'){
                this.ancho = (this.titulo == 'none')? num * 30: num * 30 + 50;
            }else if(this.tipo == 'pie'){
                this.ancho = altura + 20;
            }
        },
        parseItems: function(arg){
            if(this.tipo == 'linea'){
                this.createLineChart(this.titulo, [{'categoria': '2020-01-01', 'valor': 24}, {'categoria': '2020-02-01-', 'valor': 34}, {'categoria': '2020-03-01-', 'valor': 14}]);
            }else if(this.tipo == 'barra'){
                this.createColumnChart(this.titulo, [{'categoria': '2020-01-01', 'valor': 24}, {'categoria': '2020-02-01-', 'valor': 34}]);
            }else if(this.tipo == 'torta'){
                this.createPieChart(this.titulo, [{'categoria': '2020-01-01', 'valor': 24}, {'categoria': '2020-02-01-', 'valor': 42}]);
            }
            this.hasData = true;
        }
    },
    mounted(){
        this.setPaleta(this.paleta);
        this.iniConfig();
        this.parseItems(this.items);
    }
}
</script>