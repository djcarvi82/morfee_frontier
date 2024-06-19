<template>
    <div>
        <div class="d-flex justify-content-between mt-3 mb-3">
            <div>
                <h5 class="txt-dark mb-0">KPI</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de auditorías</div>
            </div>
            <div :class="'form-group mb-0 ' + cssStatus('none')">
                <div class="input-group">
                    <span class="input-group-btn"><button class="btn btn-default bootstrap-touchspin-down px-2" type="button" @click="selectYear(vigencia--)">-</button></span>
                    <input type="text" class="form-control text-center" style="width:8rem" :value="vigencia" @keydown.prevent.stop>
                    <span class="input-group-btn"><button class="btn btn-default bootstrap-touchspin-up px-2" type="button" @click="selectYear(vigencia++)">+</button></span>
                    <span class="input-group-btn d-none">
                        <button class="btn btn-success">
                            <i class="fa fa-spinner fa-spin" v-if="status == state.LOADING"></i>
                            <i class="fa fa-search" v-else></i> 
                            <!-- <span class="ms-2">Consultar</span> -->
                        </button>
                    </span>
                </div>
            </div>
        </div><!-- End header VIGENCIA -->
        <!-- Begin month's section -->
        <div :class="'row mb-1 ' + cssStatus('none')">
            <div :class="elm.index == month? 'col-sm-1 df-solid': 'col-sm-1 df-opaco'" v-for="(elm, i) in periodos" :key="i">
                <div class="box-month" @click="selectMonth(elm.index)">
                    <a href="javascript:void(0)" class="btn btn-block btn-mes px-2 py-2">
                        <div class="df-success" :style="{'width': elm.px}"></div>
                        <div class="df-tx">
                            <div class="d-flex justify-content-between">
                                <div>{{ elm.mes.slice(0, 3) }}</div>
                                <div>{{ elm.total > 0? elm.px: '' }}</div>
                            </div>
                        </div>
                    </a>
                    <div class="fuse">{{ miles(elm.total) }}</div>
                </div>
            </div>
        </div><!-- End month's section -->
        <!-- Begin days section -->
        <div :class="'btn-group btn-group-justified mb-4 ' + cssStatus('none')">
            <div :class="cssDay(d)" v-for="(d, i) in days" :key="i" @click="selectDay(d)">{{ d }}</div>
        </div><!-- End days section -->
        <div :class="list_mode? 'd-none': 'row'">
            <div class="col-sm-3">
                <div :class="'panel panel-default card-view border ' + cssStatus('f_conci')">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">CIFRA CONCILIADA</h6>
                                <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_conci')" :key="i">{{ sub.label }}</div>
                                <div class="df-subtitle">{{ titles.timer }}</div>
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-torta 
                                ref="gp_conci" 
                                enfocar 
                                alfa="0" 
                                radio="50" 
                                angulo="semi" 
                                area="65" 
                                etiquetas="value" 
                                campo_categoria="_id" 
                                campo_valor="sglo" 
                                campo_color="color" 
                                lanzarevento="evt-conci"
                                custom="<div>{category}: <strong>${value}</strong></div><div>Facturas: <strong>{total}</strong></div>"
                                altura="160"></amchart-torta>
                        </div>
                    </div>
                </div>
                <div :class="'panel panel-default card-view border ' + cssStatus('f_auditor')">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">AUDITORES</h6>
                                <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_auditor')" :key="i">{{ sub.label }}</div>
                                <div class="df-subtitle">{{ titles.timer }}</div>
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-barra-vertical 
                                ref="gp_auditor" 
                                empty_category="(En blanco)" 
                                enfocar 
                                etiquetas 
                                unidad="30" 
                                sin_valores 
                                grilla="0" 
                                paleta="#41AEA9" 
                                campo_categoria="_id" 
                                lanzarevento="evt-auditor"
                                tooltip
                                custom="{valueX} facturas"
                                cursor
                                campo_valor="total"></amchart-barra-vertical>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-7">
                <div :class="'panel panel-default card-view border ' + cssStatus('none')">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">{{ titles.line }}</h6>
                                <div class="df-subtitle" v-for="(sub, i) in getSubtitles('no-apply')" :key="i">{{ sub.label }}</div>
                                <div class="df-subtitle">{{ titles.timer }}</div>
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-linea 
                                ref="g_line" 
                                campo_categoria="_id" 
                                campo_valor="total" 
                                altura="350" 
                                sin_valores 
                                puntos 
                                etiquetas 
                                cursor 
                                paleta="1" 
                                grosor="2" 
                                min="0"
                                lanzarevento="open-point" 
                                suavex
                                rotar
                                custom="{valueY} facturas"
                                gradient
                                procesar_fechas></amchart-linea>
                            <div class="text-center">
                                <button type="button" :class="calday == 0? 'btn btn-success py-1': 'btn btn-default btn-outline py-1'" @click="fillDates(0)">Fecha radicado</button>
                                <button type="button" :class="calday == 20? 'btn btn-success py-1': 'btn btn-default btn-outline py-1'" @click="fillDates(20)">20 días hábiles</button>
                                <button type="button" :class="calday == 25? 'btn btn-success py-1': 'btn btn-default btn-outline py-1'" @click="fillDates(25)">25 días hábiles</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-2">
                <div :class="status_filter + '-static panel panel-default card-view border'">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <h6 class="panel-title txt-dark text-bold text-upper mb-0">ZONA DE FILTROS</h6>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <div class="df-filtro py-1 px-2">
                                <div class="d-flex align-items-center">
                                    <i class="zmdi zmdi-filter-list text-success me-2 fs-5"></i>
                                    <div><div class="df-label">AÑO</div><div>{{ vigencia }}</div></div>
                                </div>
                            </div>
                            <div class="df-filtro py-1 px-2">
                                <div class="d-flex align-items-center">
                                    <i class="zmdi zmdi-filter-list text-success me-2 fs-5"></i>
                                    <div><div class="df-label">MES</div><div>{{ meses[month] }}</div></div>
                                </div>
                            </div>
                            <div class="df-filtro py-1 px-2" v-if="day > 0">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="d-flex align-items-center">
                                        <i class="zmdi zmdi-filter-list text-success me-2 fs-5"></i>
                                        <div><div class="df-label">DÍA</div><div>Del 1 al {{ day }}</div></div>
                                    </div>
                                    <a href="javascript:void(0)" @click="removeFilters('day')">
                                        <i class="fa fa-times text-danger"></i>
                                    </a>
                                </div>
                            </div>
                            <div class="df-filtro py-1 px-2" v-for="(f, i) in filtros" :key="i">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="d-flex align-items-center">
                                        <i class="zmdi zmdi-filter-list text-success me-2 fs-5"></i>
                                        <div>
                                            <div class="df-label">{{ getHumanLabel(f) }}</div>
                                            <div>{{ getHumanFilter(f) }}</div>
                                        </div>
                                    </div>
                                    <a href="javascript:void(0)" @click="removeFilters(f)">
                                        <i class="fa fa-times text-danger"></i>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div :class="'panel panel-default card-view border ' + cssStatus('f_estado')">
                    <div class="panel-heading">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="panel-title txt-dark text-bold text-upper mb-0">ESTADO FACTURAS</h6>
                                <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_estado')" :key="i">{{ sub.label }}</div>
                                <div class="df-subtitle">{{ titles.timer }}</div>
                            </div>
                            <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        </div>
                    </div>
                    <div class="panel-wrapper collapse in">
                        <div class="panel-body">
                            <amchart-barra-vertical 
                                ref="gp_estado" 
                                empty_category="(En blanco)" 
                                enfocar 
                                sin_valores 
                                grilla="0" 
                                etiquetas 
                                unidad="30" 
                                paleta="#41AEA9" 
                                campo_categoria="_id" 
                                tooltip
                                cursor
                                custom="{valueX} facturas"
                                lanzarevento="evt-estado"
                                campo_valor="total"></amchart-barra-vertical>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="list_mode" class="panel panel-default card-view border">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0" v-if="calday == 0">FACTURAS CON FECHA DE RADICADO {{ fixed_at }}</h6>
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0" v-else-if="calday == 20">FACTURAS QUE CUMPLEN CON 20 DÍAS HÁBILES EN LA FECHA {{ fixed_at }}</h6>
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0" v-else-if="calday == 25">FACTURAS QUE CUMPLEN CON 25 DÍAS HÁBILES EN LA FECHA {{ fixed_at }}</h6>
                        <div class="df-subtitle" v-for="(sub, i) in getSubtitles('f_estado')" :key="i">{{ sub.label }}</div>
                    </div>
                    <div>
                        <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                        <a href="javascript:void(0)" class="ms-2" @click="closeList"><i class="zmdi zmdi-close"></i></a>
                    </div>
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <div class="d-flex justify-content-between border-bottom pb-3">
                        <button type="button" class="btn btn-success" @click="loadPage(pagina - 1)" :disabled="pagina <= 1"><i class="zmdi zmdi-arrow-left"></i> Atrás</button>
                        <div>
                            <div class="text-center" style="font-size:1.3rem; font-family:Arial; color:#000">{{ f_total }}</div>
                            <div class="text-center" style="letter-spacing:1px; font-size:11px; font-family:Verdana">Facturas</div>
                        </div>
                        <button type="button" class="btn btn-success" @click="loadPage(pagina + 1)" :disabled="facturas.length < 51">Siguiente <i class="zmdi zmdi-arrow-right"></i></button>
                    </div>
                    <div class="table-wrap">
                        <div class="table-responsive">
                            <table :class="'table table-striped ' + status_filter">
                                <thead>
                                    <tr>
                                        <th class="colmin">No.</th>
                                        <th>Razón social</th>
                                        <th class="colmin">Factura</th>
                                        <th class="colmin">Consecutivo</th>
                                        <th class="colmin">Fecha radicado</th>
                                        <th class="colmin" v-if="calday > 0">{{ calday == 20? '20 días hábiles': '25 días hábiles' }}</th>
                                        <th>Auditor</th>
                                        <th>Estado</th>
                                        <th class="text-center">Valor Neto</th>
                                        <th class="text-center">Acepta EPS</th>
                                        <th class="text-center">Acepta IPS</th>
                                        <th class="text-center">Total Glosa</th>
                                        <th class="text-center">Conciliación</th>
                                        <th class="text-center">Dif. Valores</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(fac, i) in facturas.slice(0, 50)" :key="i">
                                        <td class="py-2">{{ getNumRow(i) }}</td>
                                        <td class="py-2">{{ fac.razon_social }}</td>
                                        <td class="py-2">{{ fac.factura }}</td>
                                        <td class="py-2">{{ fac.consecutivo_radica }}</td>
                                        <td class="py-2">{{ fac.fecha_radicado }}</td>
                                        <td class="py-2" v-if="calday > 0"><span class="label label-success">{{ fixed_at }}</span></td>
                                        <td class="py-2">{{ fac.usuario_auditoria_tecnica }}</td>
                                        <td class="py-2">{{ fac.estado_tecnica }}</td>
                                        <td class="py-2 text-center">{{ miles(fac.valor_neto) }}</td>
                                        <td class="py-2 text-center">{{ miles(fac.valor_total_acepta_eps) }}</td>
                                        <td class="py-2 text-center">{{ miles(fac.valor_total_acepta_ips) }}</td>
                                        <td class="py-2 text-center">{{ miles(fac.total_glosas) }}</td>
                                        <td class="py-2 text-center">
                                            <span class="label label-success" v-if="fac.formi == 'Conciliado'">{{ fac.formi }}</span>
                                            <span class="label label-danger" v-else>{{ fac.formi }}</span>
                                        </td>
                                        <td class="py-2 text-center">{{ miles(altfixed((fac.valor_total_acepta_eps + fac.valor_total_acepta_ips) - fac.total_glosas, 2)) }}</td>
                                    </tr>
                                </tbody>
                                <tfoot v-if="facturas.length > 0">
                                    <tr>
                                        <th :colspan="calday > 0? 13: 12">TOTAL DIFERENCIAS:</th>
                                        <th class="text-center text-bold">{{ totalizer() }}</th>
                                    </tr>
                                </tfoot>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        mimetic: {type: String, default: ''},
		pathdata: {type: String, default: ''}
    },
    data() {
        return {
            // Vars of calc add days...
            festivos: {'2022-01-10': true, '2022-03-21': true, '2022-04-14': true, '2022-04-15': true, '2022-05-30': true, '2022-06-20': true, '2022-06-27': true, '2022-07-04': true, '2022-07-20': true, '2022-08-15': true, '2022-10-17': true, '2022-11-07': true, '2022-11-14': true, '2022-12-08': true, '2023-01-09': true, '2023-03-20': true, '2023-04-06': true, '2023-04-07': true, '2023-05-01': true, '2023-05-22': true, '2023-06-12': true, '2023-06-19': true, '2023-07-03': true, '2023-07-20': true, '2023-08-07': true, '2023-08-21': true, '2023-10-16': true, '2023-11-06': true, '2023-11-13': true, '2023-12-08': true, '2023-12-25': true},
            after20: {},	// {'2023-11-20': true}	Aspect asign...
            after25: {},
            before20: {},
            before25: {},
            lens: {},  // {'2023': {'1': {'len': 31}, '2': {'len': 28} } }
            // End vars calc
            meses: ['', 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            vigencia: new Date().getFullYear(),
            // vigencia: 2022,
            month: 0,
            day: 0,
            f_auditor: '',
            f_estado: '',
            f_conci: '',
            f_fecha: '',
            fixed_at: '',
            f_total: 0,
            pagina: 1,
            pagina_alt: 1,
            list_mode: false,
            human: {'f_auditor': 'AUDITOR', 'f_estado': 'ESTADO', 'f_conci': 'CONCILIACIÓN'},
            subtitles: {'f_auditor': 'Auditor: ', 'f_estado': 'Estado de la factura: ', 'f_conci': 'Estado de conciliación: '},
            calday: 0,  // 0 | 20 | 25
            days: [],
            periodos: [],   // For build box months.
			datos: [],
            fechas: [],     // For build line chart.
            facturas: [],
            filtros: [],
            filter_exe: '',
            titles: {
                'timer': '',
                'line': '',
                'filtros': [],
            },
            status: 'ini',
            status_data: 'ini',
            status_filter: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
        // Section calc dates
        isFestivo: function(day, fecha){
            if(day % 6 == 0) return true; // Day 0 or 6 is festivo! (Sábado y Domingo)
            return (this.festivos[fecha] === true);
        },
        getLen: function(a, m){
            if(this.lens[a] != undefined && this.lens[a][m] != undefined){
                return this.lens[a][m].len;
            }else{
                let len = (m == 12)? new Date(a + 1, 0, 0).getDate(): new Date(a, m, 0).getDate();
                if(this.lens[a] == undefined){
                    this.lens[a] = {};
                    this.lens[a][m] = {'len': len};
                }else{
                    this.lens[a][m] = {'len': len};
                }
                return len;
            }
        },
        totalizer: function(){
            let sum = 0;
            this.facturas.slice(0, 50).forEach(fac => {
                sum += (fac.valor_total_acepta_eps + fac.valor_total_acepta_ips) - fac.total_glosas;
            });
            return this.miles(this.altfixed(sum, 2));
        },
        addDays20: function(fecha, numday=20){
            if(this.swapDay(fecha, numday) != undefined){
                return this.swapDay(fecha, numday);
            }
            let len = null;
            let bi = fecha.split('-').map(tx => parseInt(tx));
            let wday = new Date(bi[0], bi[1] - 1, bi[2]).getDay();
            let day = bi[2];
            let count = 0;
            let date = '';
            while(count < numday){
                if(len != null){
                    if(bi[1] == 12){
                        bi[0]++;
                        bi[1] = 1;
                    }else{
                        bi[1]++;
                    }
                    day = 1;
                }
                len = this.getLen(bi[0], bi[1]);
                let prefix = bi[0] + '-' + `0${bi[1]}`.slice(-2) + '-';
                for(day; day <= len; day++){	// Begin day and end len of month.
                    date = prefix + `0${day}`.slice(-2);
                    if(date != fecha && !this.isFestivo(wday, date)){
                        count++;
                    }
                    if(count == numday){
                        if(numday == 20){
                            if(this.before20[date] == undefined) this.before20[date] = [];
                            this.before20[date].push(fecha);
                            this.after20[fecha] = date;
                        }else if(numday == 25){
                            if(this.before25[date] == undefined) this.before25[date] = [];
                            this.before25[date].push(fecha);
                            this.after25[fecha] = date;
                        }
                        break;
                    }
                    wday = (wday == 6)? 0: wday + 1;
                }
            }
            return this.swapDay(fecha, numday);
        },
        swapDay: function(fecha, num){
            if(num == 20){
                return this.after20[fecha];
            }else if(num == 25){
                return this.after25[fecha];
            }
        },
        // End section calc dates.
        buildTitles: function(){
            this.titles.timer = (this.day == 0)? this.meses[this.month] + ' de ' + this.vigencia: this.meses[this.month] + ' 1 al ' + this.day + ' de ' + this.vigencia;
            this.titles.filtros = [];
            this.filtros.forEach(filtro => {
                this.titles.filtros.push({
                    'name': filtro,
                    'label': this.subtitles[filtro] + this[filtro],
                });
            });
        },
        getSubtitles: function(filtro){
            let sub = [];
            for(let i = 0; i < this.titles.filtros.length; i++){
                if(this.titles.filtros[i].name == filtro){
                    break;
                }else{
                    sub.push(this.titles.filtros[i]);
                }
            }
            return sub;
        },
        rango: function(num){
            let arr = [];
            while(arr.length < num) arr.push(arr.length + 1);
            return arr;
        },
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        miles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        altfixed: function(num, dec=1){
            return (num % 1)? Number.parseFloat(num).toFixed(dec): num;
        },
        cssDay: function(num){
            if(this.day == 0) return 'btn btn-warning py-0 px-2';
            return num <= this.day? 'btn btn-warning py-0 px-2': 'btn btn-default py-0 px-2';
        },
        cssStatus: function(filtro){
            if(this.status_data == this.state.LOADING){
                return 'loading'
            }
            if(this.status_filter == this.state.LOADING){
                if(filtro == 'none'){
                    return 'loading';
                }
                let pos = this.filtros.indexOf(this.filter_exe);
                let local = this.filtros.indexOf(filtro);
                return (local == -1 || local > pos)? 'loading': 'loading-static';
            }
            return '';
        },
        setMonth: function(num){
            this.month = num;
            this.getDays(this.vigencia, this.month);
            return num;
        },
        setDay: function(num){
            this.day = (num == this.days.length)? 0: num;   // 0 equal all month...
        },
        getDays: function(a, m){    // Real notation
            if(m == 12){
                a++;
                m = 0;
            }
            let len = new Date(a, m, 0).getDate();
            this.days = this.rango(len);
            this.setDay(0);
        },
        getHumanLabel: function(arg){
            return this.human[arg];
        },
        getHumanFilter: function(arg){
            return (this[arg] == "")? "(En blanco)": this[arg];
        },
        getNumRow: function(i){
            return (this.pagina_alt - 1) * 50 + (i + 1);
        },
        loadData: function(){
            if(this.status_data != this.state.LOADING){
                this.status_data = this.state.LOADING;
                let pam = new FormData();
                pam.append('vigencia', this.vigencia);
                let tm = {};
                this.meses.slice(1).forEach((elm, i) => {
                    let ike = i + 1;
                    tm[ike] = {'per': this.vigencia + '-' + ike.toString().padStart(2, '0'), 'suma': 0, 'diff': 0, 'equal': 0, 'total': 0, 'px': 0, 'index': ike, 'mes': elm};
                });
                axios.post(this.pathdata, pam).then(res => {
                    res.data[0].monthead.forEach(elm => {
                        let index = parseInt(elm._id.per.split('-')[1]);
                        tm[index][elm._id.formi] += elm.sglo;
                        tm[index].suma += elm.sglo;
                        tm[index].total += elm.total;
                    });
                    this.periodos = Object.values(tm).map(elm => {
                        // let aux = (elm.suma == 0)? 0: (elm.equal / elm.suma) * 100;
                        let aux = (elm.suma == 0)? 0: (elm.equal / elm.suma) * 100;
                        elm.px = this.altfixed(aux) + '%';// (elm.suma == 0)? 0 + '%': ((elm.equal / elm.suma) * 100).toString() + '%';
                        return elm;
                    });
                    let yx = new Date().getFullYear();
                    let mx = 1;
                    if(this.vigencia == yx){
                        mx = new Date().getMonth() + 1;
                    }else if(this.vigencia < yx){
                        mx = 12;
                    }
                    this.status_data = this.state.LOADED;
                    this.loadControl(this.vigencia, this.setMonth(mx), 0);
                }).catch(err => {
                    this.status_data = this.state.FAILED;
                    console.log(err);
                });
            }
        },
        loadControl: function(anio, mes, dia){
            if(this.status_data != this.state.LOADING){
                this.status_data = this.state.LOADING;
                let pam = new FormData();
                pam.append('vigencia', anio);
                pam.append('mes', mes);
                pam.append('dia', dia);
                axios.post(this.pathdata + '/control', pam).then(res => {
                    this.fechas = res.data[0].fechas;
                    this.$refs.gp_conci.setDatos(res.data[0].periodo.map(elm => {
                        elm.color = (elm._id == 'Conciliado')? '#16C79A': '#FD5D5D';    // 41AEA9
                        return elm;
                    }));
                    this.$refs.gp_estado.setDatos(res.data[0].estado);
                    this.$refs.gp_auditor.setDatos(res.data[0].auditor.sort((a, b) => a.total - b.total));
                    this.fillDates();   // Llena la gráfica de líneas...
                    this.buildTitles();
                    this.status_data = this.state.LOADED;
                }).catch(err => {
                    this.status_data = this.state.FAILED;
                });
            }
        },
        loadControlFilter: function(filtername){
            if(this.status_filter != this.state.LOADING){
                this.status_filter = this.state.LOADING;
                this.filter_exe = filtername;
                let pam = new FormData();
                pam.append('vigencia', this.vigencia);
                pam.append('mes', this.month);
                pam.append('dia', this.day);
                this.filtros.forEach(elm => {
                    if(this[elm] == ""){
                        pam.append(elm, "-empty-") 
                    }else{
                        pam.append(elm, this[elm]) 
                    }
                });
                axios.post(this.pathdata + '/control', pam).then(res => {
                    this.fechas = res.data[0].fechas;
                    this.fillDates();
                    ['f_auditor', 'f_estado', 'f_conci'].forEach(elm => {
                        if(this.filtros.some(fto => fto == elm)){

                        }else{
                            if(elm == 'f_auditor'){
                                this.$refs.gp_auditor.setDatos(res.data[0].auditor.sort((a, b) => a.total - b.total));
                            }else if(elm == 'f_estado'){
                                this.$refs.gp_estado.setDatos(res.data[0].estado);
                            }else if(elm == 'f_conci'){
                                this.$refs.gp_conci.setDatos(res.data[0].periodo.map(elm => {
                                    elm.color = (elm._id == 'Conciliado')? '#16C79A': '#FD5D5D';    // 41AEA9
                                    return elm;
                                }));
                            }
                        }
                    });
                    this.buildTitles();
                    this.status_filter = this.state.LOADED;
                }).catch(err => {
                    this.status_filter = this.state.FAILED;
                });
            }
        },
        loadFechas: function(fcas, page=1){ // fcas is string dates separate with | (pipe)
            if(this.status_filter != this.state.LOADING){
                this.status_filter = this.state.LOADING;   
                this.list_mode = true;
                this.pagina = page;
                this.filter_exe = 'no-apply';
                let pam = new FormData();
                pam.append('vigencia', this.vigencia);
                pam.append('mes', this.month);
                pam.append('dia', this.day);
                this.filtros.forEach(elm => {
                    if(this[elm] == ""){
                        pam.append(elm, "-empty-") 
                    }else{
                        pam.append(elm, this[elm]) 
                    }
                });
                pam.append('fechas', fcas);
                pam.append('pagina', this.pagina);
                axios.post(this.pathdata + '/control/fechas', pam).then(res => {
                    console.log('mis fechas!');
                    console.log(res.data);
                    this.facturas = res.data[0].facturas;
                    this.pagina_alt = this.pagina;
                    this.status_filter = this.state.LOADED;
                }).catch(err => {
                    this.status_filter = this.state.FAILED;
                });
            }
        },
        loadPage: function(pretend){
            if(this.status_filter != this.state.LOADING){
                if(pretend < 1){
                    pretend = 1;
                }
                this.loadFechas(this.f_fecha, pretend);
            }
        },
        fillDates: function(cdy=1){
            if([0, 20, 25].includes(cdy)){
                this.calday = cdy;
            }
            if(this.calday == 0){
                this.$refs.g_line.setDatos(this.fechas, "#0093AB");
                this.titles.line = 'NÚMERO DE FACTURAS SEGÚN FECHA DE RADICACIÓN';
            }else{
                this.titles.line = (this.calday == 20)? 'NÚMERO DE FACTURAS SEGÚN FECHA LÍMITE DE 20 DÍAS': 'NÚMERO DE FACTURAS SEGÚN FECHA LÍMITE DE 25 DÍAS';
                let mycolor = (this.calday == 20)? "#17B978": "#DD4A48"
                let tm = {};
                this.fechas.forEach(elm => {
                    let fx = this.addDays20(elm._id, this.calday);
                    if(tm[fx] == undefined){
                        tm[fx] = {'_id': fx, 'total': 0};
                    }
                    tm[fx].total += elm.total;
                });
                this.$refs.g_line.setDatos(Object.values(tm), mycolor);
                console.log('Los 20:');
                console.log(this.after20);
                console.log('Los 25:');
                console.log(this.after25);
            }
        },
        closeList: function(){
            this.list_mode = false;
            this.facturas = [];
        },
        selectMonth: function(num){
            this.setMonth(num);
            this.filtros = [];
            this.closeList();
            this.loadControl(this.vigencia, this.month, 0);
        },
        selectYear: function(vgc){
            this.filtros = [];
            this.closeList();
            this.loadData();
        },
        selectDay: function(num){
            this.setDay(num);
            this.filtros = [];
            this.closeList();
            this.loadControl(this.vigencia, this.month, this.day);
        },
        updateFilters: function(arg){
            let pos = this.filtros.findIndex(elm => elm == arg) + 1;
            if(pos > 0){
                this.filtros.splice(pos, 10);
            }else{
                this.filtros.push(arg);
            }
            this.loadControlFilter(arg);
        },
        removeFilters: function(arg){   // Es invocado en la 
            if(arg == 'day'){
                this.selectDay(0);
            }else{
                let pos = this.filtros.findIndex(elm => elm == arg);
                this.filtros.splice(pos, 10);
                this.loadControlFilter('no-apply');
            }
        },
        listen: function(){
            this.$eventBus.$on('evt-auditor', arg => {
                this.f_auditor = arg._id;
                this.updateFilters('f_auditor');
            });
            this.$eventBus.$on('evt-estado', arg => {
                this.f_estado = arg._id;
                this.updateFilters('f_estado');
            });
            this.$eventBus.$on('evt-conci', arg => {
                this.f_conci = arg._id;
                this.updateFilters('f_conci');
            });
            this.$eventBus.$on('open-point', arg => {
                this.f_fecha = arg._id;
                this.fixed_at = arg._id;
                this.f_total = arg.total;
                if(this.calday == 20){
                    this.f_fecha = this.before20[arg._id].join('|');
                }else if(this.calday == 25){
                    this.f_fecha = this.before25[arg._id].join('|');
                }
                this.loadFechas(this.f_fecha, 1);
            });
        }
    },
    mounted() {
        this.listen();
        this.getDays(this.vigencia, this.month);
        this.loadData();
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .btn-mes {position:relative; border:none; background:linear-gradient(#FFFFFF, #EAEAEA) !important; font-family: Arial; font-size:.75rem; color:#000; letter-spacing: 1px}
    .btn-mes .df-success {position:absolute; top:0; bottom:0; left:0; background:#17B978; z-index: 100}
    .btn-mes .df-tx {position:relative; z-index: 1000}
    .day {background:#000; color:#FFF; padding: .2rem .5rem; font-size:11px; font-family: Verdana; letter-spacing: 2px; text-align: center}
    .df-opaco {opacity: .45}
    .df-filtro {background:#FCFCFC; border:1px solid #DDD}
    .df-filtro + .df-filtro {border-top:1px solid #FFF}
    .df-label {font-size:10px; font-family: Verdana; letter-spacing: 1px; color:#000 !important}
    .df-subtitle {font-size:.8rem; letter-spacing: 1px; color:#000}
    .loading {opacity: .45; pointer-events: none}
    .loading-static {pointer-events: none !important; user-select: none !important; cursor: wait !important}
    .col-sm-1.df-opaco:hover {opacity: .7}
    .row > .col-sm-1 {padding-left: 5px; padding-right: 5px}
    .row > .col-sm-1:first-child {padding-left: 15px}
    .row > .col-sm-1:last-child {padding-right: 15px}
    .fuse {letter-spacing:2px; font-family: Verdana; font-size:11px; text-align: center; background:#000; border-top:1px solid #000; color:#FFF; padding-top:0.1rem; padding-bottom:0.1rem; user-select: none; cursor: pointer}
    .df-opaco > .fuse {background:#999; border-top-color:#999}
    .df-solid .fuse {background:#F0C541; padding-top:8px; padding-bottom: 8px}
    .box-month {border:1px solid #000}
    /* .col-sm-1.df-opaco:hover > .fuse {background: #F0C541; color:#000} */
    .box-filter {border:2px dashed #DDD; background:#FCFCFC}
</style>
