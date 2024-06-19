<template>
    <div style="position:relative">
        <div id="mf-simple-map" class="border" :style="{height: lc_altura}"></div>
        <div :class="loading? 'kemala d-flex align-items-center justify-content-center': 'd-none'">
            <i class="fa fa-spinner fa-spin fs-2"></i>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        altura: {type: String, default: '300'},
        unidad: {type: String, default: 'px'},
        latitud: {type: String, default: '10.978965'},
        longitud: {type: String, default: '-74.799904'},
        autocentrar: {type: Boolean, default: false},
        campo_latitud: {type: String, default: 'lat'},
        campo_longitud: {type: String, default: 'lng'},
        zoom: {type: String, default: '13'},
        localcenter: {type: Boolean, default: false}
    },
    data() {
        return {
            lc_altura: '',
            lc_zoom: 13,
            mapa: null,
            starEvent: false,
            starIcon: null,
            starLocation: null,
            vistas: ['roadmap', 'satellite', 'terrain', 'hybrid'],
            registros: [],
            puntos: [],
            _latitud: 0,
            _longitud: 0,
            _vista: 'roadmap',
            limitLat: {min: 0, max: 0},
            limitLng: {min: 0, max: 0},
            lastStyle: -1,
            style: 1,
            styles: [//Clean | DarkYellow | Night
        		[{featureType: 'poi', stylers: [{visibility: 'off'}]},{featureType: 'transit', elementType: 'labels.icon', stylers: [{visibility: 'off'}]}],
		        [{"featureType": "all","elementType": "labels.text.fill","stylers": [{"saturation": 36},{"color": "#000000"},{"lightness": 40}]},{"featureType": "all","elementType": "labels.text.stroke","stylers": [{"visibility": "on"},{"color": "#000000"},{"lightness": 16}]},{"featureType": "all","elementType": "labels.icon","stylers": [{"visibility": "off"}]},{"featureType": "administrative","elementType": "geometry.fill","stylers": [{"lightness": 20}]},{"featureType": "administrative","elementType": "geometry.stroke","stylers": [{"color": "#000000"},{"lightness": 17},{"weight": 1.2}]},{"featureType": "administrative.province","elementType": "labels.text.fill","stylers": [{"color": "#e3b141"}]},{"featureType": "administrative.locality","elementType": "labels.text.fill","stylers": [{"color": "#e0a64b"}]},{"featureType": "administrative.locality","elementType": "labels.text.stroke","stylers": [{"color": "#0e0d0a"}]},{"featureType": "administrative.neighborhood","elementType": "labels.text.fill","stylers": [{"color": "#d1b995"}]},{"featureType": "landscape","elementType": "geometry","stylers": [{"color": "#000000"},{"lightness": 20}]},{"featureType": "poi","elementType": "geometry","stylers": [{"color": "#000000"},{"lightness": 21}]},{"featureType": "road","elementType": "labels.text.stroke","stylers": [{"color": "#12120f"}]},{"featureType": "road.highway","elementType": "geometry.fill","stylers": [{"lightness": "-77"},{"gamma": "4.48"},{"saturation": "24"},{"weight": "0.65"}]},{"featureType": "road.highway","elementType": "geometry.stroke","stylers": [{"lightness": 29},{"weight": 0.2}]},{"featureType": "road.highway.controlled_access","elementType": "geometry.fill","stylers": [{"color": "#f6b044"}]},{"featureType": "road.arterial","elementType": "geometry","stylers": [{"color": "#4f4e49"},{"weight": "0.36"}]},{"featureType": "road.arterial","elementType": "labels.text.fill","stylers": [{"color": "#c4ac87"}]},{"featureType": "road.arterial","elementType": "labels.text.stroke","stylers": [{"color": "#262307"}]},{"featureType": "road.local","elementType": "geometry","stylers": [{"color": "#a4875a"},{"lightness": 16},{"weight": "0.16"}]},{"featureType": "road.local","elementType": "labels.text.fill","stylers": [{"color": "#deb483"}]},{"featureType": "transit","elementType": "geometry","stylers": [{"color": "#000000"},{"lightness": 19}]},{"featureType": "water","elementType": "geometry","stylers": [{"color": "#0f252e"},{"lightness": 17}]},{"featureType": "water","elementType": "geometry.fill","stylers": [{"color": "#080808"},{"gamma": "3.14"},{"weight": "1.07"}]}],
		        [{"featureType": "all", "elementType": "all", "stylers": [{"visibility": "on"}]},{"featureType": "all", "elementType": "labels", "stylers": [{"visibility": "off"}, {"saturation": "-100"}]},{"featureType": "all", "elementType": "labels.text.fill", "stylers": [{"saturation": 36}, {"color": "#000000"}, {"lightness": 40}, {"visibility": "off"}]},{"featureType": "all", "elementType": "labels.text.stroke", "stylers": [{"visibility": "off"}, {"color": "#000000"}, {"lightness": 16}]},{"featureType": "all", "elementType": "labels.icon", "stylers": [{"visibility": "off"}]},{"featureType": "administrative", "elementType": "geometry.fill", "stylers": [{"color": "#000000"}, {"lightness": 20}]},{"featureType": "administrative", "elementType": "geometry.stroke", "stylers": [{"color": "#000000"}, {"lightness": 17}, {"weight": 1.2}]},{"featureType": "landscape", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 20}]},{"featureType": "landscape", "elementType": "geometry.fill", "stylers": [{"color": "#4d6059"}]},{"featureType": "landscape", "elementType": "geometry.stroke", "stylers": [{"color": "#4d6059"}]},{"featureType": "landscape.natural", "elementType": "geometry.fill", "stylers": [{"color": "#4d6059"}]},{"featureType": "poi", "elementType": "geometry", "stylers": [{"lightness": 21}]},{"featureType": "poi", "elementType": "geometry.fill", "stylers": [{"color": "#4d6059"}]},{"featureType": "poi", "elementType": "geometry.stroke", "stylers": [{"color": "#4d6059"}]},{"featureType": "road", "elementType": "geometry", "stylers": [{"visibility": "on"}, {"color": "#7f8d89"}]},{"featureType": "road", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.highway", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}, {"lightness": 17}]},{"featureType": "road.highway", "elementType": "geometry.stroke", "stylers": [{"color": "#7f8d89"}, {"lightness": 29}, {"weight": 0.2}]},{"featureType": "road.arterial", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 18}]},{"featureType": "road.arterial", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.arterial", "elementType": "geometry.stroke", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.local", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 16}]},{"featureType": "road.local", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.local", "elementType": "geometry.stroke", "stylers": [{"color": "#7f8d89"}]},{"featureType": "transit", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 19}]},{"featureType": "water", "elementType": "all", "stylers": [{"color": "#2b3638"}, {"visibility": "on"}]},{"featureType": "water", "elementType": "geometry", "stylers": [{"color": "#2b3638"}, {"lightness": 17}]},{"featureType": "water", "elementType": "geometry.fill", "stylers": [{"color": "#24282b"}]},{"featureType": "water", "elementType": "geometry.stroke", "stylers": [{"color": "#24282b"}]},{"featureType": "water", "elementType": "labels", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.text", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.text.fill", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.text.stroke", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.icon", "stylers": [{"visibility": "off"}]}]
            ],
            _getCoords: null,
            loading: false
        }
    },
    methods: {
        makeMap: function(){
            /* Montería: {'lat': 8.750282, 'lng': -75.880082} */
            var cfg = {
                zoom: this.lc_zoom,
                center: {'lat': this._latitud, 'lng': this._longitud},
                mapTypeId: this._vista,
                mapTypeControl: false
            };
			this.mapa = new google.maps.Map(document.getElementById("mf-simple-map"), cfg);
            this.mapa.addListener('click', event => {
                // var tm = JSON.stringify(event.latlng, null, 2);
                // console.log(event);
                this.drawStar(event.latLng);
            });
            this.changeStyle(this.style);
        },
		changeStyle: function(arg){
            this.style = (arg >= 1 && arg <= 3)? arg: 1;
            if(this.style != this.lastStyle){
                localStorage.setItem('styleMap', this.style);
                this.mapa.setOptions({styles: this.styles[this.style - 1]});
                this.lastStyle = this.style;
            }
		},
        getStyle: function(){
            return this.style;
        },
        setCenter: function(c1, c2){
            this.mapa.setCenter({lat: c1, lng: c2});
        },
        limpiar: function(){
            this.puntos.forEach(mk => {
                google.maps.event.clearListeners(mk, 'click');
                mk.setMap(null);
            });
            this.puntos = [];
        },
        starClear: function(){
            if(this.starIcon != null){
                this.starIcon.setMap(null);
                this.starIcon = null;
                this.starLocation = null;
            }
        },
        setDatos: function(arg){
            this.limpiar();
            this.registros = arg;
            this.limitLat = (this.registros.length > 0)? {min: this.registros[0][this.campo_latitud], max: this.registros[0][this.campo_latitud]}: {min: 0, max: 0};
            this.limitLng = (this.registros.length > 0)? {min: this.registros[0][this.campo_longitud], max: this.registros[0][this.campo_longitud]}: {min: 0, max: 0};
            this.registros.forEach(elm => {
                var cfg = {'map': this.mapa, 'position': this._getCoords(elm), 'title': this.getText(elm.title)};
                if(!this.isEmpty(elm.label)) cfg.label = {'text': this.getText(elm.label), 'color': "white"};
                if(!this.isEmpty(elm.icon)) cfg.icon = elm.icon;
                var marca = new google.maps.Marker(cfg);
                marca.addListener("click", () => {
                    this.$eventBus.$emit('click-pin', elm);
                });
                this.puntos.push(marca);
            });
            if(this.autocentrar && this.starIcon == null){
                this._latitud = (this.limitLat.max - this.limitLat.min) * 0.5 + this.limitLat.min;
                this._longitud = (this.limitLng.max - this.limitLng.min) * 0.5 + this.limitLng.min;
                if(this.registros.length > 0){
                    this.setCenter(this.registros[0].lat, this.registros[0].lng);
                }
            }
            this.loading = false;
        },
        getText: function(arg, def=''){
            return (arg == undefined || arg == null)? def: arg;
        },
        isEmpty: function(arg){
            return (arg == undefined || arg == null)
        },
        ubicar: function(){
            if(this.localcenter){
                navigator.geolocation.getCurrentPosition(res => {
                    var crd = res.coords;
                    this.lc_zoom = 10;                    
                    this.setCenter(crd.latitude, crd.longitude);
                    this.mapa.setZoom(this.lc_zoom);
                }, err => console.log(err));
            }
        },
        drawStar: function(coords){ // Invoke in click event
            if(this.starEvent){
                if(this.starIcon != null){
                    this.starIcon.setMap(null);
                    this.starIcon = null;
                }
                // this.starIcon = new google.maps.Marker({'position': coords, 'map': this.mapa});
                this.starIcon = new google.maps.Marker({'position': coords, 'map': this.mapa, 'icon': static_path + 'star_icon.png'});
                this.mapa.panTo(coords);
                this.starLocation = {'lat': this.starIcon.getPosition().lat(), 'lng': this.starIcon.getPosition().lng()};
                this.$eventBus.$emit('position-load', this.starLocation);

            }
        }
    },
    mounted() {
        // Require in template: include 'morfeeweb/partials/google-heatmap.html'
        this.lc_altura = this.altura + this.unidad;
        this._latitud = parseFloat(this.latitud);
        this._longitud = parseFloat(this.longitud);
        this.lc_zoom = parseInt(this.zoom);
        if(localStorage.getItem('styleMap') == null){
            localStorage.setItem('styleMap', this.style);
        }else{
            this.style = localStorage.getItem('styleMap');
        }
        this.makeMap();
        if(this.autocentrar){
            this._getCoords = elm => {
                var lat = parseFloat(elm[this.campo_latitud]);
                var lng = parseFloat(elm[this.campo_longitud]);
                this.limitLat.min = Math.min(this.limitLat.min, lat);
                this.limitLat.max = Math.max(this.limitLat.max, lat);
                this.limitLng.min = Math.min(this.limitLng.min, lng);
                this.limitLng.max = Math.max(this.limitLng.max, lng);
                return {'lat': lat, 'lng': lng};
            };
        }else{
            this._getCoords = elm => {
                var lat = parseFloat(elm[this.campo_latitud]);
                var lng = parseFloat(elm[this.campo_longitud]);
                return {'lat': lat, 'lng': lng};
            };
        }
        this.ubicar();
    }
}
</script>
<style scoped>
.kemala {position:absolute; top:0; left:0; right:0; bottom:0; background:#FFFFFF; opacity: .4;}
</style>