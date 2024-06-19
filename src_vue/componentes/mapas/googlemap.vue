<template>
    <div>
        <div :id="keyname" :style="{height: lc_altura}"></div>
        <div class="text-center" v-if="!calor && mapa != null && !sincontroles">
            <div class="btn-group mt-10">
                <button type="button" :class="(style == 1)? classOn: classOff" v-on:click="changeStyle(1)">Normal</button>
                <button type="button" :class="(style == 2)? classOn: classOff" v-on:click="changeStyle(2)">Amarillo oscuro</button>
                <button type="button" :class="(style == 3)? classOn: classOff" v-on:click="changeStyle(3)">Nocturno</button>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        apikey: {type: String, default: ''},
        latitud: {type: String, default: '9.305844'},
        longitud: {type: String, default: '-75.393827'},
        autocentrar: {type: Boolean, default: false},
        campo_latitud: {type: String, default: 'lat'},
        campo_longitud: {type: String, default: 'lng'},
        campo_peso: {type: String, default: 'none'},
        calor: {type: Boolean, default: false},
        vista: {type: String, default: 'roadmap'},
        radio: {type: String, default: 'none'},
        altura: {type: String, default: 'none'},
        sincontroles: {type: Boolean, default: false}
    },
    data(){
        return {
            keyname: '_mapa_' + Math.random().toString().replace("0.", ""),
            classOn: 'btn btn-default btn-success btn-xs txt-white',
            classOff: 'btn btn-default btn-outline btn-xs',
            vistas: ['roadmap', 'satellite', 'terrain', 'hybrid'],
            registros: [],
            puntos: [],
            hotdata: [],
            geocoder: null,
            mapa: null,
            heatmap: null,
            lastStyle: -1,
            style: 1,
            styles: [//Clean | DarkYellow | Night
        		[{featureType: 'poi', stylers: [{visibility: 'off'}]},{featureType: 'transit', elementType: 'labels.icon', stylers: [{visibility: 'off'}]}],
		        [{"featureType": "all","elementType": "labels.text.fill","stylers": [{"saturation": 36},{"color": "#000000"},{"lightness": 40}]},{"featureType": "all","elementType": "labels.text.stroke","stylers": [{"visibility": "on"},{"color": "#000000"},{"lightness": 16}]},{"featureType": "all","elementType": "labels.icon","stylers": [{"visibility": "off"}]},{"featureType": "administrative","elementType": "geometry.fill","stylers": [{"lightness": 20}]},{"featureType": "administrative","elementType": "geometry.stroke","stylers": [{"color": "#000000"},{"lightness": 17},{"weight": 1.2}]},{"featureType": "administrative.province","elementType": "labels.text.fill","stylers": [{"color": "#e3b141"}]},{"featureType": "administrative.locality","elementType": "labels.text.fill","stylers": [{"color": "#e0a64b"}]},{"featureType": "administrative.locality","elementType": "labels.text.stroke","stylers": [{"color": "#0e0d0a"}]},{"featureType": "administrative.neighborhood","elementType": "labels.text.fill","stylers": [{"color": "#d1b995"}]},{"featureType": "landscape","elementType": "geometry","stylers": [{"color": "#000000"},{"lightness": 20}]},{"featureType": "poi","elementType": "geometry","stylers": [{"color": "#000000"},{"lightness": 21}]},{"featureType": "road","elementType": "labels.text.stroke","stylers": [{"color": "#12120f"}]},{"featureType": "road.highway","elementType": "geometry.fill","stylers": [{"lightness": "-77"},{"gamma": "4.48"},{"saturation": "24"},{"weight": "0.65"}]},{"featureType": "road.highway","elementType": "geometry.stroke","stylers": [{"lightness": 29},{"weight": 0.2}]},{"featureType": "road.highway.controlled_access","elementType": "geometry.fill","stylers": [{"color": "#f6b044"}]},{"featureType": "road.arterial","elementType": "geometry","stylers": [{"color": "#4f4e49"},{"weight": "0.36"}]},{"featureType": "road.arterial","elementType": "labels.text.fill","stylers": [{"color": "#c4ac87"}]},{"featureType": "road.arterial","elementType": "labels.text.stroke","stylers": [{"color": "#262307"}]},{"featureType": "road.local","elementType": "geometry","stylers": [{"color": "#a4875a"},{"lightness": 16},{"weight": "0.16"}]},{"featureType": "road.local","elementType": "labels.text.fill","stylers": [{"color": "#deb483"}]},{"featureType": "transit","elementType": "geometry","stylers": [{"color": "#000000"},{"lightness": 19}]},{"featureType": "water","elementType": "geometry","stylers": [{"color": "#0f252e"},{"lightness": 17}]},{"featureType": "water","elementType": "geometry.fill","stylers": [{"color": "#080808"},{"gamma": "3.14"},{"weight": "1.07"}]}],
		        [{"featureType": "all", "elementType": "all", "stylers": [{"visibility": "on"}]},{"featureType": "all", "elementType": "labels", "stylers": [{"visibility": "off"}, {"saturation": "-100"}]},{"featureType": "all", "elementType": "labels.text.fill", "stylers": [{"saturation": 36}, {"color": "#000000"}, {"lightness": 40}, {"visibility": "off"}]},{"featureType": "all", "elementType": "labels.text.stroke", "stylers": [{"visibility": "off"}, {"color": "#000000"}, {"lightness": 16}]},{"featureType": "all", "elementType": "labels.icon", "stylers": [{"visibility": "off"}]},{"featureType": "administrative", "elementType": "geometry.fill", "stylers": [{"color": "#000000"}, {"lightness": 20}]},{"featureType": "administrative", "elementType": "geometry.stroke", "stylers": [{"color": "#000000"}, {"lightness": 17}, {"weight": 1.2}]},{"featureType": "landscape", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 20}]},{"featureType": "landscape", "elementType": "geometry.fill", "stylers": [{"color": "#4d6059"}]},{"featureType": "landscape", "elementType": "geometry.stroke", "stylers": [{"color": "#4d6059"}]},{"featureType": "landscape.natural", "elementType": "geometry.fill", "stylers": [{"color": "#4d6059"}]},{"featureType": "poi", "elementType": "geometry", "stylers": [{"lightness": 21}]},{"featureType": "poi", "elementType": "geometry.fill", "stylers": [{"color": "#4d6059"}]},{"featureType": "poi", "elementType": "geometry.stroke", "stylers": [{"color": "#4d6059"}]},{"featureType": "road", "elementType": "geometry", "stylers": [{"visibility": "on"}, {"color": "#7f8d89"}]},{"featureType": "road", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.highway", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}, {"lightness": 17}]},{"featureType": "road.highway", "elementType": "geometry.stroke", "stylers": [{"color": "#7f8d89"}, {"lightness": 29}, {"weight": 0.2}]},{"featureType": "road.arterial", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 18}]},{"featureType": "road.arterial", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.arterial", "elementType": "geometry.stroke", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.local", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 16}]},{"featureType": "road.local", "elementType": "geometry.fill", "stylers": [{"color": "#7f8d89"}]},{"featureType": "road.local", "elementType": "geometry.stroke", "stylers": [{"color": "#7f8d89"}]},{"featureType": "transit", "elementType": "geometry", "stylers": [{"color": "#000000"}, {"lightness": 19}]},{"featureType": "water", "elementType": "all", "stylers": [{"color": "#2b3638"}, {"visibility": "on"}]},{"featureType": "water", "elementType": "geometry", "stylers": [{"color": "#2b3638"}, {"lightness": 17}]},{"featureType": "water", "elementType": "geometry.fill", "stylers": [{"color": "#24282b"}]},{"featureType": "water", "elementType": "geometry.stroke", "stylers": [{"color": "#24282b"}]},{"featureType": "water", "elementType": "labels", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.text", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.text.fill", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.text.stroke", "stylers": [{"visibility": "off"}]},{"featureType": "water", "elementType": "labels.icon", "stylers": [{"visibility": "off"}]}]
            ],
            limitLat: {min: 0, max: 0},
            limitLng: {min: 0, max: 0},
            _latitud: 0,
            _longitud: 0,
            _vista: 'roadmap',
            _getCoords: null,
            lc_altura: '',
        }
    },
    methods: {
        makeMap: function(){
            /* Montería: {'lat': 8.750282, 'lng': -75.880082} */
			this.mapa = new google.maps.Map(document.getElementById(this.keyname), {zoom:14, center:{'lat': this._latitud, 'lng': this._longitud}, mapTypeId: this._vista, mapTypeControl: false});
            this.changeStyle(this.style);
        },
		changeStyle: function(arg){
            if(!this.calor && this.vista != 'google'){
                this.style = (arg >= 1 && arg <= 3)? arg: 1;
                if(this.style != this.lastStyle){
                    localStorage.setItem('styleMap', this.style);
                    this.mapa.setOptions({styles: this.styles[this.style - 1]});
                    this.lastStyle = this.style;
                }
            }
		},
        setCenter: function(c1, c2){
            this.mapa.setCenter({lat: c1, lng: c2});
        },
        localizar: function(direccion){
            if(this.geocoder == null){
                this.geocoder = new google.maps.Geocoder();
            }
            this.limpiar();
            this.geocoder.geocode({'address': direccion, 'componentRestrictions': {country: 'CO'}}, (rs, status) => {
                if(status == 'OK'){
                    this.$eventBus.$emit('mf-localize', rs[0].geometry.location);
                    this.mapa.setCenter(rs[0].geometry.location);
                    this.puntos.push(new google.maps.Marker({map: this.mapa, position: rs[0].geometry.location, title: direccion}));
                }else{
                    this.$eventBus.$emit('mf-not-localize', status);
                }
            });
        },
        localizarLocation: function(direccion, location){
            this.limpiar();
            this.mapa.setCenter(location);
            this.puntos.push(new google.maps.Marker({map: this.mapa, position: location, title: direccion}));
        },
        setVista: function(arg, force = true){
            if(arg == '' || arg == undefined || arg == 'google'){
                this._vista = 'roadmap';
            }else if(this.vistas.indexOf(arg) > -1){
                this._vista = arg;
            }else if(/^\d+$/.test(arg)){
                var num = parseInt(arg);
                this._vista = (num > 0 && num <= this.vistas.length)? this.vistas[num - 1]: this.vistas[0];
            }else{
                this._vista = this.vistas[0];
            }
            if(force){
                this.mapa.setMapTypeId(this._vista[arg]);
            }
        },
        setDatos: function(arg){
            this.limpiar();
            this.registros = arg;
            this.limitLat = (this.registros.length > 0)? {min: this.registros[0][this.campo_latitud], max: this.registros[0][this.campo_latitud]}: {min: 0, max: 0};
            this.limitLng = (this.registros.length > 0)? {min: this.registros[0][this.campo_longitud], max: this.registros[0][this.campo_longitud]}: {min: 0, max: 0};
            if(this.calor){
                this.registros.forEach(elm => {
                    this._getCoords(elm);
                });
                if(this.heatmap == null){
                    this.heatmap = new google.maps.visualization.HeatmapLayer({data: this.hotdata});
                    this.heatmap.setMap(this.mapa);
                    if(this.radio != 'none'){
                        var rad = (this.radio == '')? 20: parseInt(this.radio);
                        this.heatmap.set("radius", rad);
                    }
                }
            }else{
                this.registros.forEach(elm => {
                    this.puntos.push(new google.maps.Marker({map: this.mapa, position: this._getCoords(elm), label: {text: elm.label, color: "white"}, title: elm.title}));
                });
            }
            if(this.autocentrar){
                this._latitud = (this.limitLat.max - this.limitLat.min) * 0.5 + this.limitLat.min;
                this._longitud = (this.limitLng.max - this.limitLng.min) * 0.5 + this.limitLng.min;
                this.setCenter(this._latitud, this._longitud);
            }
        },
        setAltura: function(arg){
            this.lc_altura = (arg == 'none')? '75vh': arg + 'px';
        },
        limpiar: function(){
            this.puntos.forEach(mk => mk.setMap(null));
            this.puntos = [];
        }
    },
    mounted(){
        console.log('Google Map is mounted!');
        this.setAltura(this.altura);
        this.setVista(this.vista, false);
        this._latitud = parseFloat(this.latitud);
        this._longitud = parseFloat(this.longitud);
        if(localStorage.getItem('styleMap') == null){
            localStorage.setItem('styleMap', this.style);
        }else{
            this.style = localStorage.getItem('styleMap');
        }
        if(this.calor){
            if(this.autocentrar){
                if(this.campo_peso == 'none'){
                    this._getCoords = elm => {
                        var lat = parseFloat(elm[this.campo_latitud]);
                        var lng = parseFloat(elm[this.campo_longitud]);
                        this.limitLat.min = Math.min(this.limitLat.min, lat);
                        this.limitLat.max = Math.max(this.limitLat.max, lat);
                        this.limitLng.min = Math.min(this.limitLng.min, lng);
                        this.limitLng.max = Math.max(this.limitLng.max, lng);
                        this.hotdata.push(new google.maps.LatLng(lat, lng));
                    };
                }else{
                    this._getCoords = elm => {
                        var lat = parseFloat(elm[this.campo_latitud]);
                        var lng = parseFloat(elm[this.campo_longitud]);
                        this.limitLat.min = Math.min(this.limitLat.min, lat);
                        this.limitLat.max = Math.max(this.limitLat.max, lat);
                        this.limitLng.min = Math.min(this.limitLng.min, lng);
                        this.limitLng.max = Math.max(this.limitLng.max, lng);
                        this.hotdata.push({'location': new google.maps.LatLng(lat, lng), 'weight': elm[this.campo_peso]});
                    };
                }
            }else{
                if(this.campo_peso == 'none'){
                    this._getCoords = elm => {
                        var lat = parseFloat(elm[this.campo_latitud]);
                        var lng = parseFloat(elm[this.campo_longitud]);
                        this.hotdata.push(new google.maps.LatLng(lat, lng));
                    };
                }else{
                    this._getCoords = elm => {
                        var lat = parseFloat(elm[this.campo_latitud]);
                        var lng = parseFloat(elm[this.campo_longitud]);
                        this.hotdata.push({'location': new google.maps.LatLng(lat, lng), 'weight': elm[this.campo_peso]});
                    };
                }
            }
        }else{
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
        }
        this.makeMap();
        this.$eventBus.$emit('mf-map-ini', 'Mapa inicializado!');
    }
}
</script>
<style scoped>
a[target="_blank"] {display:none !important}
</style>