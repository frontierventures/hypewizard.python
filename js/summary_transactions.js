$(document).ready(function(){
    $("select[name*=transaction_status]").change(function(){     
        window.location='../summary_transactions?status=' + this.value; 
    }); 
});
