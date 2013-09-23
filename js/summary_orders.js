$(document).ready(function(){
    $("select[name*=order_status]").change(function(){     
        window.location='../summary_orders?status=' + this.value; 
    }); 
});
