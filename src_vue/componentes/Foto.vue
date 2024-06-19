
<template>
    <div class="file">
        <a href="#">
            <div class="image" :style="'background-image:url(' + imagen + ')'"></div>
            <div class="file-name">
                {{ titulo }}Italy street.jpg
                <br>
                <span>{{ descripcion }}</span>
            </div>
        </a>
    </div>
</template>
<script>
export default {
    props: {
        imagen: {type: String, default: ''},
        titulo: {type: String, default: 'Título'},
        descripcion: {type: String, default: 'Descripción'}
    },
    data(){
        return {
            keyname: '_count_' + Math.random().toString().replace("0.", ""),
        }
    },
    mounted(){
        console.log('Caja fotográfica!');
    }
}
</script>