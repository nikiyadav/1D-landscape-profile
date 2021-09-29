//d3.js code
//var svgWidth = "90%", svgHeight = "90%";

var red = "#ff5555"
var blue = "#5555ff"
var green = "#55ff55"
var pink = "#FF69B4"

var svgWidth = 900, svgHeight = 600;
var svg = d3.select("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

var minPersistence, maxPersistence;
var maxWidth;
var group;
var xScale, yScale, x_axis, y_axis;
//load tree from JSON file
tree = [];
d3.json("./data/cat3.json", function(data) {
    //console.log(data);
	tree = data;
    minPersistence = tree[0].i;
    maxPersistence = minPersistence;
    maxWidth = tree[0].w*1.1; //10% increased
    for(var i = 0; i < tree.length; i++) {
        if(tree[i].i > maxPersistence)
            maxPersistence = tree[i].i;
    }
    maxPersistence = maxPersistence*1.05; //5% increased
    console.log("minPersistence = " + minPersistence);
    console.log("maxPersistence = " + maxPersistence);
    setAxes();
	PaintPart(0, 0, maxWidth, minPersistence- minPersistence*0.05);
});

function setAxes() {
    xScale = d3.scaleLinear()
        .domain([0,	maxWidth])
        .range([0, svgWidth]);

    yScale = d3.scaleLinear()
        .domain([minPersistence- minPersistence*0.05, maxPersistence + maxPersistence*0.05])
        .range([svgHeight, 0]);

    x_axis = d3.axisBottom().scale(xScale);

    y_axis = d3.axisLeft().scale(yScale);


    var xAxisBase = 25;
    var xAxisTranslate = svgHeight - xAxisBase;
    group = svg.append("g")
        .attr("transform", "translate(30, -" + xAxisBase + ")");
    group.call(y_axis);

    svg.append("g")
        .attr("transform", "translate(30, " + xAxisTranslate  +")")
        .call(x_axis);
}

function PaintPart(node, _x, width, base) {
    var baseIsoVal = base;
    var x = _x;

    //draw for each node in pedge
    if(tree[node].c.length == 0) {
        //draw in center    - DRAW HILL
        pedge = tree[node].p.slice().reverse()
        //console.log(pedge);
        for(var i = 0; i < pedge.length; i++) {
            //for each augmented node
            //console.log(pedge[i].i + ", " + baseIsoVal);
            group.append("rect")
                .attr("x", xScale(x + width/2 - pedge[i].w/2))
                .attr("y", yScale(pedge[i].i))
                .attr("width", xScale(pedge[i].w))
                .attr("height", yScale(baseIsoVal) - yScale(pedge[i].i))
                .attr("fill", blue);
            baseIsoVal = pedge[i].i;
        }
        //now draw node itself
        group.append("rect")
            .attr("x", xScale(x + width/2 - tree[node].w/2))
            .attr("y", yScale(tree[node].i))
            .attr("width", xScale(tree[node].w))
            .attr("height", yScale(baseIsoVal) - yScale(tree[node].i))
            .attr("fill", blue);
        baseIsoVal = tree[node].i;
        //console.log(node + " = node,isovalue = " + tree[node].i);
    } else {
        //draw in left side - DRAW PART
        pedge = tree[node].p.slice().reverse()
        //console.log(pedge);
        for(var i = 0; i < pedge.length; i++) {
            //for each augmented node
            //console.log(pedge[i].i + ", " + baseIsoVal);
            group.append("rect")
                .attr("x", xScale(x))
                .attr("y", yScale(pedge[i].i))
                .attr("width", xScale(pedge[i].w))
                .attr("height", yScale(baseIsoVal) - yScale(pedge[i].i))
                .attr("fill", red);
            baseIsoVal = pedge[i].i;
        }
        //now draw node itself
        group.append("rect")
            .attr("x", xScale(x))
            .attr("y", yScale(tree[node].i))
            .attr("width", xScale(tree[node].w))
            .attr("height", yScale(baseIsoVal) - yScale(tree[node].i))
            .attr("fill", red);
        baseIsoVal = tree[node].i;

        //call for each child
        for(var i = 0; i < tree[node].c.length; i++) {
            //know the width required for this child
            var child = tree[node].c[i];
            var w = tree[child].w;
            if(tree[child].p.length != 0) {
                w = tree[child].p[tree[child].p.length - 1].w;
            }
            PaintPart(child, x, w, baseIsoVal);
            x = x + w;
        }
    }
}
