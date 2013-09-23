$(document).ready(function(){
    $('a[href*=reset_password]').colorbox({
        inline:true,           
        href: function() {              
            return "#reset_password_popup";
        }      
    });
    $('form[name*=reset_password_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(response) {
                if (response.error) {
                    $('#reset_password_alert').empty();
                    $('#reset_password_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = response.url; 
                }
            }     
        });
        return false; 
    }); 
});
