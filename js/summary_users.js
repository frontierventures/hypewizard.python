$(document).ready(function(){
    $("select[name*=user_status]").change(function(){     
        window.location='../summary_users?status=' + this.value; 
    }); 
});
