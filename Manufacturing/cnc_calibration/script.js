
function line_intersect(x1, y1, x2, y2, x3, y3, x4, y4)
{
    var ua, ub, denom = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1);
    if (denom == 0) {
        return null;
    }
    ua = ((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3))/denom;
    ub = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3))/denom;
    return {
        x: x1 + ua * (x2 - x1),
        y: y1 + ua * (y2 - y1),
        seg1: ua >= 0 && ua <= 1,
        seg2: ub >= 0 && ub <= 1
    };
}

function svg_scaling(param){


    return (param/500 + 150)

}



function calc(){

    for(var i=0; i<8; i++){
        document.getElementById("p"+i+"x").innerHTML = "";
        document.getElementById("p"+i+"y").innerHTML = "";
        document.getElementById("p"+i+"z").innerHTML = "";

        document.getElementById("p"+i+"d").innerHTML= "";
    }

    var str = document.getElementById("input_text").value;
    //alert(str);

    var lines = str.split('\n');
    var points = [];
    var intersections = [];
    console.log(lines);

    lines.forEach(function(item, index){
    
        item = item.trim();

        if (item.startsWith("[PRB:") && item.endsWith(":1]")){
            points.push({str: item.trim(), x:0, y:0, z:0});

        }
        
    });

    document.getElementById("poly_points").setAttribute("points", "");

    var angleArray = [];


    while(points.length>8){

        console.log("shift")

        points.shift();

    }

    if (points.length<8){
        alert("Length error");
        return;
    }

    points.forEach(function(item, index){

        var parts = item.str.split(":");
        var coordinates = parts[1].split(",");
        
        item.x = parseFloat(coordinates[0])*1000;
        item.y = (parseFloat(coordinates[1])*1000)*(-1);
        item.z = parseFloat(coordinates[2])*1000;


        if (index%4 > 1){

            document.getElementById("p"+index+"x").innerHTML = item.x;
        }
        else{

            document.getElementById("p"+index+"y").innerHTML = item.y;
        }
        


       // document.getElementById("p"+index+"z").innerHTML = item.z;

       var points_string = document.getElementById("poly_points").getAttribute("points");
       points_string += " " + svg_scaling(item.x) +"," +svg_scaling(item.y)
       document.getElementById("poly_points").setAttribute("points", points_string);

       if (index ==7){

            var points_string = document.getElementById("poly_points").getAttribute("points");
            points_string += " " + svg_scaling(points[0].x) +"," +svg_scaling(points[0].y)
            document.getElementById("poly_points").setAttribute("points", points_string);
            

       }

        if (index%2 == 1){

            //console.log(index);

            var measured_param1 = points[index].y;
            var measured_param2 = points[index-1].y;
            var constant_param1 = points[index].x;
            var constant_param2 = points[index-1].x;


            if (index%4>=2){
                measured_param1 = points[index].x;
                measured_param2 = points[index-1].x;
                var constant_param1 = points[index].y;
                var constant_param2 = points[index-1].y;

                
            }


            if (index == 1){

                document.getElementById("p"+index+"d").innerHTML=  measured_param2 - measured_param1;
                document.getElementById("p"+(index-1)+"d").innerHTML= measured_param1 - measured_param2;

            }
            else if (index == 3){

                document.getElementById("p"+index+"d").innerHTML=  measured_param1 - measured_param2;
                document.getElementById("p"+(index-1)+"d").innerHTML= measured_param2 - measured_param1;
               
            }
            else if (index == 5){

                document.getElementById("p"+index+"d").innerHTML=  ( measured_param1 - measured_param2);
                document.getElementById("p"+(index-1)+"d").innerHTML=   (    measured_param2 - measured_param1);

            }
            else if (index == 7){

                document.getElementById("p"+index+"d").innerHTML=  ( measured_param2 - measured_param1);
                document.getElementById("p"+(index-1)+"d").innerHTML=   (    measured_param1 - measured_param2);

            }



            var dx = 0;
            var dy = 0;
            var angle= 0;

            if (index == 3 || index == 7){

                dx = constant_param2 - constant_param1;
                dy = measured_param2 - measured_param1;
                var angle = Math.atan(dy/dx)*(180/Math.PI)
            }
            else{

                dy = constant_param2 - constant_param1;
                dx = measured_param2 - measured_param1;
                var angle = Math.atan(dy/dx)*(180/Math.PI)

            }
            
           angle = (angle+360 + 45)%90 -45;
           
            console.log(angle);
            angleArray.push(angle);

        }
        
    });



    var res0 = line_intersect(points[0].x, points[0].y, points[1].x, points[1].y,points[2].x, points[2].y, points[3].x, points[3].y)
    var res1 = line_intersect(points[2].x, points[2].y, points[3].x, points[3].y,points[4].x, points[4].y, points[5].x, points[5].y)
    var res2 = line_intersect(points[4].x, points[4].y, points[5].x, points[5].y,points[6].x, points[6].y, points[7].x, points[7].y)
    var res3 = line_intersect(points[6].x, points[6].y, points[7].x, points[7].y,points[0].x, points[0].y, points[1].x, points[1].y)

    var res = [res0, res1, res2, res3];


    document.getElementById("xoffset").innerHTML= "X"+ Math.floor((res[0].x + res[1].x + res[2].x + res[3].x)/4)/1000;
    document.getElementById("yoffset").innerHTML= "Y"+ Math.floor((res[0].y + res[1].y + res[2].y + res[3].y)/4)/1000;
    document.getElementById("rotation").innerHTML= "Rotation: "+Math.floor(1000*(angleArray[0] + angleArray[1] + angleArray[2] + angleArray[3])/4)/1000 + "°";


    var points_string = "";
    points_string += " " + svg_scaling(res0.x) +"," +svg_scaling(res0.y);
    points_string += " " + svg_scaling(res1.x) +"," +svg_scaling(res1.y);
    points_string += " " + svg_scaling(res2.x) +"," +svg_scaling(res2.y);
    points_string += " " + svg_scaling(res3.x) +"," +svg_scaling(res3.y);
    points_string += " " + svg_scaling(res0.x) +"," +svg_scaling(res0.y);
    document.getElementById("poly_intersections").setAttribute("points", points_string);


    for (var i=0; i<4; i++){

        document.getElementById("i"+i+"x").innerHTML=Math.floor(res[i].x);
        document.getElementById("i"+i+"y").innerHTML=Math.floor(res[i].y);

    }

    console.log(res0);
    console.log(res1);
    console.log(res2);
    console.log(res3);

    

}