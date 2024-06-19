<template>
    <div>
        <ul role="tablist" class="nav nav-tabs" id="myTabs_15">
            <li v-for="(elm, i) in tipos" :key="i" :class="elm.ky == ripTarget? 'active': ''" role="presentation">
                <a href="javascript:void(0)" v-on:click="ripTarget = elm.ky">{{ elm.tx }}</a>
            </li>
            <!-- <li class="active" role="presentation">
                <a href="javascript:void(0)" data-toggle="tab" role="tab">Usuarios</a>
            </li>
            <li role="presentation">
                <a href="javascript:void(0)" data-toggle="tab" role="tab">Consultas</a>
            </li> -->
        </ul>
        <div class="panel panel-default card-view border">
            <div class="panel-wrapper collapse in">
                <div class="panel-body">
                    <div v-if="ripTarget == 'us'">
                        <local-importer 
                            ref="i_us"
                            destino="audit_rip_us_0"
                            separador="|"
                            info
                            sindiccionario
                            head="file_parse" 
                            fields="c_rad:numero_radicado|c_file:nombre_archivo|c_rw:numero_fila|c_ld:consecutivo_cargue|tid:tipo_identificacion|ide:numero_identificacion|eps:codigo_entidad|tus:tipo_usuario|ap1:primer_apellido|ap2:segundo_apellido|nm1:primer_nombre|nm2:segundo_nombre|eda:edad|uni:unidad_medida_edad|sx:sexo|dp:codigo_departamento|mc:codigo_municipio|zn:zona" 
                            rules="ide:string|dp:string|mc:string"
                            skipintro
                            titulo="ARCHIVO DE USUARIOS" 
                            subtitulo="DATOS GENÉRICOS">
                        </local-importer>
                    </div>
                    <div v-if="ripTarget == 'ac'">
                        <local-importer 
                            ref="i_ac"
                            destino="audit_rip_ac_0"
                            separador="|"
                            info
                            sindiccionario
                            head="file_parse" 
                            fields="c_rad:numero_radicado|c_file:nombre_archivo|c_rw:numero_fila|c_ld:consecutivo_cargue|nfa:numero_factura|hab:codigo_prestador|tid:tipo_identificacion|ide:numero_identificacion|fec:fecha_consulta|aut:numero_autorizacion|cup:codigo_consulta|fin:finalidad_consulta|cau:causa_externa|cie0:codigo_diagnostico_principal|cie1:codigo_diagnostico_relacionado_1|cie2:codigo_diagnostico_relacionado_2|cie3:codigo_diagnostico_relacionado_3|diag:tipo_diagnostico_principal|val:valor_consulta|cuo:valor_cuota_moderadora|net:valor_neto_pagar" 
                            rules="ide:string|nfa:string|aut:string|cup:string|cie0:string|cie1:string|cie2:string|cie3:string|fin:string|cau:string"
                            skipintro
                            titulo="ARCHIVO DE CONSULTAS" 
                            subtitulo="DATOS GENÉRICOS">
                        </local-importer>
                    </div>
                    <div v-if="ripTarget == 'ap'">
                        <import-basic 
                            ref="i_ap"
                            destino="audit_rip_ap_0"
                            separador="|"
                            info
                            sindiccionario
                            head="file_fixed" 
                            fields="name|doc" 
                            skipintro
                            titulo="ARCHIVO DE PROCEDIMIENTOS" 
                            subtitulo="DATOS GENÉRICOS">
                        </import-basic>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Imoka from './import-basic.vue';
export default {
    components: {'local-importer': Imoka},
    data() {
        return {
            tipos: [
                {'tx': 'Usuarios', 'ky': 'us'},
                {'tx': 'Consultas', 'ky': 'ac'},
                {'tx': 'Procedimientos', 'ky': 'ap'},
            ],
            ripTarget: 'us',
        }
    },
    methods: {

    },
    mounted() {

    }
}
</script>
<style scoped>
ul.nav.nav-tabs > li.active > a {background:#F0C541 !important; color:#FFF !important}
</style>