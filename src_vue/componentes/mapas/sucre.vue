<template>
    <div>
        <div :id="keyname" class="grafico" ref="chartdiv" :style="{height: altura + 'px'}"></div>
        <div ref="kojima" :style="{height: altura + 'px', visibility: 'hidden', position: 'absolute', top: '0px'}"></div>
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4maps from "@amcharts/amcharts4/maps";
import am4geodata_colombiaMuniHigh from "@amcharts/amcharts4-geodata/colombiaMuniHigh";
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
        paleta: {type: String, default: "basica"},
        minzoom: {type: String, default: ""},
        maxzoom: {type: String, default: ""},
        zoom: {type: String, default: ""},
        unique: {type: Boolean, default: false}
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            mcpios: {'70001':{'cod': 'CO-SU-SL', 'name': 'Sincelejo'}, '70110':{'cod': 'CO-SU-BU', 'name': 'Buenavista'}, '70124':{'cod': 'CO-SU-CA', 'name': 'Caimito'}, '70204':{'cod': 'CO-SU-CS', 'name': 'Colosó'}, '70215':{'cod': 'CO-SU-CZ', 'name': 'Corozal'}, '70233':{'cod': 'CO-SU-RO', 'name': 'El Roble'}, '70221':{'cod': 'CO-SU-CO', 'name': 'Coveñas'}, '70230':{'cod': 'CO-SU-CH', 'name': 'Chalán'}, '70235':{'cod': 'CO-SU-GA', 'name': 'Galeras'}, '70265':{'cod': 'CO-SU-GU', 'name': 'Guaranda'}, '70400':{'cod': 'CO-SU-LU', 'name': 'La Unión'}, '70418':{'cod': 'CO-SU-LP', 'name': 'Los Palmitos'}, '70429':{'cod': 'CO-SU-MA', 'name': 'Majagual'}, '70473':{'cod': 'CO-SU-MO', 'name': 'Morroa'}, '70508':{'cod': 'CO-SU-OV', 'name': 'Ovejas'}, '70523':{'cod': 'CO-SU-PA', 'name': 'Palmito'}, '70670':{'cod': 'CO-SU-SA', 'name': 'Sampués'}, '70678':{'cod': 'CO-SU-SB', 'name': 'San Benito Abad'}, '70702':{'cod': 'CO-SU-SJ', 'name': 'San Juan de Betulia'}, '70708':{'cod': 'CO-SU-SM', 'name': 'San Marcos'}, '70713':{'cod': 'CO-SU-SO', 'name': 'San Onofre'}, '70717':{'cod': 'CO-SU-SP', 'name': 'San Pedro'}, '70742':{'cod': 'CO-SU-SI', 'name': 'San Luis de Sincé'}, '70771':{'cod': 'CO-SU-SU', 'name': 'Sucre'}, '70820':{'cod': 'CO-SU-TO', 'name': 'Santiago de Tolú'}, '70823':{'cod': 'CO-SU-TV', 'name': 'San José de Toluviejo'}},
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
            charthide: null,
            polygonSeries1: null,
            activeMorph: null,
            _accion: null,
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
        getLista: function(){
            var lti = [];
            for(var i in this.mcpios){
                var mc = this.mcpios[i];
                mc.divipola = i;
                lti.push(mc);
            }
            return lti;
        },
        setMunicipio: function(divipola){
            if(this.charthide == null){
                this.chart.projection = new am4maps.projections.Mercator();
                this.chart.minZoomLevel = 0.9;
                this.chart.zoomLevel = 0.9;
                this.chart.maxZoomLevel = 1;

                this.charthide = am4core.create(this.$refs.kojima, am4maps.MapChart);
                this.charthide.geodata = am4geodata_colombiaMuniHigh;
                this.charthide.projection = new am4maps.projections.Mercator();

                this.polygonSeries1 = this.charthide.series.push(new am4maps.MapPolygonSeries());
                this.polygonSeries1.useGeodata = true;
                this.polygonSeries1.data = [];
            }

            let morphToPolygon;
            this.polygonSeries1.include = [this.mcpios[divipola].cod];

            this.polygonSeries1.events.once("validated", () => {
                morphToPolygon = this.polygonSeries1.mapPolygons.getIndex(0);
                if(morphToPolygon){
                    let countryPolygon = this.polygonSeries.mapPolygons.getIndex(0);
                    let morpher = countryPolygon.polygon.morpher;
                    let morphAnimation = morpher.morphToPolygon(morphToPolygon.polygon.points);
                }
            });
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
            var tmp = [];
            arg.forEach(elm => {
                if(this.mcpios.hasOwnProperty(elm[this.campo_categoria])){
                    tmp.push({
                        id: this.mcpios[elm[this.campo_categoria]].cod,
                        divipola: elm[this.campo_categoria],
                        value: elm[this.campo_valor]
                    });
                }
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
            for(var i in this.mcpios){
                dts.push({"categoria": i, "valor": Math.round(Math.random() * 80000 + 20000)});
            }
            this.setDatos(dts);
            /*let pt = [{"title": "Sincelejo", "latitude": 9.303011, "longitude": -75.394431}];
            this.setPuntos(pt);*/
        },
        createChart: function(){
            var colorSet = new am4core.ColorSet();
            colorSet.list = this.getPaleta().map(col => new am4core.color(col));

            this.chart = am4core.create(this.$refs.chartdiv, am4maps.MapChart);
            this.chart.colors = colorSet;
            this.chart.geodata = am4geodata_colombiaMuniHigh;

            if(this.minzoom != "") this.chart.minZoomLevel = parseFloat(this.minzoom);
            if(this.zoom != "") this.chart.zoomLevel = parseFloat(this.zoom);
            if(this.maxzoom != "") this.chart.maxZoomLevel = parseFloat(this.maxzoom);

            this.polygonSeries = this.chart.series.push(new am4maps.MapPolygonSeries());
            this.polygonSeries.include = this.unique? Object.entries(this.mcpios).map(val => val[1].cod).filter((elm, ind) => ind < 1): Object.entries(this.mcpios).map(val => val[1].cod);


            if(!this.multicolor){
                this.polygonSeries.heatRules.push({
                    property: "fill",
                    target: this.polygonSeries.mapPolygons.template,
                    min: this.chart.colors.getIndex(1).brighten(1),
                    max: this.chart.colors.getIndex(1).brighten(-0.3)
                });
            }

            this.polygonSeries.useGeodata = true;
            this.polygonSeries.data = this.datos;

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
            polygonTemplate.events.on("hit", evt => {
                if(this._accion != null){
                    this._accion(evt.target.dataItem.dataContext);
                }
            });

            let hs = polygonTemplate.states.create("hover");
            if(this.multicolor){
                hs.properties.fillOpacity = 1;
            }else{
                hs.properties.fill = am4core.color("#3C5BDC");
            }
            this.isCreated = true;

            /*let series = this.chart.series.push(new am4maps.MapImageSeries());
            series.dataFields.value = this.campo_valor;

            let template = series.mapImages.template;
            template.verticalCenter = "middle";
            template.horizontalCenter = "middle";
            template.propertyFields.latitude = "lat";
            template.propertyFields.longitude = "long";

            let label = template.createChild(am4core.Label);
            label.text = "{value}";
            label.fill = am4core.color("#FFF");
            label.verticalCenter = "middle";
            label.horizontalCenter = "middle";
            label.nonScaling = true;*/
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