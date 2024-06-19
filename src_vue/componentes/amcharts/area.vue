<template>
    <div :id="keyname" class="grafico" ref="chartdiv"></div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        altura: {type: Number, default: 150},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        campo_serie: {type: String, default: ''},
        alfa: {type: String, default: '1'}
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            chart: null,
            datos: [],
            ejeCategorias: null,
            ejeValores: null,
            listSeries: [],

            dateAxis: null,
            valueAxis: null,
            series: null,

            colors: ["#F0C541", "#2ECD99", "#4E9DE6", "#04D215", "#2A0CD0", "#FF0F00", "#FF6600", "#FF9E01", "#FCD202", "#F8FF01", "#B0DE09", "#0D8ECF", "#0D52D1", "#8A0CCF", "#CD0D74", "#754DEB", "#DDDDDD", "#999999", "#333333", "#000000", "#57032A", "#CA9726", "#990000", "#4B0C25"],
        }
    },
    methods: {
        loadRuta: function(){
            if(this.ruta != 'none'){
                axios.get(this.ruta).then(response => {
                    this.datos = response.data[this.contexto];
                    this.chart.data = this.datos;
                }).catch(err => {console.log(err)});
            }
        },
        createChart: function(){
            var colorSet = new am4core.ColorSet();
            colorSet.list = this.colors.map(function(col){
                return new am4core.color(col);
            });

            this.chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
            this.chart.colors = colorSet;
            /*this.chart.plotContainer.stroke = am4core.color("#000000");
            this.chart.plotContainer.pixelPerfect = true;
            this.chart.plotContainer.strokeWidth = 0.2;
            this.chart.plotContainer.strokeOpacity = 1;*/
            this.ejeCategorias = this.chart.xAxes.push(new am4charts.CategoryAxis());
            this.ejeCategorias.dataFields.category = this.campo_categoria;
            this.ejeCategorias.renderer.grid.template.location = 0.5;
            this.ejeCategorias.renderer.grid.template.strokeOpacity = 0;
            this.ejeCategorias.startLocation = 0.5;
            this.ejeCategorias.endLocation = 0.5;
            this.ejeCategorias.fontFamily = 'Poppins';
            this.ejeCategorias.fontSize = 11;
            this.ejeCategorias.tooltip.disabled = true;
            this.ejeValores = this.chart.yAxes.push(new am4charts.ValueAxis());
            this.ejeValores.renderer.grid.template.strokeOpacity = 0;
            this.ejeValores.fontFamily = 'Poppins';
            this.ejeValores.fontSize = 11;
            this.ejeValores.tooltip.disabled = true;

            this.listSeries.forEach(elm => {
                var serie = this.chart.series.push(new am4charts.LineSeries());
                serie.dataFields.valueY = elm;
                serie.dataFields.categoryX = this.campo_categoria;
                serie.strokeWidth = 2;
                serie.tensionX = 0.77;
                serie.fillOpacity = 0.6;
                serie.tooltipText = elm + ": {valueY}";
                var bullet = serie.bullets.push(new am4charts.CircleBullet());
                bullet.strokeWidth = 1;
                bullet.circle.radius = 3;
            });
            this.chart.cursor = new am4charts.XYCursor();
            this.chart.cursor.lineX.strokeOpacity = 0;
            this.chart.cursor.lineY.strokeOpacity = 0;

            /*var label = this.series.bullets.push(new am4charts.LabelBullet());
            label.label.text = "{valueY.value}";
            label.label.dy = -10;*/
            //this.chart.dataSource.url = this.ruta;
        }
    },
    mounted(){
        if(this.campo_serie == ''){
            this.listSeries = this.campo_valor.split(',');
        }else{
            this.listSeries = this.campo_serie.split(',');
        }
        this.createChart();
        this.loadRuta();
    }
}
</script>