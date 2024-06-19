<template>
    <div>
        <div id="chartdiv" ref="chartdiv" :style="{height: altura}"></div>
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''}
    },
    data() {
        return {
            altura: '400px',
			datos: [],
            cates: [],
            cuentas: {'1': 'ACTIVOS', '2': 'PASIVOS', '3': 'PATRIMONIO', '4': 'INGRESOS', '5': 'GASTOS', '6': 'COSTOS DEL SISTEMA GENERAL DE SEGURIDAD SOCIAL EN SALUD', '8': 'CUENTAS DE ORDEN DEUDORAS', '9': 'CUENTAS DE ORDEN ACREEDORAS'},
            hash: {},
            total: 0,
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        sortAsc: function(a, b){
            if(a == b){
                return 0;
            }
            return (a < b)? 1: -1;
        },
        loadData: function(){
            this.status = this.state.LOADING;
            axios.post(this.pathdata).then(res => {
                let aux = {};
                let num = 0;
                res.data[0].finanza.forEach(elm => {
                    if(aux[elm._id.n_eps] == undefined){
                        aux[elm._id.n_eps] = {'eps': elm._id.n_eps};
                    }
                    aux[elm._id.n_eps][this.cuentas[elm._id.n_cod]] = elm.suma;
                    num++;
                });
                this.datos = Object.values(aux);
                this.altura = (num * 40 + 30) + 'px';
                this.makeChart();
                this.status = this.state.LOADED;
            }).catch(err => {
                this.status = this.state.FAILED;
                console.log(err);
            });
            // this.datos = [
            //     {'eps': 'Sanitas', 'den': 'Activos', 'suma': 154263},
            //     {'eps': 'Sanitas', 'den': 'Patrimonio', 'suma': 134263},
            // ];
            // this.makeChart();
        },
        makeChart: function(){
            let chart = am4core.create("chartdiv", am4charts.XYChart);

            // Add data
            chart.data = this.datos;

            // Create axes
            let categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
            categoryAxis.dataFields.category = "eps";
            // categoryAxis.numberFormatter.numberFormat = "#";
            categoryAxis.renderer.inversed = true;
            categoryAxis.renderer.grid.template.location = 0;
            categoryAxis.renderer.cellStartLocation = 0.1;
            categoryAxis.renderer.cellEndLocation = 0.9;

            let  valueAxis = chart.xAxes.push(new am4charts.ValueAxis()); 
            valueAxis.renderer.opposite = true;

            // Create series
            function createSeries(field, name) {
                let series = chart.series.push(new am4charts.ColumnSeries());
                series.dataFields.valueX = field;
                series.dataFields.categoryY = "eps";
                series.name = name;
                series.columns.template.tooltipText = "{name}: [bold]{valueX}[/]";
                series.columns.template.height = am4core.percent(80);
                series.sequencedInterpolation = true;

                let valueLabel = series.bullets.push(new am4charts.LabelBullet());
                valueLabel.label.text = "{valueX}";
                valueLabel.label.horizontalCenter = "left";
                valueLabel.label.dx = 10;
                valueLabel.label.hideOversized = false;
                valueLabel.label.truncate = false;

                let categoryLabel = series.bullets.push(new am4charts.LabelBullet());
                categoryLabel.label.text = "{name}";
                categoryLabel.label.horizontalCenter = "right";
                categoryLabel.label.dx = -10;
                categoryLabel.label.fill = am4core.color("#fff");
                categoryLabel.label.hideOversized = false;
                categoryLabel.label.truncate = false;
            }
            Object.values(this.cuentas).forEach(elm => {
                createSeries(elm, elm);
            });
        },
    },
    mounted() {
        this.loadData();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
</style>