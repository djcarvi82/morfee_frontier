<template>
    <div>
        <div v-if="empty_data != '' && hasData && datos.length == 0" class="empty-data alert alert-warning">
            <div class="d-flex align-items-center">
                <i class="fa fa-info-circle fs-3 me-3"></i>
                <p class="mb-0">{{ empty_data }}</p>
            </div>
        </div>
        <div v-if="preloading != 'none' && !hasData" :style="{height: altura + 'px'}">
            <div class="text-center font-24 vertical-align-middle" :style="{'margin-top': halfsize + 'px'}">
                <i class="fa fa-spinner fa-spin"></i> {{ (preloading == '')? "Cargando datos ...": preloading }}
            </div>
        </div>
        <div ref="chartdiv" :class="(preloading != 'none' && !hasData)? 'hide': ''" :style="{height: lc_altura + 'px'}"></div>
        <div class="alert alert-warning mt-2" v-if="overload">
            <div class="d-flex">
                <i class="fa fa-warning me-2"></i>
                <span>Hay demasiados datos para graficar! (Más de 50).</span>
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
        titulo: {type: String, default: ''},
        titulo_eje: {type: String, default: 'none'},
        titulo_categoria: {type: String, default: 'none'},
        altura: {type: String, default: "300"},
        multicolor: {type: Boolean, default: false},
        ordenar: {type: Boolean, default: false},
        redondear: {type: Boolean, default: false},
        apilar: {type: Boolean, default: false},
        leyenda: {type: String, default: 'none'},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'categoria'},
        campo_valor: {type: String, default: 'valor'},
        alfa: {type: String, default: '1'},
        etiquetas: {type: Boolean, default: false},
        lanzarevento: {type: String, default: 'none'},
        muestra: {type: Boolean, default: false},
        preloading: {type: String, default: 'none'},
        min: {type: String, default: "none"},
        max: {type: String, default: "none"},
        paleta: {type: String, default: "basica"},
        grosor: {type: String, default: "none"},
        suave: {type: Boolean, default: false},
        puntos: {type: Boolean, default: false},
        cursor: {type: Boolean, default: false},
        grilla: {type: String, default: '0.15'},
        sin_valores: {type: Boolean, default: false},
        unidad: {type: String, default: '45'},
        altura_minima: {type: String, default: '0'},
        tooltip: {type: Boolean, default: false}, 
        porcentaje: {type: String, default: ''},
        truncar: {type: Boolean, default: false},
        enfocar: {type: Boolean, default: false},
        cebra: {type: Boolean, default: false},
        catsize: {type: String, default: 'none'},
        pretag: {type: String, default: ''},
        empty_data: {type: String, default: ''},    // Hace que se despliegue un alert con un mensaje.
        empty_category: {type: String, default: ''},
        custom: {type: String, default: ''},
        custom_label: {type: String, default: ''}
    },
    data(){
        return {
            lc_altura: 0,
            lc_grilla: 0.1,
            lc_pretag: this.pretag,
            lc_custom: this.custom,
            title: null,
            chart: null,
            datos: [],
            ejeCat: null,
            ejeValores: null,
            listSeries: [],
            boxSeries: [],
            txleyendas: [],
            boxTypes: [],
            custom_color: [],
            tags: [],
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
            overload: false
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
        setFocusBar: function(index){
            let opaque = (index == -1)? 1: 0.3;
            this.chart.series.values[0].columns.values.forEach((elm, i) => {
                if(index == i){
                    elm.fillOpacity = 1;
                }else{
                    elm.fillOpacity = opaque;
                }
            });
        },
        resetFocus: function(){
            this.setFocusBar(-1);
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
        loadRuta: function(){
            if(this.ruta != 'none'){
                axios.get(this.ruta).then(response => {
                    this.setDatos(response.data[this.contexto])
                }).catch(err => {console.log(err)});
            }
        },
        setDatos: function(arg, ptag='none'){
            if(Array.isArray(arg)){
                if(ptag != 'none'){
                    this.lc_pretag = ptag;
                    let mnu = (this.custom_label != '')? this.lc_pretag + this.custom_label: this.lc_pretag + "{valueX}" + this.porcentaje;
                    for(let i = 0; i < this.tags.length; i++){
                        this.tags[i].label.text = mnu; //this.lc_pretag + "{valueX}" + this.porcentaje;
                    }
                }
                if(arg.length > 50){
                    this.overload = true;
                    this.datos = (this.empty_category == '')? arg.slice(0, 50): arg.slice(0, 50).map(elm => {
                        if(elm[this.campo_categoria] === ''){
                            elm[this.campo_categoria] = this.empty_category;
                        }
                        return elm;
                    });
                }else{
                    this.overload = false;
                    this.datos = (this.empty_category == '')? arg: arg.map(elm => {
                        if(elm[this.campo_categoria] === ''){
                            elm[this.campo_categoria] = this.empty_category;
                        }
                        return elm;
                    });
                }
                let ckey = this.listSeries[0];
                if(this.ordenar){
                    this.datos = this.datos.sort((a, b) => a[ckey] - b[ckey]);
                }
                if(this.isCreated){
                    var aux = parseInt(this.unidad);				// h-- ok begin
                    if(this.datos.length > 0 && this.altura_minima != '0' && (this.altura_minima / this.datos.length) > aux) aux = this.altura_minima / this.datos.length;
                    this.lc_altura = this.datos.length * aux + 50;	// h-- ok end
                    this.chart.data = this.datos;
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
        preview: function(){
            var a = ["Colombia", "Brasil", "Argentina", "Perú", "Ecuador", "Venezuela", "Chile", "Paraguay", "Uruguay", "Bolivia", "Japón", "Korea"];
            var b = [];
            let ckey = this.listSeries[0];
            a.forEach(elm => {
                var dt = new Object();
                dt[this.campo_categoria] = elm;
                dt[ckey] = Math.round(Math.random() * 100 + 70);
                b.push(dt);
            });
            this.setDatos(b);
        },
        createChart: function(){
            var colorSet = new am4core.ColorSet();
            colorSet.list = this.getPaleta().map(col => new am4core.color(col));
            this.chart = am4core.create(this.$refs.chartdiv, am4charts.XYChart);
            this.chart.zoomOutButton.disabled = true;
            // this.chart.paddingLeft = 0;
            // this.chart.paddingRight = 0;
            this.chart.colors = colorSet;
            this.chart.data = this.datos;
            if(this.titulo != ''){
                this.title = this.chart.titles.push(new am4core.Label());
                this.title.text = this.titulo;
                this.title.fontSize = 18;
                this.title.marginBottom = 15;
            }
            //this.chart.legend.valueLabels.template.disabled = true;
            // if(this.leyenda != 'none'){
            //     this.chart.legend = new am4charts.Legend();
            //     this.chart.legend.position = (this.leyenda == '')? 'top': this.leyenda;
            //     this.chart.legend.background.fill = am4core.color("#F1F3F4");
            //     this.chart.legend.marginTop = 24;
            // }
            if(this.leyenda == 'hide'){
                // Nafen
            }else if(this.leyenda != 'none'){
                // position | fontSize | markerHeight | color | showValues
                var opt = ['bottom', 12, 14, '#F1F3F4', true];
                this.leyenda.split('|').forEach((elm, i) => opt[i] = elm);
                this.chart.legend = new am4charts.Legend();
                // this.chart.legend.useDefaultMarker = true;

                this.chart.legend.position = opt[0];
                this.chart.legend.labels.template.fontSize = opt[1];
                this.chart.legend.markers.template.height = opt[2];
                this.chart.legend.background.fill = am4core.color(opt[3]);
                if(opt[4] == 'true'){
                    this.chart.legend.valueLabels.template.disabled = true;
                }else{
                    this.chart.legend.valueLabels.template.align = 'right';
                    this.chart.legend.valueLabels.template.textAlign = 'end';
                }
            }else if(this.listSeries.length > 1){
                this.chart.legend = new am4charts.Legend();
                this.chart.legend.position = 'top';
                this.chart.legend.background.fill = am4core.color("#F1F3F4");
                this.chart.legend.marginBottom = 24;
            }
            this.ejeCat = this.chart.yAxes.push(new am4charts.CategoryAxis());	// h-- ok
            this.ejeCat.dataFields.category = this.campo_categoria;
            this.ejeCat.renderer.grid.template.strokeOpacity = this.lc_grilla;
            this.ejeCat.fontFamily = 'Arial';
            this.ejeCat.renderer.minGridDistance = 20;

            this.ejeCat.renderer.ticks.template.disabled = false;
            this.ejeCat.renderer.ticks.template.stroke = am4core.color("#333");
            this.ejeCat.renderer.ticks.template.strokeWidth = 1;
            this.ejeCat.renderer.ticks.template.strokeOpacity = 1;
            this.ejeCat.renderer.line.disabled = false;
            this.ejeCat.renderer.line.strokeOpacity = .5;
            if(this.catsize != 'none'){
                this.ejeCat.renderer.labels.template.fontSize = parseInt(this.catsize);
            }
            if(this.truncar){
                // this.ejeCat.renderer.labels.template.wrap = true;
                this.ejeCat.renderer.labels.template.truncate = true;
                this.ejeCat.renderer.labels.template.maxWidth = 120;
            }
            //this.ejeCat.renderer.grid.template.disabled = true;    Oculta la línea
            if(this.titulo_categoria != 'none'){
                this.ejeCat.title.text = this.titulo_categoria;
            }
            this.ejeCat.renderer.grid.template.location = 0;
            if(this.listSeries.length > 1 && !this.apilar){
                this.ejeCat.renderer.cellStartLocation = 0.1;
                this.ejeCat.renderer.cellEndLocation = 0.9;
            }
            if(this.cebra){
                this.ejeCat.renderer.axisFills.template.disabled = false;
                this.ejeCat.renderer.axisFills.template.fillOpacity = 0.05;
            }
            this.ejeVal = this.chart.xAxes.push(new am4charts.ValueAxis());		// h-- ok
            this.ejeVal.renderer.grid.template.strokeOpacity = this.lc_grilla;
            this.ejeVal.fontFamily = 'Arial';
            this.ejeVal.tooltip.disabled = true;

            if(this.sin_valores){
                this.ejeVal.renderer.labels.template.disabled = true;
            }else{
                this.ejeVal.renderer.ticks.template.disabled = false;
                this.ejeVal.renderer.ticks.template.stroke = am4core.color("#333");
                this.ejeVal.renderer.ticks.template.strokeWidth = 1;
                this.ejeVal.renderer.ticks.template.strokeOpacity = 1;
                this.ejeVal.renderer.line.disabled = false;
                this.ejeVal.renderer.line.strokeOpacity = .5;
            }
            if(this.min != "none") this.ejeVal.min = parseInt(this.min);
            if(this.max != "none"){
                this.ejeVal.max = parseInt(this.max);
            }else{
                this.ejeVal.extraMax = 0.2;
            }
            if(this.titulo_eje != 'none'){
                this.ejeVal.title.text = this.titulo_eje;
            }
            this.listSeries.forEach((elm, indice) => {
                var boxType = this.boxTypes[indice];
                var serie = (boxType == 'columna')? this.chart.series.push(new am4charts.ColumnSeries()): this.chart.series.push(new am4charts.LineSeries());
                serie.name = this.txleyendas[indice];
				serie.dataFields.categoryY = this.campo_categoria;		// h-- ok
				serie.dataFields.valueX = elm;							// h-- ok
                if(boxType == 'columna'){
                    if(this.tooltip){
                        serie.columns.template.tooltipText = this.lc_custom == ''? this.txleyendas[indice] + "\n [bold]{valueX}" + this.porcentaje + "[/]": this.lc_custom;
						serie.tooltip.pointerOrientation = "left";
						serie.columns.template.tooltipX = am4core.percent(100);
						serie.columns.template.tooltipY = am4core.percent(50);
						// serie.tooltip.getFillFromObject = false;
						// serie.tooltip.background.fill = am4core.color("#000");
						serie.tooltip.label.textAlign = "middle";
                        if(this.lanzarevento != 'none'){
                            serie.tooltip.label.interactionsEnabled = true;
                            serie.tooltip.keepTargetHover = true;
                            serie.tooltip.events.on('hit', ev => {
                                let contexto = ev.target.dataItem.dataContext;
                                contexto.campo_categoria = this.campo_categoria;
                                contexto.campo_valor = elm;
                                if(this.empty_category != '' && contexto[this.campo_categoria] == this.empty_category){
                                    contexto[this.campo_categoria] = "";
                                }
                                this.$eventBus.$emit(this.lanzarevento, contexto);
                                if(this.enfocar){
                                    this.setFocusBar(ev.target.dataItem.index);
                                }
                            });
                        }
                    }
                    serie.columns.template.strokeWidth = 0;
                    serie.columns.template.strokeOpacity = 1;
                    if(this.custom_color[indice] != 'void'){
                        serie.columns.template.fill = am4core.color(this.custom_color[indice]);
                        serie.columns.template.stroke = serie.columns.template.fill;
                    }
                    if(this.apilar){
                        serie.stacked = true;
                    }
                    if(this.redondear){
                        serie.columns.template.column.cornerRadiusTopRight = 8;
                        serie.columns.template.column.cornerRadiusBottomRight = 8;
                    }
                    if(this.multicolor && this.listSeries.length == 1){
                        serie.columns.template.adapter.add('fill', (fill, target) => this.chart.colors.getIndex(target.dataItem.index));
                    }
                    serie.columns.template.events.on("hit", ev => {
                        var contexto = ev.target.dataItem.dataContext;
                        if(this._accion != null){
                            this._accion(contexto);
                        }
                        if(this.lanzarevento != 'none'){
                            var tm = contexto;
                            tm.campo_categoria = this.campo_categoria;
                            tm.campo_valor = elm;
                            if(this.empty_category != '' && tm[this.campo_categoria] == this.empty_category){
                                tm[this.campo_categoria] = "";
                            }
                            this.$eventBus.$emit(this.lanzarevento, tm);
                        }
                        if(this.enfocar){
                            this.setFocusBar(ev.target.dataItem.index);
                        }
                    });
                }else if(boxType == 'linea'){
                    if(this.suave) serie.tensionX = 0.77;
                    if(this.grosor != "none") serie.strokeWidth = parseInt(this.grosor);
                    if(this.puntos){
                        var bullet = serie.bullets.push(new am4charts.CircleBullet());
                        bullet.tooltipText = this.txleyendas[indice] + ": {valueY}";
                        bullet.circle.fill = am4core.color("#FFF");
                        bullet.circle.strokeWidth = (this.grosor != "none")? parseInt(this.grosor): 1;
                    }

                }
                if(this.etiquetas){
                    var tag = serie.bullets.push(new am4charts.LabelBullet());
                    if(this.custom != ''){
                        tag.label.text = this.lc_pretag + this.custom;		// h-- ok
                    }else{
                        tag.label.text = this.lc_pretag + "{valueX}" + this.porcentaje;		// h-- ok
                    }
                    //tag.label.fill = am4core.color('#FFFFFF');
                    if(boxType == 'columna'){
                        if(this.apilar){
                            // tag.label.horizontalCenter = 'left';
                            // tag.label.dx = 10;
                            tag.locationX = 0.5;
                            tag.label.truncate = true;
                            tag.label.hideOversized = true;
                            tag.label.fill = am4core.color("#FFFFFF");
                        }else{
                            tag.label.truncate = false;
                            tag.label.hideOversized = false;
                            tag.label.horizontalCenter = 'left';
                            // tag.locationX = 0;
                            tag.label.dx = 6;
                        }
                    }
                    this.tags.push(tag);
                }
                this.boxSeries.push(serie);
            });
            if(this.cursor){
                var cursor = new am4charts.XYCursor();
                this.chart.cursor = cursor;
                cursor.lineX.disabled = true;
                cursor.lineY.disabled = true;
                cursor.behavior = "none";
            }
            this.isCreated = true;
        },
    },
    mounted(){
        this.setPaleta(this.paleta);
        this.lc_grilla = parseFloat(this.grilla);
        this.lc_altura = parseInt(this.altura);
        this.halfsize = this.lc_altura * 0.5;
        this.campo_valor.split(',').forEach(elm => {
            var tm = elm.split(':');
            this.listSeries.push(tm[0]);
            (tm.length > 1)? this.txleyendas.push(tm[1]): this.txleyendas.push(tm[0]);
            if(tm.length > 2){
                if(tm[2].charAt(0) == "#"){
                    this.boxTypes.push(this.getTypeSerie("columna"));
                    this.custom_color.push(tm[2]);
                }else{
                    this.boxTypes.push(this.getTypeSerie(tm[2]));
                    this.custom_color.push('void');
                }
            }else{
                this.boxTypes.push(this.getTypeSerie("columna"));
                this.custom_color.push('void');
            }
        });
        this.createChart();
        this.loadRuta();
        if(this.muestra){
            this.preview();
        }
    }
}
</script>
<style scoped>
    .empty-data ~ div {display: none !important}
</style>