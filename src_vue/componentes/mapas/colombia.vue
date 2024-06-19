<template>
    <div :id="keyname" class="grafico" ref="chartdiv" :style="{height: altura + 'px'}"></div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_colombiaHigh from "@amcharts/amcharts4-geodata/colombiaHigh";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        altura: {type: String, default: '300'},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        campo_titulo: {type: String, default: 'title'},
        campo_latitud: {type: String, default: 'latitude'},
        campo_longitud: {type: String, default: 'longitude'},
        multicolor: {type: Boolean, default: false},
        lanzarevento: {type: String, default: 'none'},
        muestra: {type: Boolean, default: false},
        paleta: {type: String, default: "basica"}
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            deptos: {"05":"CO-ANT", "08":"CO-ATL", "11":"CO-DC", "13":"CO-BOL", "15":"CO-BOY", "17":"CO-CAL", "18":"CO-CAQ", "19":"CO-CAU", "20":"CO-CES", "23":"CO-COR", "25":"CO-CUN", "27":"CO-CHO", "41":"CO-HUI", "44":"CO-LAG", "47":"CO-MAG", "50":"CO-MET", "52":"CO-NAR", "54":"CO-NSA", "63":"CO-QUI", "66":"CO-RIS", "68":"CO-SAN", "70":"CO-SUC", "73":"CO-TOL", "76":"CO-VAC", "81":"CO-ARA", "85":"CO-CAS", "86":"CO-PUT", "88":"CO-SAP", "91":"CO-AMA", "94":"CO-GUA", "95":"CO-GUV", "97":"CO-VAU", "99":"CO-VID"},
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
            chart: null,
            polygonSeries: null,
            imageSeries: null,
            datos: [],
            listSeries: [],
            isCreated: false,
            hasPoint: false,
        }
    },
    methods: {
        loadRuta: function(){
            if(this.ruta != 'none'){
                axios.get(this.ruta).then(response => {
                    this.setDatos(response.data[this.contexto]);
                }).catch(err => {console.log(err)});
            }
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
            var tmp = [];
            arg.forEach(elm => {
                tmp.push({
                    id: this.deptos[elm[this.campo_categoria]],
                    value: elm[this.campo_valor]
                });
            });
            this.datos = tmp;
            this.polygonSeries.data = this.datos;
        },
        setPuntos: function(arg){
            if(this.hasPoint == false){
                this.imageSeries = this.chart.series.push(new am4maps.MapImageSeries());
                let imageSeriesTemplate = this.imageSeries.mapImages.template;
                let circle = imageSeriesTemplate.createChild(am4core.Sprite);
                circle.scale = 0.4;
                circle.fill = new am4core.InterfaceColorSet().getFor("alternativeBackground");
                circle.path = "M9,0C4.029,0,0,4.029,0,9s4.029,9,9,9s9-4.029,9-9S13.971,0,9,0z M9,15.93 c-3.83,0-6.93-3.1-6.93-6.93S5.17,2.07,9,2.07s6.93,3.1,6.93,6.93S12.83,15.93,9,15.93 M12.5,9c0,1.933-1.567,3.5-3.5,3.5S5.5,10.933,5.5,9S7.067,5.5,9,5.5 S12.5,7.067,12.5,9z";
                imageSeriesTemplate.propertyFields.latitude = this.campo_latitud;
                imageSeriesTemplate.propertyFields.longitude = this.campo_longitud;
                imageSeriesTemplate.horizontalCenter = "middle";
                imageSeriesTemplate.verticalCenter = "middle";
                imageSeriesTemplate.align = "center";
                imageSeriesTemplate.valign = "middle";
                imageSeriesTemplate.width = 8;
                imageSeriesTemplate.height = 8;
                imageSeriesTemplate.nonScaling = true;
                imageSeriesTemplate.tooltipText = "{title}";
                imageSeriesTemplate.fill = am4core.color("#000");
                imageSeriesTemplate.background.fillOpacity = 0;
                imageSeriesTemplate.background.fill = am4core.color("#FFFFFF");
                imageSeriesTemplate.setStateOnChildren = true;
                imageSeriesTemplate.states.create("hover");
                this.hasPoint = true;
            }
            this.imageSeries.data = arg;
        },
        preview: function(){
            let dts = [];
            for(var i in this.deptos){
                dts.push({
                    "categoria": i,
                    "valor": Math.round(Math.random() * 80000 + 20000)
                });
            }
            this.setDatos(dts);

            var pt = [
                {"title": "Bogota", "latitude": 4.6473, "longitude": -74.0962},
                {"title": "Sincelejo", "latitude": 9.303011, "longitude": -75.394431},
                {"title": "Montería", "latitude": 8.737682, "longitude": -75.887635}
            ];
            this.setPuntos(pt);
        },
        createChart: function(){
            var colorSet = new am4core.ColorSet();
            colorSet.list = this.getPaleta().map(col => new am4core.color(col));

            this.chart = am4core.create(this.$refs.chartdiv, am4maps.MapChart);
            this.chart.colors = colorSet;
            this.chart.geodata = am4geodata_colombiaHigh;
            
            this.polygonSeries = this.chart.series.push(new am4maps.MapPolygonSeries());

            if(!this.multicolor){
                this.polygonSeries.heatRules.push({
                    property: "fill",
                    target: this.polygonSeries.mapPolygons.template,
                    min: this.chart.colors.getIndex(1).brighten(1),
                    max: this.chart.colors.getIndex(1).brighten(-0.3)
                });
            }

            this.polygonSeries.useGeodata = true;
            this.polygonSeries.data = this.datos;//[{id: this.deptos["23"], value: 489785}];

            let polygonTemplate = this.polygonSeries.mapPolygons.template;
            polygonTemplate.tooltipText = "{name}: {value}";
            polygonTemplate.nonScalingStroke = true;
            polygonTemplate.strokeWidth = 0.5;

            if(this.multicolor){
                polygonTemplate.fillOpacity = 0.6;
                polygonTemplate.adapter.add("fill", (fill, target) => {
                    if(target.dataItem.index > 0){
                        return this.chart.colors.getIndex(target.dataItem.index);
                    }
                    return fill;
                });
            }

            let hs = polygonTemplate.states.create("hover");
            if(this.multicolor){
                hs.properties.fillOpacity = 1;
            }else{
                hs.properties.fill = am4core.color("#3C5BDC");
            }
            this.isCreated = true;
        }
    },
    mounted(){
        this.setPaleta(this.paleta);
        this.createChart();
        this.loadRuta();
        if(this.muestra){
            this.preview();
        }
    }
}
</script>