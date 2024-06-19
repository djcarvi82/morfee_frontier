<template>
    <div>
        daniel  asdjfkqlweruoiqwer 
        <div v-if="preloading != 'none' && !hasData" :style="{height: altura + 'px'}">
            <div class="text-center font-24 vertical-align-middle" :style="{'margin-top': halfsize + 'px'}">
                <i class="fa fa-spinner fa-spin"></i> {{ (preloading == '')? "Cargando datos ...": preloading }}
            </div>
        </div>
        <div :id="keyname" :class="(preloading != 'none' && !hasData)? 'hide': ''" :style="{height: lc_altura + 'px'}"></div>
    </div>
</template>
<script>
import * as am4core from "@amcharts/amcharts4/core";
import * as am4charts from "@amcharts/amcharts4/charts";

export default {
    props: {
        altura: {type: String, default: 'auto'},
        colores: {type: String, default: '#67B7DC,#A367DC'},
        agrupar: {type: String, default: '0'},
        ruta: {type: String, default: 'none'},
        contexto: {type: String, default: 'datos'},
        campo_categoria: {type: String, default: 'edad'},
        campo_hombre: {type: String, default: 'male'},
        campo_mujer: {type: String, default: 'female'},
        etiquetas: {type: Boolean, default: false},
        lanzarevento: {type: String, default: 'none'},
        muestra: {type: Boolean, default: false},
        preloading: {type: String, default: 'none'},
    },
    data(){
        return {
            keyname: '_am4_' + Math.random().toString().replace("0.", ""),
            lc_agrupar: 0,
            lc_grupos: [],
            lc_campo_categoria: '',
            lc_altura: '0',
            lc_colores: [],
            mainContainer: null,
            maleChart: null,
            femaleChart: null,
            maleColor: '',
            femaleColor: '',
            chart: null,
            datos: [],
            _accion: null,
            hasData: false,
            halfsize: 0,
            isCreated: false
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
        detectPatron: function(ref){
            var pass = true;
            ['count', '_id'].forEach(prop => {
                if(pass){
                    if(ref.hasOwnProperty(prop)){
                        if(prop == '_id'){
                            pass = ref._id.hasOwnProperty('edad') && ref._id.hasOwnProperty('genero');
                        }
                    }else{
                        pass = false;
                    }
                }
            });
            return pass;
        },
        parseData: function(customData){
            let namekey = {"F": this.campo_mujer, "M": this.campo_hombre};
            let memory = {};
            customData.forEach(elm => {
                if(memory[elm._id.edad] == undefined){
                    memory[elm._id.edad] = {};
                    memory[elm._id.edad][this.campo_categoria] = elm._id.edad;
                    memory[elm._id.edad][this.campo_mujer] = 0;
                    memory[elm._id.edad][this.campo_hombre] = 0;
                }
                memory[elm._id.edad][namekey[elm._id.genero]] += elm.count;
            });
            return Object.values(memory);
        },
        setDatos: function(arg){
            this.datos = [];
            if(arg.length > 0 && this.detectPatron(arg[0])){
                this.createGroups(this.parseData(arg));
            }else{
                this.createGroups(arg);
            }
            this.hasData = true;
        },
        createGroups: function(arg){
            //FORMAT GROUPS: 0:5:De 0 a 5|6:15:De 6 a 15 años       <from>:<to>:<label>
            let kys = [];
            let tmp = {};
            if(this.lc_agrupar > 0){
                let base = 0;
                arg.forEach(elm => {
                    base = Math.floor(parseInt(elm[this.campo_categoria])/this.lc_agrupar) * this.lc_agrupar;
                    elm['label_group'] = base + ' a ' + (base + (this.lc_agrupar - 1));
                    elm['_orden_'] = base;
                    if(tmp[base] == undefined){
                        tmp[base] = elm;
                    }else{
                        tmp[base][this.campo_hombre] += elm[this.campo_hombre];
                        tmp[base][this.campo_mujer] += elm[this.campo_mujer];
                    }
                    if(kys.indexOf(base) == -1) kys.push(base);
                });
                kys.sort((a, b) => a - b);
                kys.forEach(elm => {
                    this.datos.push(tmp[elm]);
                });
                if(this.altura == 'auto'){
                    this.lc_altura = (kys.length * 24 + 30).toString();
                }
            }else if(this.lc_grupos.length > 0){
                let next = true;
                let sumData = (ix, el) => {
                    if(tmp[ix] == undefined){
                        tmp[ix] = el;
                    }else{
                        tmp[ix][this.campo_hombre] += el[this.campo_hombre];
                        tmp[ix][this.campo_mujer] += el[this.campo_mujer];
                    }
                };
                arg.forEach(elm => {
                    next = true;
                    var ax = parseInt(elm[this.campo_categoria]);
                    this.lc_grupos.forEach((grupo, indice) => {
                        if(next){
                            if(grupo.from == grupo.to && ax >= grupo.from){
                                elm['label_group'] = grupo.label;
                                elm['_orden_'] = indice;
                                sumData(indice, elm);
                                next = false;
                            }else if(ax >= grupo.from && ax <= grupo.to){
                                elm['label_group'] = grupo.label;
                                elm['_orden_'] = indice;
                                sumData(indice, elm);
                                next = false;
                            }
                        }
                    });
                });
                for(var i in tmp){
                    this.datos.push(tmp[i]);
                }
                this.datos.sort((a, b) => a._orden_ - b._orden_);
                if(this.altura == 'auto'){
                    this.lc_altura = (this.lc_grupos.length * 24 + 30).toString();
                }
            }else{
                this.datos = arg;
            }
            if(this.isCreated){
                this.maleChart.data = this.datos;
                this.femaleChart.data = this.datos;
            }
        },
        preview: function(){
            var lts = [];
            for(var i = 0; i < 100; i++){
                lts.push({
                    'edad': i,
                    'male': Math.round(Math.random() * 80),
                    'female': Math.round(Math.random() * 80)
                });
            }
            this.setDatos(lts);
        },
        createChart: function(){
            this.mainContainer = am4core.create(this.keyname, am4core.Container);
            this.mainContainer.width = am4core.percent(100);
            this.mainContainer.height = am4core.percent(100);
            this.mainContainer.layout = "horizontal";

            /* HOMBRES */
            this.maleChart = this.mainContainer.createChild(am4charts.XYChart);
            this.maleChart.paddingRight = 0;
            this.maleChart.data = this.datos;

            let maleEjeCategoria = this.maleChart.yAxes.push(new am4charts.CategoryAxis());
            maleEjeCategoria.dataFields.category = this.lc_campo_categoria;
            maleEjeCategoria.renderer.grid.template.location = 0;
            maleEjeCategoria.renderer.minGridDistance = 15;
            //maleEjeCategoria.renderer.cellStartLocation = 0.1;
            //maleEjeCategoria.renderer.cellEndLocation = 0.9;
            maleEjeCategoria.fontFamily = 'Arial';

            let maleEjeValor = this.maleChart.xAxes.push(new am4charts.ValueAxis());
            maleEjeValor.renderer.inversed = true;
            maleEjeValor.min = 0;
            maleEjeValor.max = 60;
            maleEjeValor.strictMinMax = true;
            maleEjeValor.numberFormatter = new am4core.NumberFormatter();
            maleEjeValor.numberFormatter.numberFormat = "#.#'%'";
            maleEjeValor.fontFamily = 'Arial';
            //maleEjeValor.title.text = 'Hombres';
            
            let maleSeries = this.maleChart.series.push(new am4charts.ColumnSeries());
            maleSeries.dataFields.categoryY = this.lc_campo_categoria;
            maleSeries.dataFields.valueX = this.campo_hombre;
            maleSeries.dataFields.valueXShow = "percent";
            maleSeries.calculatePercent = true;
            maleSeries.fill = am4core.color(this.maleColor);
            maleSeries.stroke = maleSeries.fill;
            maleSeries.interpolationDuration = 1000;
            maleSeries.columns.template.tooltipText = "Hombres: {valueX} ({valueX.percent.formatNumber('#.0')}%)";

            /* MUJERES */
            this.femaleChart = this.mainContainer.createChild(am4charts.XYChart);
            this.femaleChart.paddingLeft = 0;
            this.femaleChart.data = this.datos;

            let femaleEjeCategoria = this.femaleChart.yAxes.push(new am4charts.CategoryAxis());
            femaleEjeCategoria.dataFields.category = this.lc_campo_categoria;
            femaleEjeCategoria.renderer.opposite = true;
            femaleEjeCategoria.renderer.grid.template.location = 0;
            femaleEjeCategoria.renderer.minGridDistance = 15;
            //femaleEjeCategoria.renderer.cellStartLocation = 0.1;
            //femaleEjeCategoria.renderer.cellEndLocation = 0.9;
            femaleEjeCategoria.fontFamily = 'Arial';

            let femaleEjeValor = this.femaleChart.xAxes.push(new am4charts.ValueAxis());
            femaleEjeValor.min = 0;
            femaleEjeValor.max = 60;
            femaleEjeValor.strictMinMax = true;
            femaleEjeValor.numberFormatter = new am4core.NumberFormatter();
            femaleEjeValor.numberFormatter.numberFormat = "#.#'%'";
            femaleEjeValor.renderer.minLabelPosition = 0.01;
            femaleEjeValor.fontFamily = 'Arial';
            //femaleEjeValor.title.text = 'Mujeres';

            let femaleSeries = this.femaleChart.series.push(new am4charts.ColumnSeries());
            femaleSeries.dataFields.categoryY = this.lc_campo_categoria;
            femaleSeries.dataFields.valueX = this.campo_mujer;
            femaleSeries.dataFields.valueXShow = "percent";
            femaleSeries.calculatePercent = true;
            femaleSeries.fill = am4core.color(this.femaleColor);
            femaleSeries.stroke = femaleSeries.fill;
            femaleSeries.columns.template.tooltipText = "Mujeres: {valueX} ({valueX.percent.formatNumber('#.0')}%)";
            femaleSeries.interpolationDuration = 1000;

            /* TAGS/ETIQUETAS */
            if(this.etiquetas){
                let maleTag = maleSeries.bullets.push(new am4charts.LabelBullet());
                maleTag.label.text = "{valueX}";
                maleTag.label.truncate = false;
                maleTag.label.horizontalCenter = "right";
                maleTag.label.dx = -10;


                let femaleTag = femaleSeries.bullets.push(new am4charts.LabelBullet());
                femaleTag.label.text = "{valueX}";
                femaleTag.label.truncate = false;
                femaleTag.label.horizontalCenter = "left";
                femaleTag.label.dx = 10;
            }

            this.maleChart.events.on("datavalidated", evt => {
                let chart = evt.target;
                let ajuste = parseInt(this.lc_altura) - chart.yAxes.getIndex(0).pixelHeight;
                let targetHeight = chart.pixelHeight + ajuste;
                chart.svgContainer.htmlElement.style.height = targetHeight + 'px';
            });
            this.isCreated = true;
        }
    },
    mounted(){
        this.lc_altura = this.altura;
        this.halfsize = this.lc_altura * 0.5;
        if(/:/.test(this.agrupar)){
            /* <from>:<to>:<label> */
            this.agrupar.split("|").forEach(group => {
                var aux = group.split(":");
                var gp = {'from': 0, 'to': 0, 'label': ''};
                gp.from = parseInt(aux[0]);
                gp.to = (aux.length >= 2 && aux[1] != '')? parseInt(aux[1]): gp.from;
                if(aux.length >= 3){
                    gp.label = aux[2];
                }else{
                    gp.label = (gp.from == gp.to)? gp.from.toString() + ' o más': gp.from.toString() + ' a ' + gp.to.toString();
                }
                this.lc_grupos.push(gp);
            });
            this.lc_campo_categoria = 'label_group';
        }else{
            this.lc_agrupar = parseInt(this.agrupar);
            this.lc_campo_categoria = (this.lc_agrupar > 0)? 'label_group': this.campo_categoria;
        }
        this.lc_colores = this.colores.split(',');
        if(this.lc_colores.length >= 2){
            this.maleColor = this.lc_colores[0];
            this.femaleColor = this.lc_colores[1];
        }else if(this.lc_colores.length == 1){
            this.maleColor = this.lc_colores[0];
            this.femaleColor = '#A367DC';
        }else{
            this.maleColor = '#67B7DC';
            this.femaleColor = '#A367DC';
        }
        if(this.muestra){
            this.preview();
        }
        this.createChart();
        this.loadRuta();
    }
}
</script>
