$(document).ready(function(){
    $(".collapsedHeading.collapsed").next().hide();$(".collapsedHeading").click(function(){$(this).next().slideToggle("fast");$(this).toggleClass("collapsed")})
    
    //cool little titan services hover
        jq('#titanServicesLink').hover(
	    function(){//over
		jq("#titanServicesLinks").fadeIn(300);
	    },
	    function(){//out
		jq("#titanServicesLinks").fadeOut(200);
	    }
        ); 
    //end titan services stuff
    
    
});