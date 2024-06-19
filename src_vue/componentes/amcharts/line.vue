<template>
    <div>
        <div v-if="preloading != 'none' && !hasData" :style="{height: altura + 'px'}">
            <div class="text-center font-24 vertical-align-middle" :style="{'margin-top': halfsize + 'px'}">
                <i class="fa fa-spinner fa-spin"></i> {{ (preloading == '')? "Cargando datos ...": preloading }}
            </div>
        </div>
        <div :id="keyname" ref="chartdiv" :class="(preloading != 'none' && !hasData)? 'hide': ''" :style="{height: altura + 'px'}"></div>
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";
import am4themes_animated from "@amcharts/amcharts4/themes/animated";

am4core.useTheme(am4themes_animated);

export default {
    props: {
        altura: {type: String, default: '150'},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        alfa: {type: String, default: '1'},
        etiquetas: {type: Boolean, default: false},
        lanzarevento: {type: String, default: 'none'},
        min: {type: String, default: "none"},
        max: {type: String, default: "none"},
        paleta: {type: String, default: "custom"},
        grosor: {type: String, default: "none"},
        suave: {type: Boolean, default: false},
        relleno: {type: String, default: "none"},   // solido | degradado
        enmarcado: {type: String, default: "none"},
        puntos: {type: Boolean, default: false},
        cursor: {type: String, default: "none"},
        grilla: {type: String, default: "none"},
        guias: {type: String, default: ""},
        procesar_fechas: {type: Boolean, default: false},
        filtro: {type: String, default: "none"},
        preloading: {type: String, default: 'none'},
        manual: {type: Boolean, default: false},
        sin_valores: {type: Boolean, default: false},
        rotar: {type: Boolean, default: false},
        custom: {type: String, default: ''},
        gradient: {type: Boolean, default: false}
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            emptyDates: 0,
            lc_campo_categoria: '',
            lc_campo_valor: '',
            lc_custom: this.custom,
            field_categoria: 'categoria', 
            smart_category: null,
            chart: null,
            datos: [],
            ejeCategorias: null,
            ejeValores: null,
            listSeries: [],
            lineas: [],

            dateAxis: null,
            valueAxis: null,
            series: null,

            paletas: {
                basica: ["#67b7dc", "#6794dc", "#6771dc", "#8067dc", "#a367dc", "#c767dc", "#dc67ce", "#dc67ab", "#dc6788", "#dc6967", "#dc8c67", "#dcaf67", "#dcd267", "#c3dc67", "#a0dc67", "#7ddc67", "#67dc75", "#67dc98", "#67dcbb", "#67dadc"],
                material: ["#f44336", "#e91e63", "#9c27b0", "#673ab7", "#3f51b5", "#2196f3", "#03a9f4", "#00bcd4", "#009688", "#4caf50", "#8bc34a", "#cddc39", "#ffeb3b", "#ffc107", "#ff9800", "#ff5722", "#795548", "#9e9e9e", "#607d8b"],
                dataviz: ["#283250", "#902c2d", "#d5433d", "#f05440", "#f05440", "#f26958", "#f47e6f", "#f69487", "#f7a99f", "#f9beb6", "#fbd3ce", "#d32711", "#eb2b12", "#741509", "#8c1a0b", "#a41e0d", "#bb220f", "#741509", "#8c1a0b", "#a41e0d", "#bb220f", "#d32711", "#eb2b12", "#ee3f28"],
                kelly: ["#f3c300", "#875692", "#f38400", "#a1caf1", "#be0032", "#c2b280", "#848482", "#008856", "#e68fac", "#0067a5", "#f99379", "#604e97", "#f6a600", "#b3446c", "#dcd300", "#882d17", "#8db600", "#654522", "#e25822", "#2b3d26", "#f2f3f4", "#222222"],
                frozen: ["#bec4f8", "#a5abee", "#6a6dde", "#4d42cf", "#713e8d", "#a160a0", "#eb6eb0", "#f597bb", "#fbb8c9", "#f8d4d8"],
                moonrise: ["#3a1302", "#601205", "#8a2b0d", "#c75e24", "#c79f59", "#a4956a", "#868569", "#756f61", "#586160", "#617983"],
                custom: ["#F0C541", "#2ECD99", "#4E9DE6", "#04D215", "#2A0CD0", "#FF0F00", "#FF6600", "#FF9E01", "#FCD202", "#F8FF01", "#B0DE09", "#0D8ECF", "#0D52D1", "#8A0CCF", "#CD0D74", "#754DEB", "#DDDDDD", "#999999", "#333333", "#000000", "#57032A", "#CA9726", "#990000", "#4B0C25"],
            },
            themePaleta: '',
            lc_emptyAction: null,
            isCreated: false,
            hasData: false,
            halfsize: 0,
        }
    },
    methods: {
        setDatosVacios: function(fun){
            this.lc_emptyAction = fun;
        },
        aplicarFiltros: function(arg){
            if(this.filtro == 'date'){
                return new Date(arg);
            }else{
                return arg;
            }
        },
        setCategoria: function(){
            if(/\./.test(this.lc_campo_categoria)){
                this.field_categoria = "_fecha_";
                this.smart_category = (nodo) => this.lc_campo_categoria.split(".").reduce((acum, elm) => acum[elm], nodo);
            }else{
                this.field_categoria = this.lc_campo_categoria;
                this.smart_category = (nodo) => nodo[this.lc_campo_categoria];
            }
        },
        getCategoriaValue: function(nodo){
            return this.lc_campo_categoria.split(".").reduce((acum, elm) => acum[elm], nodo);
        },
        loadRuta: function(){
            if(this.ruta != 'none'){
                axios.get(this.ruta).then(response => {
                    this.setDatos(response.data[this.contexto]);
                }).catch(err => {console.log(err)});
            }
        },
        fillDatos: function(arg){
            this.emptyDates = 0;
            this.datos = [];
            let tmp = null;
            arg.forEach(elm => {
                tmp = this.smart_category(elm);
                if(tmp == undefined || tmp == "" || tmp == 0){
                    this.emptyDates += elm[this.lc_campo_valor];
                }else{
                    elm[this.field_categoria] = this.aplicarFiltros(tmp);
                    this.datos.push(elm);
                }
            });
        },
        setDatos: function(arg, pale=''){
            this.fillDatos(arg);
            /*let ckey = this.listSeries[0];
            if(this.ordenado){
                this.datos = this.datos.sort((a, b) => b[ckey] - a[ckey]);
            }*/
            if(this.isCreated){
                if(pale != ''){
                    this.changeColor(pale);
                }
                this.chart.data = this.datos;
                //this.hideIndicator();
            }
            if(this.emptyDates > 0){
                if(this.lc_emptyAction != null){
                    this.lc_emptyAction(this.emptyDates);
                }
            }
            this.hasData = true;
        },
        setDatosFromID: function(datosi, idcatField, iditemField, valField){
            let pre = {};
            let lines = {};
            datosi.forEach(elm => {
                if(pre[elm._id[idcatField]] == undefined){
                    pre[elm._id[idcatField]] = {};
                    pre[elm._id[idcatField]][idcatField] = elm._id[idcatField];
                }
                pre[elm._id[idcatField]][elm._id[iditemField]] = elm[valField];
                lines[elm._id[iditemField]] = elm._id[iditemField];
            });
            let predata = this.procesar_fechas? Object.values(pre): Object.values(pre).sort((a, b) => b[valField] - a[valField]);

            this.lc_campo_categoria = idcatField;
            this.lc_campo_valor = Object.values(lines).join(',');
            this.setCategoria();
            this.listSeries = this.lc_campo_valor.split(',');

            this.fillDatos(predata);
            this.createChart();
            this.chart.data = this.datos;
            this.hasData = true;

            console.log('CAROLINA');
            console.log(predata);
        },
        setPaleta: function(arg){
            if(arg == '' || arg == undefined){
                this.themePaleta = 'custom';
            }else if(['basica', 'material', 'dataviz', 'kelly', 'frozen', 'moonrise'].indexOf(arg) > -1){
                this.themePaleta = arg;
            }else if(/^\d+$/.test(arg)){
                var plt = ['basica', 'basica', 'material', 'dataviz', 'kelly', 'frozen', 'moonrise'];
                var num = parseInt(arg);
                this.themePaleta = (num > 0 && num < 7)? plt[num]: 'custom';
            }else if(/#/.test(arg)){
                this.paletas.custom = arg.split(',');
                this.themePaleta = 'custom';
            }else{
                this.themePaleta = 'custom';
            }
        },
        getPaleta: function(){
            return this.paletas[this.themePaleta];
        },
        addGuias: function(){
            /* <valor>:<texto>:<color>:<grosor> */
            this.guias.split("|").forEach(guia => {
                let gsd = guia.split(":");
                let range = this.ejeValores.axisRanges.create();
                range.value = parseFloat(gsd[0]);
                range.endValue = range.value;
                range.grid.stroke = (gsd.length > 2)? am4core.color(gsd[2]): am4core.color("#396478");
                range.grid.strokeWidth = (gsd.length > 3)? parseInt(gsd[3]): 1;
                range.grid.strokeOpacity = 1;
                range.grid.strokeDasharray = "3,3";
                range.label.inside = true;
                range.label.text = (gsd.length > 1)? gsd[1]: "";
                range.label.fill = range.grid.stroke;
                range.label.verticalCenter = "bottom";
            });
        },
        changeColor: function(pale){
            this.setPaleta(pale);
            let colorSet = new am4core.ColorSet();
            console.log(this.getPaleta());
            colorSet.list = this.getPaleta().map(col => new am4core.color(col));
            this.chart.colors = colorSet;
            this.lineas.forEach(serie => {
                serie.stroke = this.chart.colors.getIndex(0);
                if(this.gradient){
                    let efecto = new am4core.LinearGradient();
                    efecto.rotation = 90;
                    efecto.addColor(this.chart.colors.getIndex(0), 0.3);
                    efecto.addColor(this.chart.colors.getIndex(0), 0);
                    serie.fill = efecto;
                }
            });
        },
        createChart: function(){
            let colorSet = new am4core.ColorSet();
            colorSet.list = this.getPaleta().map(col => new am4core.color(col));

            this.chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
            this.chart.colors = colorSet;
            // if(this.gradient){
            //     this.chart.tooltip.getFillFromObject = false;
            //     this.chart.tooltip.background.fill = am4core.color("#000");
            // }
            if(this.enmarcado != "none"){
                this.chart.plotContainer.stroke = am4core.color((this.enmarcado == "")? "#AAA": this.enmarcado);
                this.chart.plotContainer.pixelPerfect = true;
                this.chart.plotContainer.strokeOpacity = 1;
            }
            
            this.ejeCategorias = (this.procesar_fechas)? this.chart.xAxes.push(new am4charts.DateAxis()): this.chart.xAxes.push(new am4charts.CategoryAxis());
            if(!this.procesar_fechas) this.ejeCategorias.dataFields.category = this.field_categoria;
            this.ejeCategorias.renderer.minGridDistance = 40;
            this.ejeCategorias.renderer.grid.template.location = 0.5;

            this.ejeCategorias.renderer.ticks.template.disabled = false;
            this.ejeCategorias.renderer.ticks.template.stroke = am4core.color((this.enmarcado == "" || this.enmarcado == "none")? "#AAA": this.enmarcado);
            this.ejeCategorias.renderer.ticks.template.strokeOpacity = 1;
            //this.ejeCategorias.startLocation = 0.5;
            //this.ejeCategorias.endLocation = 0.5;
            this.ejeCategorias.fontFamily = 'Poppins';
            //this.ejeCategorias.fontSize = 11;
            //this.ejeCategorias.tooltip.disabled = true;
            if(this.rotar){
                this.ejeCategorias.renderer.labels.template.horizontalCenter = "right";
                this.ejeCategorias.renderer.labels.template.verticalCenter = "middle";
                this.ejeCategorias.renderer.labels.template.rotation = 315;
            }
            this.ejeValores = this.chart.yAxes.push(new am4charts.ValueAxis());
            this.ejeValores.fontFamily = 'Poppins';
            if(this.sin_valores) this.ejeValores.renderer.labels.template.disabled = true;

            // Eye: Oculta los valores del eje.
            //this.ejeValores.renderer.labels.template.disabled = true;
            this.addGuias();

            if(this.grilla != ""){
                var gridAlpha = (this.grilla == "none")? 0: parseFloat(this.grilla);
                this.ejeCategorias.renderer.grid.template.strokeOpacity = gridAlpha;
                this.ejeValores.renderer.grid.template.strokeOpacity = gridAlpha;
            }
            if(this.cursor == "none"){
                this.ejeValores.cursorTooltipEnabled = false;
                this.ejeCategorias.cursorTooltipEnabled = false;
            }else{
                this.ejeValores.cursorTooltipEnabled = false;
                // this.ejeCategorias.cursorTooltipEnabled = false;
            }
            if(this.min != "none") this.ejeValores.min = parseInt(this.min);
            if(this.max != "none"){
                this.ejeValores.max = parseInt(this.max);
            }else{
                this.ejeValores.extraMax = 0.2;
            }
            this.listSeries.forEach((elm, indice) => {
                let serie = this.chart.series.push(new am4charts.LineSeries());
                serie.dataFields.valueY = elm;
                if(this.procesar_fechas){
                    serie.dataFields.dateX = this.field_categoria;
                }else{
                    serie.dataFields.categoryX = this.field_categoria;
                }
                serie.tooltip.pointerOrientation = "vertical";
                serie.tooltipText = (this.lc_custom != '')? this.lc_custom: elm + ": {valueY}";
                if(this.grosor != "none") serie.strokeWidth = parseInt(this.grosor);
                if(this.suave) serie.tensionX = 0.9;
                if(this.relleno == 'solido'){
                    serie.fillOpacity = 0.5;
                }else if(this.relleno == 'degradado'){
                    serie.fillOpacity = 1;
                    let gradient = new am4core.LinearGradient();
                    gradient.addColor(this.chart.colors.getIndex(indice), 0.15);
                    gradient.addColor(this.chart.colors.getIndex(indice), 0);
                    serie.fill = gradient;
                }
                if(this.puntos){
                    let bullet = serie.bullets.push(new am4charts.CircleBullet());
                    bullet.circle.fill = am4core.color("#FFF");
                    bullet.circle.strokeWidth = (this.grosor != "none")? parseInt(this.grosor): 1;
                    if(this.lanzarevento != 'none'){
                        bullet.events.on("hit", ev => {
                            let contexto = ev.target.dataItem.dataContext;
                            this.$eventBus.$emit(this.lanzarevento, contexto);
                        });
                    }
                }
                if(this.etiquetas){
                    let tag = serie.bullets.push(new am4charts.LabelBullet());
                    tag.label.dy = -15;
                    tag.label.text = "{valueY}";
                }
                if(this.gradient){
                    serie.fillOpacity = 1;
                    let efecto = new am4core.LinearGradient();
                    efecto.rotation = 90;
                    efecto.addColor(this.chart.colors.getIndex(0), 0.3);
                    efecto.addColor(this.chart.colors.getIndex(0), 0);
                    serie.fill = efecto;
                    serie.tooltip.getFillFromObject = false;
                    serie.tooltip.background.fill = am4core.color("#000");
                }
                this.lineas.push(serie);
            });
            if(this.cursor != 'none'){
                this.chart.cursor = new am4charts.XYCursor();
                // var nivel = (this.cursor == "none")? 0: (this.cursor == "")? 0.6: parseFloat(this.cursor);
                this.chart.cursor.xAxis = this.ejeCategorias;
                this.chart.cursor.lineX.strokeOpacity = 0; //nivel;
                this.chart.cursor.lineY.strokeOpacity = 0; //nivel;
                this.chart.cursor.fullWidthLineX = true;
                this.chart.cursor.lineX.strokeWidth = 0;
                this.chart.cursor.lineX.fill = am4core.color("#8F3985");
                this.chart.cursor.lineX.fillOpacity = 0.1;
            }

            //this.chart.legend = new am4charts.Legend();

            /*var label = this.series.bullets.push(new am4charts.LabelBullet());
            label.label.text = "{valueY.value}";
            label.label.dy = -10;*/
            //this.chart.dataSource.url = this.ruta;
            this.isCreated = true;
        }
    },
    mounted(){
        this.halfsize = parseInt(this.altura)  * 0.5;
        this.setPaleta(this.paleta);
        this.lc_campo_categoria = this.campo_categoria;
        this.lc_campo_valor = this.campo_valor;
        if(this.manual == false){
            this.setCategoria();
            this.listSeries = this.lc_campo_valor.split(',');
            this.createChart();
            this.loadRuta();
        }
    }
}
</script>