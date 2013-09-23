$(document).ready(function(){
    $("select[name*=ask_status]").change(function(){     
        window.location='../summary_asks?status=' + this.value; 
    }); 
});
