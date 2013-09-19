$(document).ready(function(){
    $("#orderStatus").change(function(){     
        window.location='../summaryOrders?status=' + this.value; 
    }); 
});
