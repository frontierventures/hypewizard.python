$(document).ready(function(){
    $('a[href*=reset_password]').colorbox({
        inline:true,           
        href: function() {              
            return "#reset_password_popup";
        }      
    });
    //$('form[name*=claim_funds_form]').submit(function() { 
    //    var response = {};
    //    $.ajax({
    //        data: $(this).serialize(),
    //        type: $(this).attr('method'),
    //        url: $(this).attr('action'),
    //        dataType: 'json',
    //        success: function(json) {
    //            if (json.response == 0) {
    //                $('#claim_funds_alert').empty();
    //                $('#claim_funds_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
    //                $.colorbox.resize();
    //            } else {
    //                $.colorbox.close();
    //                window.location = '../transactions'; 
    //            }
    //        }     
    //    });
    //    return false; 
    //}); 
});
