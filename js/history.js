$(document).ready(function(){
    $("#transactionStatus").change(function(){     
        window.location='../history?status=' + this.value; 
    }); 
});
