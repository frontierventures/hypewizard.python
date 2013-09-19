$(document).ready(function(){
    $("#userStatus").change(function(){     
        window.location='../summaryUsers?status=' + this.value; 
    }); 
});
