<template>
    <div :id="keyname" class="grafico" ref="chartdiv" :style="{height: altura + 'px'}"></div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_colombiaLow from "@amcharts/amcharts4-geodata/colombiaLow";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        altura: {type: Number, default: 300},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        campo_serie: {type: String, default: ''},
        lanzarevento: {type: String, default: 'none'},
        multitamaño: {type: Boolean, default: false},
        etiquetas: {type: Boolean, default: false},
        leyenda: {type: String, default: 'none'},
        radio: {type: Number, default: 0},
        esquinaredonda: {type: Boolean, default: false},
        alfa: {type: String, default: '1'}
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            deptos: {"05":"CO-ANT", "08":"CO-ATL", "11":"CO-DC", "13":"CO-BOL", "15":"CO-BOY", "17":"CO-CAL", "18":"CO-CAQ", "19":"CO-CAU", "20":"CO-CES", "23":"CO-COR", "25":"CO-CUN", "27":"CO-CHO", "41":"CO-HUI", "44":"CO-LAG", "47":"CO-MAG", "50":"CO-MET", "52":"CO-NAR", "54":"CO-NSA", "63":"CO-QUI", "66":"CO-RIS", "68":"CO-SAN", "70":"CO-SUC", "73":"CO-TOL", "76":"CO-VAC", "81":"CO-ARA", "85":"CO-CAS", "86":"CO-PUT", "88":"CO-SAP", "91":"CO-AMA", "94":"CO-GUA", "95":"CO-GUV", "97":"CO-VAU", "99":"CO-VID"},
            chart: null,
            datos: [],
            ejeCategorias: null,
            ejeValores: null,
            listSeries: [],
            colors: ["#F0C541", "#2ECD99", "#4E9DE6", "#ED6F56", "#F1A1C7", "#FF0F00", "#FF6600", "#FF9E01", "#FCD202", "#F8FF01", "#B0DE09", "#0D8ECF", "#0D52D1", "#8A0CCF", "#CD0D74", "#754DEB", "#DDDDDD", "#999999", "#333333", "#000000", "#57032A", "#CA9726", "#990000", "#4B0C25"],
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
            this.chart = am4core.create(this.$refs.chartdiv, am4maps.MapChart);
            this.chart.geodata = am4geodata_colombiaLow;

            let polygonSeries = this.chart.series.push(new am4maps.MapPolygonSeries());
            polygonSeries.useGeodata = true;
            polygonSeries.data = [{id: this.deptos["23"], value: 489785}];

            let polygonTemplate = polygonSeries.mapPolygons.template;
            polygonTemplate.tooltipText = "{name}: {value}";
            polygonTemplate.nonScalingStroke = true;
            polygonTemplate.strokeWidth = 0.5;

            let hs = polygonTemplate.states.create("hover");
            hs.properties.fill = am4core.color("#3C5BDC");
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