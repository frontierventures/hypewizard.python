$(document).ready(function(){
    $("#transactionStatus").change(function(){     
        window.location='../summaryTransactions?status=' + this.value; 
    }); 
});
