<template>
    <div>
        <div :class="display == 'list'? '': 'd-none'">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <h6 class="panel-title fs-5">ACTAS DE CONCILIACIÓN REGISTRADAS</h6>
                        <button class="btn btn-success btn-xs" @click="setDisplay('add')"><i class="fa fa-plus me-2"></i>Registrar acta</button>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="table-wrap">
                            <div class="table-responsive">
                                <table class="table mb-0">
                                    <thead>
                                        <tr>
                                            <th class="colmin text-center">No.</th>
                                            <th>Código</th>
                                            <th>Depto</th>
                                            <th>Mcpio</th>
                                            <th>NIT</th>
                                            <th>Prestador</th>
                                            <th>Auditor</th>
                                            <th>Registro</th>
                                            <th class="colmin px-3">Total a pagar</th>
                                            <th class="colmin px-4">Estado</th>
                                            <th class="colmin text-center">Acción</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(elm, i) in actas" :key="i">
                                            <td class="colmin text-center">{{ i + 1 }}</td>
                                            <td>{{ elm.cod }}</td>
                                            <td>{{ elm.dep }}</td>
                                            <td>{{ elm.mun }}</td>
                                            <td>{{ elm.nit }}</td>
                                            <td>{{ elm.pre }}</td>
                                            <td>{{ elm.aud }}</td>
                                            <td>{{ elm.create }}</td>
                                            <td class="text-right">{{ formatMiles(elm.total) }}</td>
                                            <td class="text-center">
                                                <span class="badge badge-success" v-if="elm.create != ''"><i class="fa fa-check me-1"></i> Final</span>
                                                <span class="badge badge-warning" v-else><i class="fa fa-eraser me-1"></i> Borrador</span>
                                            </td>
                                            <td class="text-center">
                                                <a class="l-hover" href="javascript:void(0)" @click="showActa(elm._id.$oid)"><i class="fa fa-qrcode"></i></a>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div><!-- End table-wrap -->
                    </div>
                </div>
            </div>
        </div>
        <div :class="getEditClass()">
            <div class="panel panel-default card-view border">
                <div class="panel-heading">
                    <div class="d-flex justify-content-between">
                        <h6 class="panel-title fs-5">{{ display == 'add'? 'REGISTRO DE QR PARA CERTIFICAR AUDITORÍA': 'EDICIÓN DE ACTA DE AUDITORÍA' }}</h6>
                        <button class="btn btn-success btn-xs" @click="setDisplay('list')">Atrás</button>
                    </div>

                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="border-bottom mb-5"></div>
                        <div class="row">
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Código del acta:</label>
                                    <input type="text" class="form-control" v-model="f_cod" :disabled="display == 'edit'">
                                </div>
                            </div>
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Departamento:</label>
                                    <input type="text" class="form-control" v-model="f_dep">
                                </div>
                            </div>
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Municipio:</label>
                                    <input type="text" class="form-control" v-model="f_mun">
                                </div>
                            </div>
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Auditor:</label>
                                    <input type="text" class="form-control" v-model="f_aud">
                                </div>
                            </div>
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Representante IPS:</label>
                                    <input type="text" class="form-control" v-model="f_fir">
                                </div>
                            </div>
                            <div class="col-sm-2">
                                <div class="form-group">
                                    <label class="control-label">Cargo IPS:</label>
                                    <input type="text" class="form-control" v-model="f_car">
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm-5">
                                <div class="row">
                                    <div class="col-sm-4">
                                        <div class="form-group">
                                            <label class="control-label">NIT:</label>
                                            <input type="text" class="form-control" v-model="f_nit" readonly>
                                        </div>
                                    </div>
                                    <div class="col-sm-8">
                                        <div class="form-group">
                                            <label class="control-label">Prestador:</label>
                                            <input type="text" class="form-control" v-model="f_pre" readonly>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-7">
                                <div class="row">
                                    <div class="col-sm-5">
                                        <div class="form-group">
                                            <label class="control-label">Hash o identificación única del acta:</label>
                                            <input type="text" class="form-control" v-model="codex" readonly>
                                        </div>
                                    </div>
                                    <div class="col-sm-4">
                                        <div class="form-group">
                                            <label class="control-label">Total a pagar:</label>
                                            <input type="text" class="form-control" :value="formatMiles(f_total)" readonly>
                                        </div>
                                    </div>
                                    <div class="col-sm-3">
                                        <div class="form-group">
                                            <label class="control-label">Tipo de facturas:</label>
                                            <select class="form-control">
                                                <option value=""></option>
                                                <option value="Cápita">Cápita</option>
                                                <option value="Evento">Evento</option>
                                                <option value="PGP">PGP</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="table-wrap mt-4">
                            <div class="table-responsive">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th class="py-2 px-2">No. RADICADO</th>
                                            <th class="py-2 px-2">FECHA RADICADO</th>
                                            <th class="py-2 px-2">No. FACTURA</th>
                                            <th class="py-2 px-2">VALOR FACTURA</th>
                                            <th class="py-2 px-2">VALOR GLOSA INICIAL</th>
                                            <th class="py-2 px-2">CÓDIGO DE GLOSA</th>
                                            <th class="py-2 px-2">MOTIVO DE GLOSA</th>
                                            <th class="py-2 px-2">VALOR LEVANTADO</th>
                                            <th class="py-2 px-2">VALOR ACEPTADO IPS</th>
                                            <th class="py-2 px-2">VALOR PENDIENTE POR CONCILIAR</th>
                                            <th class="py-2 px-2">VALOR A PAGAR</th>
                                            <th class="py-2 px-2 colmin">Acción</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- ['k_rad', 'f_rad	'k_fac', 'k_val', 'g_val', 'g_cod', 'g_mot', 'g_eps', 'g_ips', 'g_pen', 'k_pay'], -->
                                        <tr v-for="(elm, i) in boxdata" :key="i">
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1" :value="elm.k_rad" readonly></td>
                                            <td class="py-2 px-2"><input type="date" class="form-control m-0 px-1" :value="elm.f_rad" readonly></td>
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1" :value="elm.k_fac" readonly></td>
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1 text-right" :value="formatMiles(elm.k_val)" readonly></td>
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1 text-right" :value="formatMiles(elm.g_val)" readonly></td>
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1" :value="elm.g_cod" @change="setField('g_cod', i, $event)"></td>
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1" :value="elm.g_mot" @change="setField('g_mot', i, $event)"></td>
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1 text-right" :value="formatMiles(elm.g_eps)" readonly></td>
                                            <td class="py-2 px-2"><input type="number" class="form-control m-0 px-1" :value="elm.g_ips" @change="setField('g_ips', i, $event)"></td>
                                            <td class="py-2 px-2"><input type="text" class="form-control m-0 px-1 text-right" :value="formatMiles(elm.g_pen)" readonly></td>
                                            <td class="py-2 px-2"><input type="text" :class="isEmpty(elm.k_pay)? 'form-control m-0 px-1 no-data': 'form-control m-0 px-1 text-right'" :value="formatMiles(elm.k_pay)" readonly></td>
                                            <td class="py-2 px-2 text-center">
                                                <a href="javascript:void(0)" class="btn btn-danger py-2 px-3" @click="remFactura(i, true)" v-if="elm.dfh == 'edit'"><i class="fa fa-trash"></i></a>
                                                <a href="javascript:void(0)" class="btn btn-danger py-2 px-3" @click="remFactura(i, false)" v-else><i class="fa fa-trash"></i></a>
                                            </td>
                                        </tr>
                                    </tbody>
                                    <tfoot>
                                        <tr>
                                            <th colspan="12">
                                                <div class="d-flex justify-content-center">
                                                    <button class="btn btn-primary" type="button" @click="openModal"><i class="fa fa-plus me-2"></i>Agregar factura</button>
                                                </div>
                                            </th>
                                        </tr>
                                    </tfoot>
                                </table>
                            </div><!-- End table responsive -->
                        </div><!-- End table wrap -->
                        <div class="form-group">
                            <label class="control-label">Observaciones:</label>
                            <textarea class="form-control" rows="5" v-model="f_obs" @keypress="isValidKey($event)"></textarea>
                        </div>
                        <div class="border-bottom my-4"></div>
                        <div class="d-flex justify-content-end mt-4">
                            <div v-if="display == 'edit' && targetActa != null">
                                <button class="btn btn-warning" type="button" @click="saveEditActa(false)" :disabled="is_valid_data == false || status_add == state.LOADING" v-if="targetActa.create == ''">
                                    <i class="fa fa-check me-2"></i>Guardar cambios en borrador
                                </button>
                                <button class="btn btn-success" type="button" @click="saveEditActa(true)" :disabled="is_valid_data == false || status_add == state.LOADING">
                                    <i class="fa fa-check me-2"></i>Guardar acta final
                                </button>
                            </div>
                            <div v-else>
                                <button class="btn btn-success" type="button" @click="saveActa(false)" :disabled="is_valid_data == false || status_add == state.LOADING">
                                    <i class="fa fa-check me-2"></i>Guardar borrador
                                </button>
                                <button class="btn btn-success" type="button" @click="saveActa(true)" :disabled="is_valid_data == false || status_add == state.LOADING">
                                    <i class="fa fa-check me-2"></i>Guardar acta final
                                </button>
                            </div>
                        </div>
                    </div><!-- End panel-body -->
                </div>
            </div>
        </div>
        <div :class="display == 'show'? '': 'd-none'">
            <div class="panel panel-default card-view border no-borpad-print" v-if="status_show == state.LOADED">
                <div class="panel-heading hidden-print">
                    <div class="d-flex justify-content-end">
                        <button class="btn btn-success btn-xs" @click="setDisplay('list')"><i class="fa fa-arrow-left me-2"></i>Atrás</button>
                    </div>
                </div>
                <div class="panel-wrapper collapse in">
                    <div class="panel-body" v-if="targetActa != null">
                        <h5 class="panel-title fs-4 text-center" style="font-weight:bold">ACTA DE CONCILIACIÓN</h5>
                        <div class="mb-5 text-center fs-5" style="color:#000">{{ targetActa.cod }}</div>
                        <h6 class="panel-title fs-5 mb-4">CÓDIGO DE SEGURIDAD: <strong style="color:#000 !important">{{ targetActa.hash }}</strong></h6>
                        <table class="table table-bordered df-print">
                            <thead>
                                <tr>
                                    <th>Código del acta:</th>
                                    <th>NIT:</th>
                                    <th>Prestador:</th>
                                    <th>Departamento:</th>
                                    <th>Municipio:</th>
                                    <th>Auditor:</th>
                                    <th>Fecha de registro:</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>{{ targetActa.cod }}</td>
                                    <td>{{ targetActa.nit }}</td>
                                    <td>{{ targetActa.pre }}</td>
                                    <td>{{ targetActa.dep }}</td>
                                    <td>{{ targetActa.mun }}</td>
                                    <td>{{ targetActa.aud }}</td>
                                    <td>{{ targetActa.create }}</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="table-wrap mt-4">
                            <div class="table-responsive">
                                <table class="table table-bordered border-inner df-print">
                                    <thead>
                                        <tr>
                                            <th class="py-2 px-2">No. RAD.</th>
                                            <th class="py-2 px-2">FECHA RADICADO</th>
                                            <th class="py-2 px-2">No. FACTURA</th>
                                            <th class="py-2 px-2">VALOR FACTURA</th>
                                            <th class="py-2 px-2">VALOR GLOSA INICIAL</th>
                                            <th class="py-2 px-2">CÓDIGO DE GLOSA</th>
                                            <th class="py-2 px-2">MOTIVO DE GLOSA</th>
                                            <th class="py-2 px-2">VALOR LEVANTADO</th>
                                            <th class="py-2 px-2">VALOR ACEPTADO IPS</th>
                                            <th class="py-2 px-2">VALOR PENDIENTE POR CONCILIAR</th>
                                            <th class="py-2 px-2 text-center">VALOR A PAGAR</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <!-- ['k_rad', 'f_rad	'k_fac', 'k_val', 'g_val', 'g_cod', 'g_mot', 'g_eps', 'g_ips', 'g_pen', 'k_pay'], -->
                                        <tr v-for="(elm, i) in targetData" :key="i">
                                            <td class="py-2 px-2">{{ elm.k_rad }}</td>
                                            <td class="py-2 px-2">{{ elm.f_rad }}</td>
                                            <td class="py-2 px-2">{{ elm.k_fac }}</td>
                                            <td class="py-2 px-2 text-right">{{ formatMiles(elm.k_val) }}</td>
                                            <td class="py-2 px-2 text-right">{{ formatMiles(elm.g_val) }}</td>
                                            <td class="py-2 px-2">{{ elm.g_cod }}</td>
                                            <td class="py-2 px-2">{{ elm.g_mot }}</td>
                                            <td class="py-2 px-2 text-right">{{ formatMiles(elm.g_eps) }}</td>
                                            <td class="py-2 px-2 text-right">{{ formatMiles(elm.g_ips) }}</td>
                                            <td class="py-2 px-2 text-right">{{ formatMiles(elm.g_pen) }}</td>
                                            <td class="py-2 px-2 text-right">{{ formatMiles(elm.k_pay) }}</td>
                                        </tr>
                                        <tr v-if="targetActa != null">
                                            <td colspan="3" class="py-2 px-2" style="border:none !important"></td>
                                            <td class="py-2 px-2 text-right d-bold">{{ formatMiles(sumColumn('k_val')) }}</td>
                                            <td class="py-2 px-2 text-right d-bold">{{ formatMiles(sumColumn('g_val')) }}</td>
                                            <td colspan="2" class="py-2 px-2" style="border:none !important"></td>
                                            <td class="py-2 px-2 text-right d-bold">{{ formatMiles(sumColumn('g_eps')) }}</td>
                                            <td class="py-2 px-2 text-right d-bold">{{ formatMiles(sumColumn('g_ips')) }}</td>
                                            <td class="py-2 px-2" style="border:none !important"></td>
                                            <td class="py-2 px-2 text-right d-bold">{{ formatMiles(targetActa.total) }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div><!-- End table-wrap -->
                        <table class="table table-bordered border-inner df-print">
                            <thead>
                                <tr><th class="text-center">OBSERVACIONES</th></tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>{{ targetActa.obs }} &nbsp;</td>
                                </tr>
                            </tbody>
                        </table>
                        <div class="d-flex justify-content-between align-items-center my-5">
                            <div>
                                <div class="d-flex align-items-center">
                                    <div class="d-flex justify-content-center">
                                        <div class="py-2 px-2" style="position:relative; border:1px solid #000; min-width:150px; min-height:150px" v-if="targetActa != null && targetActa.create != ''">
                                            <div class="corner-1"></div>
                                            <div class="corner-2"></div>
                                            <div class="corner-3"></div>
                                            <div class="corner-4"></div>
                                            <img :src="getURL(targetActa._id.$oid)" alt="QR code" class="img-fluid img-fx" style="max-height:150px; vertical-align:middle" v-if="targetActa.create != ''">
                                        </div>
                                        <div v-else>
                                            <img :src="pathtemp" alt="QR borrador" class="img-fluid">
                                        </div>
                                    </div>
                                    <div class="ms-4">
                                        <img :src="pathlogo" alt="" width="142" height="103">
                                    </div>
                                </div>
                            </div>
                            <div class="ps-2 pe-5 mx-5" style="border-top:1px solid #000; color:#000; letter-spacing:1px">
                                <span style="white-space:nowrap">FIRMA INNOVACIÓN ANALÍTICA</span><br>
                                NOMBRE: <strong>{{ targetActa.aud }}</strong><br>
                                CARGO: Auditor
                            </div>
                            <div class="ps-2" style="border-top:1px solid #000; min-width:25em; color:#000; letter-spacing:1px">
                                FIRMA IPS<br>
                                NOMBRE: <strong>{{ targetActa.fir }}</strong><br>
                                CARGO: {{ targetActa.car }}
                            </div>
                        </div>
                        <button type="button" class="btn btn-primary px-3 hidden-print" @click="setDisplay('edit')"><i class="fa fa-pencil me-1"></i> Editar acta</button>
                    </div>
                </div>
            </div>
            <div class="panel panel-default card-view border no-borpad-print" v-else-if="status_show == state.LOADING">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <div class="d-flex align-items-center">
                            <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                            <span>Cargando acta...</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- End display add -->
        <!-- =========== -->
        <!-- Begin modal -->
        <!-- =========== -->
        <div id="lc_modal_fac" class="modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" style="display: none;">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
                        <h5 class="modal-title" id="myLargeModalLabel">BÚSQUEDA DE FACTURAS</h5>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-sm-12">
                                <div class="form-group">
                                    <label class="control-label">No. de radicación</label>
                                    <div class="input-group">
                                        <input type="number" class="form-control" v-model="m_radicado" @keypress.enter="loadFactura" id="fakao">
                                        <span class="input-group-btn">
                                            <button class="btn btn-success" type="button" @click="loadFactura"><i class="fa fa-search me-2"></i> Buscar</button>
                                        </span>
                                    </div>
                                </div>
                                <div class="d-flex justify-content-between align-items-center">
                                    <span :class="m_cash? 'label label-success px-3 py-2': 'label label-custom px-3 py-2'" @click="m_cash = !m_cash"><i class="fa fa-circle"></i> Sólo radicados con glosa</span>
                                    <div :class="select_all? 'dk-click text-success': 'dk-click'" @click="selectAll">
                                        <i :class="select_all? 'fa fa-check-square': 'fa fa-square-o'"></i> <span>Seleccionar todo</span>
                                    </div>
                                </div>
                            </div>
                            <div class="col-sm-6 d-none">
                                <div class="form-group">
                                    <label class="control-label">Número de la factura:</label>
                                    <div class="input-group">
                                        <input type="text" class="form-control" v-model="m_factura" @keypress.enter="loadFactura">
                                        <span class="input-group-btn">
                                            <button class="btn btn-success" type="button" @click="loadFactura"><i class="fa fa-search me-2"></i> Buscar</button>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="border-bottom mt-2 mb-4"></div>
                        <div v-if="status_s == state.LOADING" class="d-flex align-items-center">
                            <i class="fa fa-spinner fa-spin fs-4 me-2"></i>
                            <span>Cargando factura...</span>
                        </div>
                        <div class="table-wrap" v-if="status_s == state.LOADED && m_data.length > 0">
                            <div class="table-responsive">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th class="px-2 py-2">No. contrato</th>
                                            <th class="px-2 py-2">Factura</th>
                                            <th class="px-2 py-2">Consecutivo</th>
                                            <th class="px-2 py-2 colmin">Rad</th>
                                            <th class="px-2 py-2">NIT</th>
                                            <th class="px-2 py-2">Razón Social</th>
                                            <th class="px-2 py-2 text-center">Valor factura</th>
                                            <th class="px-2 py-2 text-center">Total glosas</th>
                                            <th class="px-2 py-2 colmin">Acción</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(elm, i) in m_data" :key="i" :class="getClassCandidate(elm)">
                                            <td class="px-2 py-2">{{ elm.numero_contrato }}</td>
                                            <td class="px-2 py-2">{{ elm.factura }}</td>
                                            <td class="px-2 py-2">{{ elm.consecutivo_radica }}</td>
                                            <td class="px-2 py-2 text-center">{{ elm.numero_radicacion }}</td>
                                            <td class="px-2 py-2">{{ elm.nit }}</td>
                                            <td class="px-2 py-2">{{ elm.razon_social }}</td>
                                            <td class="px-2 py-2 text-right">{{ formatMiles(elm.valor_factura) }}</td>
                                            <td class="px-2 py-2 text-right">{{ formatMiles(elm.total_glosas) }}</td>
                                            <td class="px-2 py-2 text-center">
                                                <span class="df-span" v-if="elm.hash_qr || codigos.includes(elm.factura)"><i class="fa fa-times text-danger fs-5"></i></span>
                                                <span class="df-span" v-else @click="elm.candidate = !elm.candidate"><i :class="elm.candidate? 'fa fa-check-square text-success fs-5 df-normal': 'fa fa-square-o fs-5 df-normal'"></i></span>
                                                <!-- <a href="javascript:void(0)" class="btn btn-primary btn-sm py-1 px-2" @click="addFactura(elm)"><i class="fa fa-check"></i></a> -->
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div v-else-if="status_s == state.LOADED && m_data.length == 0" class="alert alert-warning">
                            <div class="d-flex align-items-center">
                                <i class="fa fa-warning me-2"></i>
                                <span v-if="m_cash">No se encontró ninguna factura <mark>con glosa</mark> con el número de radicado <strong>{{ m_radicado }}</strong>.</span>
                                <span v-else>No se encontró ninguna factura con el número de radicado <strong>{{ m_radicado }}</strong>.</span>
                            </div>
                        </div>
                    </div><!-- End modal-body -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger text-left" data-dismiss="modal">Cerrar ventana</button>
                        <button type="button" class="btn btn-success" @click="selectFacturas" :disabled="m_data.length == 0">Seleccionar facturas</button>
                    </div>
                </div><!-- /.modal-content -->
            </div><!-- /.modal-dialog -->
        </div>
        <!-- End modal -->
    </div>
</template>
<script>
export default {
    props: {
        path: {type: String, default: ''},
        pathbase: {type: String, default: ''},
        pathsearch: {type: String, default: ''},
        pathlist: {type: String, default: ''},
        pathsave: {type: String, default: ''},
        pathlogo: {type: String, default: ''},
        pathtemp: {type: String, default: ''}
    },
    data() {
        return {
            // fecha   hora    tipo	qr|data
            // facs	str|str|str
            // rads	num|num|num
            display: 'list',    // list | add
            select_all: false,
            actas: [],
            boxdata: [],
            codex: '',
            targetActa: null,
            targetData: [],
            targetHash: {},
            targetRem: [],
            f_main: {'codex': 'hash', 'f_cod': 'cod', 'f_dep': 'dep', 'f_mun': 'mun', 'f_pre': 'pre', 'f_nit': 'nit', 'f_aud': 'aud', 'f_fir': 'fir', 'f_car': 'car', 'f_obs': 'obs', 'f_total': 'total'},
            f_all: ['k_rad', 'f_rad', 'k_fac', 'k_val', 'g_val', 'g_cod', 'g_mot', 'g_eps', 'g_ips', 'g_pen', 'k_pay'],
            f_cod: '',
            f_dep: '',
            f_mun: '',
            f_pre: '',
            f_nit: '',
            f_aud: '',
            f_fir: '',
            f_car: '',
            f_obs: '',
            f_total: 0,
            m_factura: '',
            m_radicado: '',
            m_cash: true,
            m_data: [],
            m_fact: [],
            status: 'ini',
            status_add: 'ini',
            status_show: 'ini',
            status_s: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'},
        }
    },
    computed: {
        codigos: function(){
            return  this.boxdata.map(elm => elm.k_fac);
        },
        is_valid_data: function(){
            let cmp = ['f_cod', 'f_dep', 'f_mun', 'f_aud', 'f_fir', 'f_car'].reduce((acum, elm) => acum? !this.isEmpty(this[elm]): acum, true)
            if(cmp == false){
                return false;
            }
            if(this.boxdata.length == 0){
                return false;
            }else{
                return this.boxdata.reduce((acum, elm) => acum? !this.isEmpty(elm.k_pay): acum, true);
            }
        }
    },
    methods: {
        setDisplay: function(arg){
            if(['list', 'add', 'edit', 'show'].includes(arg)){
                if(arg == 'edit'){
                    this.boxdata = [];
                    this.targetHash = {};
                    this.targetRem = [];
                    if(this.targetActa != null){
                        Object.keys(this.f_main).forEach(elm => this[elm] = this.targetActa[this.f_main[elm]]);
                        this.targetData.forEach(elm => {
                            this.boxdata.push(this.makeNodo(elm, 'edit'));
                            this.targetHash[elm.k_fac] = elm;
                        });
                    }
                }else if(arg == 'add'){
                    ['f_cod', 'f_dep', 'f_mun', 'f_pre', 'f_nit', 'f_aud', 'f_total', 'f_fir', 'f_car', 'f_obs'].forEach(elm => this[elm] = '');
                    this.boxdata = [];
                    this.loadCodex();
                }else if(arg == 'show'){
                    this.targetActa = null;
                    this.targetData = [];
                }
                this.display = arg;
            }
        },
        getURL: function(code){
            return this.pathbase + '/' + code;
        },
        openModal: function(){
            this.select_all = false;
            this.m_factura = '';
            this.m_radicado = '';
            this.m_data = [];
            this.status_s = 'ini';
            $('#lc_modal_fac').modal('show');
        },
        formatMiles: function(num){
            return num.toString().replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
        },
        clearData: function(arg){
            return arg.replace(/\s{2,}/g, ' ').replace(/(^\s+|\s+$)/g, '');
        },
        isEmpty: function(arg){
            return ['', undefined, null].includes(arg);
        },
        isValidKey: function(e){
            let char = String.fromCharCode(e.keyCode);
            if(/^['"&\\]+$/.test(char) || e.keyCode == 13){
                e.preventDefault();
            }else{
                return true;
            }
        },
        sumColumn: function(key){
            if(this.targetData.length > 0){
                return this.targetData.reduce((ac, elm) => ac + elm[key], 0);
            }else{
                return 0;
            }
        },
        loadCodex: function(){
            axios.post(this.path).then(res => {
                this.codex = res.data;
            }).catch(err => {console.log(err)});
        },
        loadFactura: function(){
            this.select_all = false;
            this.m_data = [];
            this.status_s = this.state.LOADING;
            let pam = new FormData();
            pam.append('factura', this.m_factura);
            pam.append('radicado', this.m_radicado);
            pam.append('cash', this.m_cash? 'has-value': 'none');
            axios.post(this.pathsearch, pam).then(res => {
                let mnu = (res.data.length > 0)? res.data[0].facturas: [];
                this.m_data = mnu.map(elm => {
                    elm.candidate = false;
                    elm.hash_qr = elm.itachi.length > 0;
                    return elm;
                });
                this.status_s = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status_s = this.state.FAILED;
            });
        },
        loadActas: function(){
            axios.post(this.pathlist).then(res => {
                this.actas = res.data;
            }).catch(err => {console.log(err)});
        },
        showActa: function(hash){
            let pam = new FormData();
            pam.append('codigo', hash);
            this.status_show = this.state.LOADING;
            this.setDisplay('show');
            axios.post(this.pathbase, pam).then(res => {
                this.targetActa = res.data.find(elm => elm.tipo == 'qr');
                this.targetData = res.data.filter(elm => elm.tipo == 'data');
                this.status_show = this.state.LOADED;
            }).catch(err => {
                console.log(err);
                this.status_show = this.state.FAILED;
            })
        },
        makeNodo: function(fac, dfh='add'){
            // f_all:       ['k_rad', 'f_rad', 'k_fac', 'k_val', 'g_val', 'g_cod', 'g_mot', 'g_eps', 'g_ips', 'g_pen', 'k_pay']
            let nodo = {'tipo': 'data', 'hash': this.codex};
            let assoc = {'k_rad': 'numero_radicacion', 'k_fac': 'factura', 'k_val': 'valor_neto', 'f_rad': 'fecha_radicado', 'g_val': 'total_glosas'};
            if(dfh == 'add'){
                this.f_all.forEach(elm => nodo[elm] = '');
                Object.keys(assoc).forEach(elm => nodo[elm] = fac[assoc[elm]]);
            }else{
                this.f_all.forEach(elm => nodo[elm] = fac[elm]);
                nodo['dfh'] = 'edit';
            }
            return nodo;
        },
        addFactura: function(fac){
            if(this.boxdata.length == 0){
                this.f_nit = fac.nit;
                this.f_pre = fac.razon_social;
                this.boxdata.push(this.makeNodo(fac));
            }else{
                if(this.f_nit == fac.nit){
                    this.boxdata.push(this.makeNodo(fac));
                }else{
                    alert('La factura ' + fac.factura + ', no pertenece al prestador de las demás facturas seleccionadas.')
                }
            }
        },
        selectFacturas: function(){
            this.m_fact = [];
            this.m_data.forEach(elm => {
                if(elm.candidate){
                    this.addFactura(elm);
                    this.m_fact.push(elm.factura);
                }
            });
            this.crossGlosa();
            $('#lc_modal_fac').modal('hide');
        },
        isNumber: function(num){
            return /^(\d+|\d+\.\d+)$/.test(num.toString());
        },
        getAltNumber: function(num){
            return this.isNumber(num)? parseFloat(num): 0;
        },
        remFactura: function(index, rem=false){
            if(this.boxdata.length > index){
                let ref = this.boxdata.splice(index, 1)[0];
                if(rem) this.targetRem.push(ref);
                this.f_total = this.boxdata.reduce((acum, elm) => acum + this.getAltNumber(elm.k_pay), 0);
            }
        },
        setField: function(key, index, evt){
            if('g_ips' == key){
                this.boxdata[index][key] = this.isNumber(evt.target.value)? parseFloat(evt.target.value): '';
                // g_pen	VALOR PENDIENTE POR CONCILIAR
                // k_pay	VALOR A PAGAR
                let n1 = this.boxdata[index]['k_val'];  // VALOR FACTURA
                let n2 = this.boxdata[index]['g_ips'];  // VALOR ACEPTADO IPS
                let n3 = this.boxdata[index]['g_val'];  // VALOR GLOSA INICIAL
                this.boxdata[index]['g_eps'] = (this.isEmpty(n3) || this.isEmpty(n2))?  '': this.getAltNumber(n3) - this.getAltNumber(n2);
                let n4 = this.boxdata[index]['g_eps'];  // VALOR LEVANTADO
                this.boxdata[index]['k_pay'] = (this.isEmpty(n1) || this.isEmpty(n2))? '': this.getAltNumber(n1) - this.getAltNumber(n2);
                this.boxdata[index]['g_pen'] = (this.isEmpty(n2) || this.isEmpty(n3) || this.isEmpty(n4))? '': this.getAltNumber(n3) - (this.getAltNumber(n2) + this.getAltNumber(n4));
                if(key == 'g_ips') this.f_total = this.boxdata.reduce((acum, elm) => acum + this.getAltNumber(elm.k_pay), 0);
            }else{
                this.boxdata[index][key] = evt.target.value;
            }
        },
        isExists: function(arg){
            return this.codigos.includes(arg);
        },
        isValidFac: function(fac, nit){
            if(this.boxdata.length == 0){
                return true;
            }else{
                if(this.f_nit == nit){
                    return this.isExists(fac)? false: true;
                }else{
                    return false;
                }
            }
        },
        getClassCandidate: function(elm){
            if(elm.hash_qr){
                return 'stt-qr';
            }
            if(this.codigos.includes(elm.factura)){
                return 'stt-check';
            }
            if(elm.candidate){
                return 'stt-select';
            }
        },
        selectAll: function(){
            this.select_all = !this.select_all;
            if(this.select_all){
                this.m_data.forEach(elm => {
                    if(!elm.hash_qr && !this.codigos.includes(elm.factura)){
                        elm.candidate = true;
                    }
                });
            }else{
                this.m_data.forEach(elm => {
                    elm.candidate = false;
                });
            }
        },
        getTime: function(){
            let time = new Date();
            let mm = String(time.getMonth() + 1).padStart(2, '0');
            let dd = String(time.getDate()).padStart(2, '0');
            let ymd = time.getFullYear() + '-' + mm + '-' + dd;
            let hh = String(time.getHours()).padStart(2, '0');
            let mi = String(time.getMinutes()).padStart(2, '0');
            let se = String(time.getSeconds()).padStart(2, '0');
            let hms = hh + ':' + mi + ':' + se;
            return [ymd, hms];
        },
        saveActa: function(bool){
            // history total|f1:f2:f3|r1:r2:r3|fecha|aud
            if(this.boxdata.length > 0 && this.f_total > 0){
                let dauty = this.getTime().join(' ');
                let facs = this.boxdata.map(elm => elm.k_fac);
                let rads = this.boxdata.map(elm => elm.k_rad);
                let his = this.f_total + '|' + facs.length + 'F|' + rads.length + 'R|' + dauty + '|' + this.f_aud;
                let main = {'_id': this.codex, 'tipo': 'qr', 'hash': this.codex, 'cod': this.f_cod, 'dep': this.f_dep, 'mun': this.f_mun, 'pre': this.f_pre, 'nit': String(this.f_nit), 'aud': this.f_aud, 'total': this.f_total, 'facs': '', 'rads': '', 'fir': this.f_fir, 'car': this.f_car, 'obs': this.clearData(this.f_obs), 'history': '', 'create': '', 'update': dauty};
                if(bool){
                    main['facs'] = facs.join('|');
                    main['rads'] = rads.join('|');
                    main['history'] = his;
                    main['create'] = dauty;
                }
                let datos = [main, ...this.boxdata];
                let pam = new FormData();
                pam.append('datosqr', JSON.stringify(datos));
                this.status_add = this.state.LOADING;
                axios.post(this.pathsave, pam).then(res => {
                    this.setDisplay('list');
                    this.loadActas();
                    this.status_add = this.state.LOADED;
                }).catch(err => {
                    console.log(err);
                    this.status_add = this.state.FAILED;
                });
            }else{
                alert('No hay facturas asociadas, o el total a pagar es 0.');
            }
        },
        saveEditActa: function(bool){
            let param = this.engineData(bool);
            this.status_add = this.state.LOADING;
            if(param != null){
                axios.post(this.pathsave + '/edit', param).then(res => {
                    this.status_add = this.state.LOADED;
                    this.showActa(this.targetActa.hash);
                }).catch(err => {
                    console.log(err);
                    this.status_add = this.state.FAILED;
                });
            }else{
                console.log('No hay cambios!');
                this.status_add = this.state.LOADED;
            }
        },
        engineData: function(bool){
            let pass = false;
            let dauty = this.getTime().join(' ');
            let pam = new FormData();
            let proto = {};
            let adds = [];
            ['f_cod', 'f_dep', 'f_mun', 'f_aud', 'f_fir', 'f_car', 'f_total', 'f_obs'].forEach(elm => {
                let campo = this.f_main[elm];
                if(this[elm] != this.targetActa[campo]){
                    proto[campo] = this[elm];
                }
            });
            if(bool){
                let facs = this.boxdata.map(elm => elm.k_fac);
                let rads = this.boxdata.map(elm => elm.k_rad);
                let his = this.f_total + '|' + facs.length + 'F|' + rads.length + 'R|' + dauty + '|' + this.f_aud;
                if(this.targetActa.create == ''){
                    proto['facs'] = facs.join('|');
                    proto['rads'] = rads.join('|');
                    proto['history'] = his;
                    proto['create'] = dauty;
                }else{
                    if(Object.keys(proto).length > 0){
                        proto['facs'] = facs.join('|');
                        proto['rads'] = rads.join('|');
                        proto['history'] = this.targetActa.history + '@' + this.buildHistory(facs.length + 'F', rads.length + 'R', dauty);
                    }
                }
            }
            if(Object.keys(proto).length > 0){
                proto['update'] = dauty;
                pam.append('mainqr', JSON.stringify(proto));
                pass = true;
            }
            this.targetRem.forEach(elm => {
                pam.append('elim_' + elm.k_fac, elm.k_fac);
                pass = true;
            });
            this.boxdata.forEach(elm => {
                if(elm.dfh == 'edit'){
                    let row = {};
                    ['g_cod', 'g_mot', 'g_eps', 'g_ips', 'g_pen', 'k_pay'].forEach(cmp => {
                        if(elm[cmp] != this.targetHash[elm.k_fac][cmp]) row[cmp] = elm[cmp];
                    });
                    if(Object.keys(row).length > 0){
                        pam.append('edit_' + elm.k_fac, JSON.stringify(row));
                        pass = true;
                    }
                }else{
                    adds.push(elm);
                }
            });
            if(adds.length > 0){
                pam.append('datosqr', JSON.stringify(adds));
                pass = true;
            }
            if(pass){
                pam.append('hash', this.targetActa.hash);
            }
            return pass? pam: null;
        },
        buildHistory: function(fa, ra, fecha){
            let rs = [];
            rs.push(this.f_total);
            rs.push(fa);
            rs.push(ra);
            rs.push(fecha);
            rs.push(this.f_aud);
            if(this.targetActa != null){
                let tmp = this.targetActa.history.split('@');
                let l_fa = '';
                let l_ra = '';
                tmp.forEach(elm => {
                    let xam = elm.split('|');
                    if(xam[1] != 'equal') l_fa = xam[1];
                    if(xam[2] != 'equal') l_ra = xam[2];
                });
                if(rs[1] == l_fa) rs[1] = 'equal';
                if(rs[2] == l_ra) rs[2] = 'equal';
            }
            return rs.join('|');
        },
        getEditClass: function(){
            if(this.display == 'add' || this.display == 'edit'){
                return this.status_add == this.state.LOADING? 'block-data': '';
            }else{
                return 'd-none';
            }
        },
        crossGlosa: function(){
            let pam = new FormData();
            pam.append('facturas', this.m_fact.join('|'));
            axios.post(this.pathbase + '/glosa/cross', pam).then(res => {
                res.data.forEach(elm => {
                    for(let i = 0; i < this.boxdata.length; i++){
                        if(this.boxdata[i].k_fac == elm._id){
                            let tm = /^\d+/.exec(elm.glosa);
                            this.boxdata[i].g_cod = (tm !== null)? tm[0]: '';
                            this.boxdata[i].g_mot = elm.concepto;
                            break;
                        }
                    }
                });
            }).catch(err => {console.log(err)});
        }
    },
    mounted() {
        this.loadActas();
    }
}
</script>
<style scoped>
.colmin {width: 1%; white-space:nowrap; text-align: center}
.table th {background: #F5F5F5}
.form-group > .control-label, .no-transform {text-transform: none}
.bg-custom-grey {background: #F5F5F5}
.bg-custom-grey > i.fa {color:#DDD}
.bg-custom-grey:hover > i.fa {color:#333}
.bg-custom-hover:hover {background: #E5E5E5}
.l-hover:hover {color:#4E9DE6}
table.df-border th, table.df-border td {border: 1px solid #AAA !important}
.d-bold {font-weight: bold; color:#222}
table.table-bordered.border-inner {border:none !important}
table.table-bordered.border-inner th {border:1px solid #DEDEDE !important}
.label {text-transform: none; cursor:default; user-select: none}
.label-custom {background:#E7E7E7; color:#999}
.table tr.stt-qr td {background:#FBEFEF; color:#BB0000}
.table tr.stt-select td {background:#2ECD9922}
.table tr.stt-check td {background:#F8FFFF; color:#3B88A9}
.table.table-bordered.df-print th, .table.table-bordered.df-print td {border:1px solid #000 !important; color:#000; font-family: Arial}
img-fx {transition: width 1s, height 1s}
.corner-1 {position:absolute; top:0; left:0; border-top:6px solid #000; border-left:6px solid #000; width:50px; height:50px}
.corner-2 {position:absolute; top:0; right:0; border-top:6px solid #000; border-right:6px solid #000; width:50px; height:50px}
.corner-3 {position:absolute; bottom:0; left:0; border-bottom:6px solid #000; border-left:6px solid #000; width:50px; height:50px}
.corner-4 {position:absolute; bottom:0; right:0; border-bottom:6px solid #000; border-right:6px solid #000; width:50px; height:50px}
@media print {
    .no-borpad-print {border:none !important; padding: 0 !important; margin: 0 !important;}
    .corner-1, .corner-2, .corner-3, .corner-4 {display: none}
}
.form-control.no-data {background: #FCC !important; border:1px solid #A50021}
input.form-control[readonly] {user-select: none !important; cursor: default !important}
.block-data {user-select: none; pointer-events: none !important; opacity: 0.3;}
label.label-all {user-select: none}
input:checked + label.label-all {color:#2ECD99}
.dk-click {user-select: none; cursor: pointer}
</style>