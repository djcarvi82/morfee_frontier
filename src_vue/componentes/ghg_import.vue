<template>
    <div>
        <div class="d-flex justify-content-between mb-4 df-options">
            <a :class="section == elm.code? 'flex-fill bg-target ' + status: 'flex-fill bg-custom ' + status" href="javascript:void(0)" v-for="(elm, i) in opciones" :key="i" @click="setSection(elm.code)">
                <div class="d-flex align-items-center">
                    <span class="lc-icon d-flex align-items-center justify-content-center me-2"><i :class="section == elm.code? 'fa fa-folder-open-o': 'fa fa-folder-o'"></i></span>
                    <span>{{ elm.tx }}</span>
                </div>
            </a>
        </div>
        <div :class="section == 'compra'? '': 'd-none'">
            <import-basic 
                destino="ghg_compras" 
                separador_mode="normal" 
                subtitulo="GHG - COMPRAS" 
                separador="|" 
                sindiccionario
                head="file_parse"
                fields="f_c:Fecha|tpo:Tipo|tm:TiposMov.Nombre|ter:Tercero|pro:Proveedor.Nombre|sp:Soporte|cm:CodMed|cc:CodCum|cb:CodBarra|gn:Generico|lot:Lote|f_v:FechaVen|can:Cantidad|vun:V U|ref:Referencia|obs:Observacion|io:IO|usu:Usuario|f_r:FechaReg|lab:Lab_Prov|bod:Bodega|mov:Movimiento|id:Id|obs2:Obs|con:Cons|tmed:TipoMed"
                rules=""
                codec_mode="show"
                error="ignore"
                error_mode="show"
                info
                extra>
            </import-basic>
            <div class="my-4"></div>
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <import-list coleccion="ghg_compras" titulo="BASE DE DATOS DE COMPRAS"></import-list>
                    </div>
                </div>
            </div>
        </div>
        <div :class="section == 'dispen'? '': 'd-none'">
            <import-basic 
                destino="ghg_dispensacion" 
                separador_mode="normal" 
                subtitulo="GHG - DISPENSACIÓN" 
                separador="|" 
                sindiccionario
                head="file_parse"
                fields="bod:Bodega|pac:Paciente|tip:Tipo identificacion|ide:Identificacion|gen:Genero|eda:EDAD|dir:Direccion|mun:Municipio|dep:Departamento|tel:Telefono|coa:CodAdminis|n_ad:NombreAdministradora|n_pl:NombrePlan|cum:CodCum|des:Descripcion medicamento|con:Concentracion|for:Forma farmaceutica|via:ViaAdministracion|fre:Frecuencia|dur:Dur_Tratamiento|lot:Lote|f_v:FechaVen|ca_p:Cant_Pres|ca_e:Cant_Ent|vlv:ValorVenta|vlc:ValorCosto|dg1:DiagPrincipal|dg2:Diagnostico principal|f_p:Fecha prescripcion|f_a:Fecha autorizacion de entrega|f_e:Fecha Entrega|dia:DiasTrasn|num:Numero de Formula|fac:FACTURA|pen:Pendiente|era:EraPen|cme:ConsMedicamento|ord:OrdenInt|usu:Usuario|aut:Autorizacion|f_fa:FechaFact|exp:Expr1|f_f:FechaFormula|mip:mipres|rad:Radicado|cod:CodCumInt|lis:ListaP"
                rules=""
                codec_mode="show"
                error="ignore"
                error_mode="show"
                info
                extra>
            </import-basic>
            <div class="my-4"></div>
            <div class="panel panel-default card-view border">
                <div class="panel-wrapper collapse in">
                    <div class="panel-body">
                        <import-list coleccion="ghg_dispensacion" titulo="BASE DE DATOS DE DISPENSACIÓN"></import-list>
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
            section: 'compra',
            opciones: [
                {'tx': 'COMPRAS', 'code': 'compra'}, 
                {'tx': 'DISPENSACIÓN', 'code': 'dispen'}, 
                {'tx': 'MEDICAMENTOS', 'code': 'mentos'}, 
            ],
            status: 'ini',
            state: {'INI': 'ini', 'LOADING': 'loading', 'LOADED': 'loaded', 'FAILED': 'failed'}
        }
    },
    methods: {
		isEmpty: function(arg){
			return ['', undefined, null].includes(arg)? true: /^\s*$/.test(arg);
		},
        setSection: function(code){
            this.section = code;
        }
    },
    mounted() {
        // alert('some');
    }
}
</script>
<style scoped>
    .colmin {width: 1%; white-space: nowrap; text-align: center}
    .bg-target {cursor:pointer; background:#F0C541; padding:14px 20px; color:#FFF !important}
    .bg-custom {cursor:pointer; background:#DEDEDE; padding:14px 20px}
    .bg-custom + .bg-custom {border-left:1px solid #FEFEFE}
    .bg-custom:hover {background: #DEDEDEAA}
    .lc-icon {display:inline-block; width:35px !important; height:35px !important; background:#FFF; color:#8F908F; border-radius:50% !important}
    .lc-icon > i {font-size:16px}
</style>
