var dims = {
    width: 800,
    height: 600,
    color: d3.scaleQuantize().range([
        // "rgb(255,245,240)",
        // "rgb(254,224,210)",
        // "rgb(252,187,161)",
        // "rgb(252,146,114)",
        // "rgb(251,106,74)",
        // "rgb(239,59,44)",
        // "rgb(203,24,29)",
        // "rgb(165,15,21)",
        // "rgb(103,0,13)"
        "#f7fcfd",
        "#e5f5f9",
        "#ccece6",
        "#99d8c9",
        "#66c2a4",
        "#41ae76",
        "#238b45",
        "#006d2c",
        "#00441b"
    ])
};

var projection = d3.geoAlbersUsa()
    .translate([0,0]);
var path=d3.geoPath(projection);
var r_scale=d3.scaleLinear()
    .domain([0,8000000])
    .range([5,20]);

var svg =  d3.select('#chart')
            .append('svg')
            .attr('width', dims.width)
            .attr('height', dims.height);

var map = svg.append('g')
    .attr('id', 'map')
    .attr('cursor', 'pointer');

map.append('rect')
    .attr('x',0)
    .attr('y',0)
    .attr('width', dims.width)
    .attr('height', dims.height)
    .attr('opacity', 0);

d3.json('zombie-attacks.json').then(function(zombie_data,error){
    dims.color.domain([
        d3.min(zombie_data, function(d){
            return d.num;
        }),
        d3.max(zombie_data, function(d){
            return d.num;
        })
    ]);

    d3.json('us.json').then(function(us_data, error){
       us_data.features.forEach(function(us_e, us_i){
           zombie_data.forEach(function(z_e, z_i){
               if(us_e.properties.name !== z_e.state){
                   return null;
               }
               us_data.features[us_i].properties.num=parseFloat(z_e.num);
           })
       })

        console.log(us_data);

       map.selectAll('path')
           .data(us_data.features)
           .enter()
           .append('path')
           .attr('d', path)
           .attr('fill', function(d){
               var num = d.properties.num;
               return num ? dims.color(num) : '#fff';
           })
           .attr('stroke', '#fff')
           .attr('stroke-width', 2);

       draw_cities();
    });
});

function draw_cities(){
    d3.json("us-cities.json").then(function (city_data) {
        map.selectAll("circle")
            .data(city_data)
            .enter()
            .append("circle")
            .style("fill", "#9d1c3c")
            .style("opacity", 0.8)
            .attr("cx",function(d){
                return projection([d.lon,d.lat])[0];
            })
            .attr("cy",function(d){
                return projection([d.lon,d.lat])[1];
            })
            .attr("r",function(d){
                return r_scale(d.population);
            })
            .append("title")
            .text(function(d){
                return d.city;
            });

    });
}