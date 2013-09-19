$(document).ready(function(){
    $("#assetStatus").change(function(){     
        window.location='../assets?status=' + this.value; 
    }); 
});
