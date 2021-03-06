function drawSimpleCircle(map, name, lat, lng, rad, opacity, color) {
    map.addLayer({
        'id': name,
        'type': 'circle',
        'source': {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [{
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [lng, lat]
                    }
                }]
            }
        },
        'layout': {
            'visibility': 'visible'
        },
        'paint': {
            'circle-radius': rad,
            'circle-opacity': opacity,
            'circle-color': color,
            'circle-stroke-color': 'black',
            'circle-stroke-width': 1,
            'circle-stroke-opacity': 0.8
        }
    });
}

function removeLayer(map, name) {
    map.removeLayer(name)
    map.removeSource(name)
}

function drawSourceCircle(map, name, source, rad, opacity, color) {
    map.addLayer({
        'id': name,
        'type': 'circle',
        'source': source,
        'layout': {
            'visibility': 'visible'
        },
        'paint': {
            'circle-radius': rad,
            'circle-opacity': opacity,
            'circle-color': color,
            'circle-stroke-color': 'black',
            'circle-stroke-width': 1,
            'circle-stroke-opacity': 0.8
        }
    });
}

var museums_data = null

function loadMuseums(map) {
    var openPoints = {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': []
        }
    }

    var closedPoints = {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': []
        }
    }

    $.when(
        $.ajax({
            url: "/api/museums",
            type: "get",
            data: {},
            success: function(response) {
                //console.log(response)
                museums_data = JSON.parse(response)
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        })

    ).then(function(x) {
        var x = 0
        museums_data.museums.forEach(function(item, index) {
            if (item.discard != "true"){
                ratingint = item.rating
                ratingstr = ""

                while (ratingint > 1) {
                    ratingstr = ratingstr + "\u2605"
                    ratingint = ratingint - 1
                }

                if (ratingint > 0.5)
                    ratingstr = ratingstr + "<span class='halftext'>\u2605</span>"

                var tmpmus = {
                    'type': 'Feature',
                    'properties': {
                        'description': "<b>Museum: " + item.name + "</b><br>Website: " + item.website + "<br>Phone Number: " + item.phone_number + "<br><p class='text-center'>" + ratingstr + "</p>"
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [item.longitude, item.latitude]
                    }
                }

                if (item.permanently_closed) {
                    closedPoints.data.features.push(tmpmus)
                } else {
                    openPoints.data.features.push(tmpmus)
                }
            }

        })
        map.addSource('openmus', openPoints)
        map.addSource('closedmus', closedPoints)

        drawSourceCircle(map, 'openmus', 'openmus', 10, 0.75, '#08AC00')
        drawSourceCircle(map, 'closedmus', 'closedmus', 10, 0.75, '#DE0B1D')
    })
}

var docks_data = null

function loadDocks(map) {
    var docksPoints = {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': []
        }
    }

    $.when(
        $.ajax({
            url: "/api/docks",
            type: "get",
            data: {},
            success: function(response) {
                //console.log(response)
                docks_data = JSON.parse(response)
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        })
    ).then(function(x) {
        var x = 0
        docks_data.docks.forEach(function(item, index) {
            docksPoints.data.features.push({
                'type': 'Feature',
                'properties': {
                    'description': "<b>Station: " + item.Station_Name + "</b><br>Bikes: " + item.num_bikes_available + "/" + item.capacity + "<br>Update: " + item.last_updated_date
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [item.station_lon, item.station_lat]
                }
            })
        })
        //console.log('ok')
        map.addSource('bikedocks', docksPoints)

        drawSourceCircle(map, 'bikedocks', 'bikedocks', 8, 0.75, '#1179BA')
    })
}

function bindpop(map, popup, source) {
    map.on('mouseenter', source, function(e) {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';

        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties.description;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    }); 

    map.on('mouseleave', source, function() {
        map.getCanvas().style.cursor = '';
        popup.remove();
    });
}

route = null;
function plot_path(map, coordinates, token) {
    var base_url = "https://api.mapbox.com/directions/v5/mapbox/cycling/"

    coordinates.forEach(function(item, index) {
        base_url = base_url + item[0] + "," + item[1] + ";"
    })

    var final = base_url.slice(0, -1)
    var result = {}
    var tot = coordinates.length - 1

    $.when(
        $.ajax({
            url: final,
            type: "get",
            data: {
                waypoints: "0;" + tot,
                geometries: "geojson",
                access_token: token
            },
            success: function(response) {
                result = response
            },
            error: function(xhr) {
                //Do Something to handle error
            }
        })
    ).then(function() {
        console.log(result)
        if (route != null) {
            removeLayer(map,"route")
        }
        route = result.routes[0].geometry.coordinates
        drawLine(map, "route", route , "black", 5)
    })
}

function plot_text(text) {
    var output = ""
    text.forEach(function(item, index) {
        if (item[0] == "stat") {
            //station
            var element = docks_data["docks"].find(x => x.Station_Name === item[1])
            output = output.concat("Station: " + element.Station_Name + "<br>bikes: " + element.num_bikes_available + "/" + element.capacity + "<br/><br>")

        } else {
            console.log(item[1].toUpperCase())
            var element = museums_data["museums"].find(x => x.label === item[1])
            var day = new Date().getDay()
            var hours = ""

            //sunday testing
            //day = 1

            if (element["opening_hours"] != null) {
                var time = element["opening_hours"].periods.find(x => x.open.day === day)
                if (time != undefined) {
                    hours = "<br/>hours: " + Math.round(time.open.time/100).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false})+":"+Math.round(time.open.time%100).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false}) + " - " + Math.round(time.close.time/100).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false})+":"+Math.round(time.open.time%100).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false})
                }
            }  
            output = output.concat("<strong>Museum: " + element.name + "</strong>" + hours + "<br/>Average visit: " + element.suggested_time + " mins<br/><br>")
            
        }
    })
    return output

}

function drawLine(map, name, coordinates, color, width) {
    map.addLayer({
        'id': name,
        'type': 'line',
        'source': {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'LineString',
                    'coordinates': coordinates
                }
            }
        },
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': color,
            'line-width': width,
            'line-opacity': 0.6
        }
    })
}