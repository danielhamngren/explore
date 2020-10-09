console.log("app.js successfully loaded lol");

var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function () {
    if(xhr.readyState === XMLHttpRequest.DONE) {
        var status = xhr.status;
        if (status === 0 || (status >= 200 && status < 400)) {
            // The request has been completed successfully
            console.log(xhr.responseText);
            mapboxgl.accessToken = xhr.responseText;
        } else {
            console.log("mapbox token request failed")
        }
    }
};
xhr.open('GET', "/api/mapbox_token", false);
xhr.send();

var map = new mapboxgl.Map({
    container: 'map',
    // style: 'mapbox://styles/namatoj/ckfz2pspg0atf19nq973bxo3z', // stylesheet location
    style: 'mapbox://styles/namatoj/cii4mprxb0061b8lz7pt8athu', // stylesheet location
    center: [13.004192, 55.604887], // starting position [lng, lat]
    zoom: 11 // starting zoom
});

let places_data = null;

map.on('load', function () {
// Add an image to use as a custom marker
    d3.json(
        'http://192.168.64.2:8000/api/places',
        function (err, data) {
            if (err) throw err;

            places_data = data;
            map.addSource('places', {
                type: 'geojson',
                data: places_data
            });
            map.addLayer({
                'id': 'places',
                'type': 'circle',
                'source': 'places',
                'layout': {
                    // make layer visible by default
                    'visibility': 'visible'
                },
                'paint': {
                    'circle-radius': {
                        'base': 1.75,
                        'stops': [
                            [12, 3],
                            [22, 180]
                        ]
                    },
                    'circle-color': [
                        'match',
                        ['get', 'amenity'],
                        'restaurant',
                        '#2222cc',
                        'fast_food',
                        '#cc2222',
                        'cafe',
                        '#22cc22',
                        /* other */ '#050'
                    ],
                    'circle-opacity':
                        [
                            'match',
                            ['get', 'visited'],
                            1,
                            1.0,
                            0,
                            0.1,
                            /* other */ 0.1
                        ],
                    'circle-stroke-color': '#333',
                    'circle-stroke-width': 1,
                    'circle-stroke-opacity': 0.5,
                }
            });
        }
    );
    map.on('click', 'places', function (e) {
        var coordinates = e.features[0].geometry.coordinates.slice();
        var name = e.features[0].properties.name;
        var identity = e.features[0].properties.pk;
        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }
        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(name + `<br /><button type="button" onclick="toggleMarker('${identity.toString()}')">Mark</button>`)
            .addTo(map);
    });
});

function toggleMarker(identity) {
    for (let i = 0; i < places_data.features.length; i++) {
        if (places_data.features[i].properties.pk === identity) {
            if (places_data.features[i].properties.visited === 1) {
                places_data.features[i].properties.visited = 0;
            } else {
                places_data.features[i].properties.visited = 1;

                var xhr = new XMLHttpRequest();
                xhr.onreadystatechange = function () {
                };
                xhr.open('GET', `/api/register_visit?place=${identity}`);
                xhr.send()
            }
            break;
        }
    }
    map.getSource('places').setData(places_data);
}