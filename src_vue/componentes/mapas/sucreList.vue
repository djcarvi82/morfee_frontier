<template>
    <div class="row" style="border-top:1px solid #DEDEDE; border-bottom:1px solid #DEDEDE">
        <aside class="col-lg-4 col-md-4 pr-0 pl-0">
            <div class="task-panel" style="border-right:1px solid #DEDEDE">
                <a style="padding-top:2px; padding-bottom:2px" :class="(target.divipola == elm.divipola)? 'list-group-item bg-success': 'list-group-item'" v-for="(elm, indice) in lista" :key="indice" v-on:click="setMunicipio(elm)">
                    {{ elm.name }}
                </a>
            </div>
        </aside>
        <aside class="col-lg-8 col-md-8 pl-0">
            <div ref="mapa" :style="{height: '400px'}"></div>
        </aside>
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
            indice: -1,
            target: {'cod': '', 'name': '', 'divipola': ''},
            lista: [],
            chart: null,
            polygonSeries: null,
        }
    },
    methods: {
        preview: function(){
            /*
            let dts = [];
            for(var i in this.mcpios){
                dts.push({
                    "categoria": i,
                    "valor": Math.round(Math.random() * 80000 + 20000)
                });
            }
            this.setDatos(dts);

            let pt = [
                {"title": "Sincelejo", "latitude": 9.303011, "longitude": -75.394431}
            ];
            this.setPuntos(pt);*/
        },
        getLista: function(){
            return Object.keys(this.mcpios).map(dpola => {
                var lt = this.mcpios[dpola];
                lt.divipola = dpola;
                lt.include = false;
                return lt;
            })
        },
        nextMcpio: function(){
            this.indice++;
            if(this.indice >= this.lista.length) this.indice = 0;
            this.target = this.lista[this.indice];
            return this.target;
        },
        setMunicipio: function(codex){
            this.target = codex;
            this.chart.series.pop();
            this.polygonSeries = this.chart.series.push(new am4maps.MapPolygonSeries());
            this.polygonSeries.useGeodata = true;
            this.polygonSeries.include = [this.target.cod];
        },
        createGraph: function(){
            this.chart = am4core.create(this.$refs.mapa, am4maps.MapChart);
            //this.chart.colors = colorSet;
            this.chart.geodata = am4geodata_colombiaMuniHigh;
            this.chart.projection = new am4maps.projections.Mercator();
            this.chart.minZoomLevel = 0.6;
            this.chart.zoomLevel = 0.7;
            this.chart.maxZoomLevel = 1;

            this.polygonSeries = this.chart.series.push(new am4maps.MapPolygonSeries());
            this.polygonSeries.useGeodata = true;
            this.polygonSeries.include = [this.nextMcpio().cod];
        }        
    },
    mounted(){
        this.lista = this.getLista();
        this.createGraph();
    }
}
</script>