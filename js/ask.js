$(document).ready(function(){
    $('a[href*=process_ask]').colorbox({
        inline:true,           
        onClosed: function() { window.location = '../offers?kind=' + offer_kind; },
        href: function() {              
            var APIurl = $(this).attr('href'); 
            $.ajax({
                url: APIurl, 
                async: false,
                cache: false,
                dataType: 'json',
                success: function(data) {
                    response = data;
                }
            });
            if (response.action == 'create') {
                $('input[name=status_id]').val(response.ask.status_id);
                return "#create_ask_popup";
            }
        }      
    });
    $('form[name*=create_ask_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#create_ask_alert').empty();
                    $('#create_ask_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../ask'; 
                }
            }     
        });
        return false; 
    }); 
});
