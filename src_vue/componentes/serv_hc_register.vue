<template>
    <div>
        <div class="mt-3 mb-3">
            <h5 class="txt-dark mb-0">PRESTACIÓN DE SERVICIOS</h5>
            <div style="letter-spacing:3px; color:#555; font:12px Arial">Módulo de prestación de servicios</div>
        </div>
        <div class="panel panel-default card-view border">
            <div class="panel-heading">
                <div class="d-flex justify-content-between">
                    <h6 class="panel-title txt-dark text-bold text-upper mb-0">REGISTRO DE HISTORIA CLÍNICA</h6>
                    <a href="javascript:void(0)" class="full-screen"><i class="zmdi zmdi-fullscreen"></i></a>
                </div>
            </div>
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <div v-if="status_con == state.SUCCESS">
                        <div class="alert alert-success">
                            <div class="d-flex align-items-center">
                                <i class="fa fa-check fs-3 me-3"></i>
                                <span>Consulta guardada satisfactoriamente!</span>
                            </div>
                        </div>
                        <button class="btn btn-success" type="button" @click="resetear"><i class="fa fa-arrow-left"></i> Atrás</button>
                    </div>
                    <div class="" v-else-if="['loaded', 'nomatch'].includes(status)">
                        <div v-if="status == state.LOADED">
                            <div class="table-wrap">
                                <div class="table-responsive">
                                    <table class="table table-bordered table-df">
                                        <thead>
                                            <tr>
                                                <th>Tipo de documento</th>
                                                <th>Documento</th>
                                                <th>1er nombre</th>
                                                <th>2do nombre</th>
                                                <th>1er apellido</th>
                                                <th>2do apellido</th>
                                                <th>Fecha de nacimiento</th>
                                                <th>Sexo</th>
                                                <th>Estado civil</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>{{ f_tdoc }}</td>
                                                <td>{{ f_ndoc }}</td>
                                                <td>{{ f_n1 }}</td>
                                                <td>{{ f_n2 }}</td>
                                                <td>{{ f_a1 }}</td>
                                                <td>{{ f_a2 }}</td>
                                                <td>{{ f_fnac }}</td>
                                                <td>{{ f_sex }}</td>
                                                <td>{{ f_eci }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <table class="table table-bordered table-df">
                                        <thead>
                                            <tr><th>Dirección</th><th>Teléfono</th><th>Departamento</th><th>Municipio</th><th>Régimen</th><th>Nivel</th><th>Ocupación</th><th>Administradora</th></tr>
                                        </thead>
                                        <tbody>
                                            <tr><td>{{ f_dir }}</td><td>{{ f_tel }}</td><td>{{ f_dep }}</td><td>{{ f_mcp }}</td><td>{{ f_reg }}</td><td>{{ f_niv }}</td><td>{{ f_ocu }}</td><td>{{ f_eps }}</td></tr>
                                        </tbody>
                                    </table>
                                    <table class="table table-bordered table-df">
                                        <thead>
                                            <tr><th>Tipo vinculación</th><th>Acompañante</th><th>Teléfono acompañante</th><th>Responsable</th><th>Teléfono responsable</th><th>Parentesco responsable</th></tr>
                                        </thead>
                                        <tbody>
                                            <tr><td>{{ f_tvin }}</td><td>{{ f_aco }}</td><td>{{ f_aco_tel }}</td><td>{{ f_res }}</td><td>{{ f_res_tel }}</td><td>{{ f_res_par }}</td></tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        <div v-else>
                            <div class="py-4 px-4 mb-4" style="background:#F5F5F5; border:1px solid #DDD">
                                <div class="row">
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Tipo de documento:</label>
                                            <input type="text" class="form-control" :value="f_tdoc" disabled>
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Documento:</label>
                                            <input type="text" class="form-control" :value="f_ndoc" disabled>
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">1er nombre:</label>
                                            <input type="text" class="form-control" v-model="f_n1">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">2do nombre:</label>
                                            <input type="text" class="form-control" v-model="f_n2">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">1er apellido:</label>
                                            <input type="text" class="form-control" v-model="f_a1">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">2do apellido:</label>
                                            <input type="text" class="form-control" v-model="f_a2">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Nacimiento:</label>
                                            <input type="date" class="form-control" v-model="f_fnac">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Sexo:</label>
                                            <select class="form-control" v-model="f_sex">
                                                <option value="">...</option>
                                                <option value="F">Femenino</option>
                                                <option value="M">Masculino</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Estado civil:</label>
                                            <input type="text" class="form-control" v-model="f_eci">
                                        </div>
                                    </div>
                                    <div class="col-sm-4">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Dirección:</label>
                                            <input type="text" class="form-control" v-model="f_dir">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Teléfono:</label>
                                            <input type="text" class="form-control" v-model="f_tel">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Departamento:</label>
                                            <input type="text" class="form-control" v-model="f_dep">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Municipio:</label>
                                            <input type="text" class="form-control" v-model="f_mcp">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Régimen:</label>
                                            <input type="text" class="form-control" v-model="f_reg">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Nivel:</label>
                                            <input type="text" class="form-control" v-model="f_niv">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Ocupación:</label>
                                            <input type="text" class="form-control" v-model="f_ocu">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Administradora:</label>
                                            <input type="text" class="form-control" v-model="f_eps">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Vinculación:</label>
                                            <input type="text" class="form-control" v-model="f_tvin">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Acompañante:</label>
                                            <input type="text" class="form-control" v-model="f_aco">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Tel. acompañante:</label>
                                            <input type="text" class="form-control" v-model="f_aco_tel">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Responsable:</label>
                                            <input type="text" class="form-control" v-model="f_res">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Tel. responsable:</label>
                                            <input type="text" class="form-control" v-model="f_res_tel">
                                        </div>
                                    </div>
                                    <div class="col-sm-2">
                                        <div class="form-group">
                                            <label class="control-label" style="text-transform:none">Parentesco responsable:</label>
                                            <input type="text" class="form-control" v-model="f_res_par">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <h6 class="panel-title txt-dark text-bold text-upper mt-4 mb-3">DATOS ESPECÍFICOS DE LA CONSULTA</h6>
                        <div class="py-4 px-4 mb-4" style="background:#F5F5F5; border:1px solid #DDD">
                            <div class="row">
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Fecha de consulta:</label>
                                        <input type="date" class="form-control" v-model="k_fec">
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Tipo de servicio:</label>
                                        <select class="form-control" v-model="k_tser">
                                            <option value="">Seleccione el tipo de servicio...</option>
                                            <option value="Medicina General">Medicina General</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Tipo de consulta:</label>
                                        <select class="form-control" v-model="k_tcon">
                                            <option value="">Seleccione el tipo de consulta...</option>
                                            <option value="1ra vez">1ra vez</option>
                                            <option value="Control">Control</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="control-label">Descripción:</label>
                                <textarea rows="5" class="form-control" v-model="k_nota"></textarea>
                            </div>
                            <div class="row">
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Datos generales de la consulta:</label>
                                        <input type="text" class="form-control" v-model="k_cup">
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Finalidad de la consulta:</label>
                                        <input type="text" class="form-control" v-model="k_fin">
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Causa externa:</label>
                                        <input type="text" class="form-control" v-model="k_cau">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Tipo de diagnóstico principal:</label>
                                        <input type="text" class="form-control" v-model="k_tdiag">
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Código diagnóstico principal (CIE-10):</label>
                                        <input type="text" class="form-control" v-model="k_diag">
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Descripción diagnóstico principal (CIE-10):</label>
                                        <input type="text" class="form-control" v-model="k_diag_tx">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Médico:</label>
                                        <input type="text" class="form-control" v-model="k_med">
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Área:</label>
                                        <input type="text" class="form-control" v-model="k_area">
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="form-group">
                                        <label class="control-label" style="text-transform:none">Número de registro:</label>
                                        <input type="text" class="form-control" v-model="k_nreg">
                                    </div>
                                </div>
                            </div>
                        </div><!-- End zona gris form -->
                        <div class="d-flex justify-content-between">
                            <button class="btn btn-success" type="button" @click="resetear"><i class="fa fa-arrow-left"></i> Atrás</button>
                            <button class="btn btn-success" type="button" @click="saveConsulta" :disabled="verifyFields(campos_con.map(m => 'k_' + m)) == false"><i class="fa fa-check"></i> Guardar consulta</button>
                        </div>
                    </div>
                    <div v-else>
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
                    </div>
                </div><!-- End panel-body -->
            </div><!-- End panel wrapper -->
        </div><!-- End panel box -->
    </div><!-- End root element -->
</template>
<script>
export default {
    props: {
        mimetic: {type: String, default: ''},
        pathdoc: {type: String, default: ''},
        pathsave: {type: String, default: ''},
    },
    data() {
        return {
            campos: ['tdoc','ndoc','n1','n2','a1','a2','fnac','sex','eci','dir','tel','dep','mcp','reg','niv','ocu','eps','tvin','aco','aco_tel','res','res_tel','res_par'],
            campos_con: ['fec', 'tser', 'tcon', 'nota', 'cup', 'fin', 'cau', 'tdiag', 'diag', 'diag_tx', 'med', 'area', 'nreg'],
            f_tdoc: '',
            f_ndoc: '',
            f_n1: '',
            f_n2: '',
            f_a1: '',
            f_a2: '',
            f_fnac: '',
            f_sex: '',
            f_eci: '',
            f_dir: '',
            f_tel: '',
            f_dep: '',
            f_mcp: '',
            f_reg: '',
            f_niv: '',
            f_ocu: '',
            f_eps: '',
            f_tvin: '',
            f_aco: '',
            f_aco_tel: '',
            f_res: '',
            f_res_tel: '',
            f_res_par: '',
            k_fec: '',
            k_tser: '',
            k_tcon: '',
            k_nota: '',
            k_cup: '',
            k_fin: '',
            k_cau: '',
            k_tdiag: '',
            k_diag: '',
            k_diag_tx: '',
            k_med: '',
            k_area: '',
            k_nreg: '',
            targetUser: null,
			datos: [],
            status: 'ini',
            status_con: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'SUCCESS': 'success', 'NOMATCH': 'nomatch', 'FAILED': 'failed'}
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
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
        resetear: function(){
            this.status = this.state.INI;
            this.status_con = this.state.INI;
            this.targetUser = null;
            this.campos.forEach(elm => this['f_' + elm] = '');
            this.campos_con.forEach(elm => this['k_' + elm] = '');
        },
        loadUser: function(){
            if(this.status != this.state.LOADING){
                this.status = this.state.LOADING;
                if(this.verifyFields(['f_tdoc', 'f_ndoc'])){
                    this.targetUser = null;
                    let pam = new FormData();
                    pam.append('tdoc', this.f_tdoc);
                    pam.append('ndoc', this.f_ndoc);
                    axios.post(this.pathdoc, pam).then(res => {
                        if(res.data == null){
                            this.status = this.state.NOMATCH;
                        }else{
                            this.targetUser = res.data;
                            this.campos.forEach(elm => this['f_' + elm] = this.targetUser[elm]);
                            this.status = this.state.LOADED;
                        }
                    }).catch(err => {
                        this.status = this.state.FAILED;
                    });
                }else{
                    this.status = this.state.INI;
                }
            }
        },
        saveConsulta: function(){
            if(this.status_con != this.state.LOADING){
                this.status_con = this.state.LOADING;
                // if(this.verifyFields(['f_tdoc', 'f_ndoc'])){
                    let has_user = (this.targetUser != null)? 'yes': 'no';
                    let pam = new FormData();
                    pam.append('has_user', has_user);
                    if(has_user == 'yes'){
                        pam.append('tdoc', this.f_tdoc);
                        pam.append('ndoc', this.f_ndoc);
                    }else{
                        this.campos.forEach(elm => {
                            pam.append(elm, this['f_' + elm]);
                        });
                    }
                    this.campos_con.forEach(elm => {
                        pam.append(elm, this['k_' + elm]);
                    });
                    axios.post(this.pathsave, pam).then(res => {
                        console.log(res.data);
                        // if(res.data == null){
                        //     this.status_con = this.state.NOMATCH;
                        // }else{
                        //     this.targetUser = res.data;
                        //     this.campos.forEach(elm => this['f_' + elm] = this.targetUser[elm]);
                        // }
                        this.status_con = this.state.SUCCESS;
                    }).catch(err => {
                        this.status_con = this.state.FAILED;
                    });
                // }else{
                //     this.status_con = this.state.INI;
                // }
            }
        }
    },
    mounted() {
        // alert('some');
    }
}
</script>
<style scoped>
    .loading {opacity: .5; pointer-events: none !important; user-select: none !important}
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .table.table-df th {padding-top:.3rem !important; padding-bottom: .3rem !important; color:#000; background: #F4F4F4; font-family:Arial}
    .table.table-df td {padding-top:.5rem !important; padding-bottom: .5rem !important; color:#000}
</style>
