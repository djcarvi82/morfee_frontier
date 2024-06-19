<template>
    <div>
        <div v-if="vista == null">
            <div class="mt-3 mb-3">
                <h5 class="txt-dark mb-0">PRESTACIÓN DE SERVICIOS</h5>
                <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de prestación de servicios</div>
            </div>
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <h6 class="panel-title txt-dark text-bold text-upper mb-0">CONSULTA DE HISTORIA CLÍNICA</h6>
                        <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div :class="'row ' + status">
                            <div class="col-sm-3">
                                <div class="form-group">
                                    <label class="control-label" style="text-transform:none">Tipo de documento:</label>
                                    <select class="form-control" v-model="f_tdoc">
                                        <option value="">Seleccione el tipo...</option>
                                        <option value="CC">CC - Cédula de ciudadanía</option>
                                        <option value="CE">CE - Cédula de extranjería</option>
                                        <option value="PA">PA - Pasaporte</option>
                                        <option value="RC">RC - Registro civil</option>
                                        <option value="TI">Tarjeta de identidad</option>
                                        <option value="AS">Adulto sin identificación</option>
                                        <option value="MS">Menor sin identificación</option>
                                        <option value="NU">Número único de identificación</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-sm-4">
                                <div class="form-group">
                                    <label class="control-label">Documento:</label>
                                    <div class="input-group">
                                        <input type="text" class="form-control" v-model="f_ndoc" @keypress.enter="loadUser">
                                        <span class="input-group-btn">
                                            <button class="btn btn-success" @click="loadUser" :disabled="verifyFields(['f_tdoc', 'f_ndoc']) == false">
                                                <i class="fa fa-search"></i> 
                                                <span class="ms-2">Consultar</span>
                                            </button>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div><!-- End user doc search -->
                        <div class="table-wrap mt-4" v-if="targetUser != null">
                            <div class="table-responsive">
                                <table class="table table-stripped">
                                    <thead>
                                        <tr>
                                            <th>Fecha de consulta:</th>
                                            <th>1er nombre</th>
                                            <th>2do nombre</th>
                                            <th>1er apellido</th>
                                            <th>2do apellido</th>
                                            <th>Fecha de nacimiento</th>
                                            <th>Sexo</th>
                                            <th class="colmin px-4">Acción</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(c, i) in consultas" :key="i">
                                            <td>{{ c.fec }}</td>
                                            <td>{{ targetUser.n1 }}</td>
                                            <td>{{ targetUser.n2 }}</td>
                                            <td>{{ targetUser.a1 }}</td>
                                            <td>{{ targetUser.a2 }}</td>
                                            <td>{{ targetUser.fnac }}</td>
                                            <td>{{ targetUser.sex }}</td>
                                            <td class="text-center">
                                                <a href="javascript:void(0)" @click="setVista(c)" class="btn btn-success py-1 px-2"><i class="fa fa-eye"></i></a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body ismael px-4">
                        <div class="d-flex justify-content-between px-4">
                            <div>
                                <img :src="pathlogo" alt="" height="50">
                            </div>
                            <div>
                                <h4 class="text-bold">INNOVACIÓN ANALÍTICA</h4>
                                <div style="font-size:.75rem">Dirección: Calle 26 # 16A - 63 Local 1 Sincelejo, Sucre</div>
                                <div style="font-size:.75rem">Teléfono: 321 3270697</div>
                            </div>
                            <div>
                                <i class="fa fa-times fs-4" @click="setVista(null)"></i>
                            </div>
                        </div>

                        <div class="py-4 px-4 mt-5" style="border:1px solid #000">
                            <div class="row">
                                <div class="col-sm-4">
                                    <div><span class="text-bold">Fehca de impresión:</span> 2023-02-10</div>
                                    <div><span class="text-bold">Centro de atención:</span> Innovación Analítica</div>
                                    <div><span class="text-bold">Paciente:</span> {{ targetUser.tdoc + ' - ' + targetUser.ndoc }} - {{ targetUser.n1 + ' ' + targetUser.n2 + ' ' + targetUser.a1 + ' ' + targetUser.a2 }}</div>
                                    <div><span class="text-bold">Fecha de nacimiento:</span> {{ targetUser.fnac }}</div>
                                    <div><span class="text-bold">Régimen:</span> {{ targetUser.reg }}</div>
                                    <div><span class="text-bold">Dirección residencia:</span> {{ targetUser.dir }}</div>
                                    <div><span class="text-bold">Teléfono:</span> {{ targetUser.tel }}</div>
                                    <div><span class="text-bold">Ocupación:</span> {{ targetUser.ocu }}</div>
                                    <div><span class="text-bold">Acompañante:</span> {{ targetUser.aco }}</div>
                                    <div><span class="text-bold">Responsable:</span> {{ targetUser.res }}</div>
                                    <div><span class="text-bold">Administradora:</span> {{ targetUser.eps }}</div>
                                </div>
                                <div class="col-sm-4">
                                    <div><span class="text-bold">Fecha de atención:</span> {{ vista.fec }}</div>
                                    <div><span class="text-bold">Nivel:</span> {{ targetUser.niv }}</div>
                                    <div><span class="text-bold">Departamento:</span> {{ targetUser.dep }}</div>
                                    <div><span class="text-bold">Municipio:</span> {{ targetUser.mcp }}</div>
                                </div>
                                <div class="col-sm-4">
                                    <div><span class="text-bold">Sexo:</span> {{ targetUser.sex }}</div>
                                    <div><span class="text-bold">Estado civil:</span> {{ targetUser.eci }}</div>
                                    <div><span class="text-bold">Tipo de vinculación:</span> {{ targetUser.tvin }}</div>
                                    <div><span class="text-bold">&nbsp;</span> &nbsp;</div>
                                </div>
                            </div>
                        </div>
                        <h4 class="mt-4 mb-2 text-bold">HISTORIA CLÍNICA ESPECIALIZADA</h4>
                        <div class="row mb-4">
                            <div class="col-sm-6"><span class="text-bold">Tipo de servicio:</span> {{ vista.tser }}</div>
                            <div class="col-sm-6"><span class="text-bold">Tipo de consulta:</span> {{ vista.tcon }}</div>
                        </div>
                        <span class="text-bold">Descripción</span>
                        <div class="py-4 px-4 mb-4" style="border:1px solid #000">
                            {{ vista.nota }}
                        </div>
                        <div class="py-4 px-4 mb-4" style="border:1px solid #000">
                            <div><span class="text-bold">Datos generales de la consulta:</span> {{ vista.cup }}</div>
                            <div><span class="text-bold">Finalidad consulta:</span> {{ vista.fin }}</div>
                            <div><span class="text-bold">Causa Externa:</span> {{ vista.cau }}</div>
                            <div><span class="text-bold">Tipo diagnóstico principal:</span> {{ vista.tdiag }}</div>
                            <div><span class="text-bold">Diagnóstico principal:</span> {{ vista.diag + ' - ' + vista.diag_tx }}</div>
                        </div>
                        <div class="d-flex justify-content-end" style="margin-top:5rem">
                            <div class="px-5" style="border-top:1px solid #000">
                                <div>{{ vista.med }}</div>
                                <div style="font-size:.75rem">{{ vista.area }}</div>
                                <div style="font-size:.75rem">{{ vista.nreg }}</div>
                            </div>
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
        pathdoc: {type: String, default: ''},
        pathconsulta: {type: String, default: ''},
        pathlogo: {type: String, default: ''},
    },
    data() {
        return {
            vista: null,
			datos: [],
            consultas: [],
            targetUser: null,
            f_tdoc: '',
            f_ndoc: '',
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        setVista: function(arg){
            this.vista = arg;
        },
        verifyFields: function(arr){
            let bool = true;
            arr.forEach(elm => {
                if(bool){
                    if(this.isEmpty(this[elm])){
                        bool = false;
                    }
                }
            });
            return bool;
        },
        loadUser: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                if(this.verifyFields(['f_tdoc', 'f_ndoc'])){
                    this.targetUser = null;
                    let pam = new FormData();
                    pam.append('tdoc', this.f_tdoc);
                    pam.append('ndoc', this.f_ndoc);
                    console.log('Exe user...');
                    axios.post(this.pathdoc, pam).then(res => {
                        if(res.data == null){
                            this.status = this.state.NOMATCH;
                        }else{
                            this.targetUser = res.data;
                            this.status = this.state.LOADED;
                            this.loadConsultas();
                        }
                    }).catch(err => {
                        this.status = this.state.FAILED;
                    });
                }else{
                    this.status = this.state.INI;
                }
            }
        },
        loadConsultas: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                let pam = new FormData();
                pam.append('tdoc', this.f_tdoc);
                pam.append('ndoc', this.f_ndoc);
                axios.post(this.pathconsulta, pam).then(res => {
                    this.consultas = res.data;
                    console.log(res.data);
                    this.status = this.state.LOADED;
                }).catch(err => {
                    this.status = this.state.FAILED;
                });
            }
        },
    },
    mounted() {
        // alert('some');
    }
}
</script>
<style scoped>
    .loading {opacity: .5; pointer-events: none !important; user-select: none !important}
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .ismael {font-family: Arial !important; color:#000 !important; font-size:1.1rem}
</style>
