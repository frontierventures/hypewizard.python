$(document).ready(function(){
    $("select[name*=bid_status]").change(function(){     
        window.location='../summary_bids?status=' + this.value; 
    }); 
});
