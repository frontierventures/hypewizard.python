$(document).ready(function(){
    $('a[href*=process_bid]').colorbox({
        inline:true,           
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
                return "#create_bid_popup";
            }
            if (response.action == 'engage') {
                $('input[name*=bid_id]').val(response.bid.id);
                return "#engage_promoter_popup";
            }
        }      
    });
    $('form[name*=create_bid_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#create_bid_alert').empty();
                    $('#create_bid_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../'; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name*=engage_promoter_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#create_transaction_alert').empty();
                    $('#create_transaction_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../transactions'; 
                }
            }     
        });
        return false; 
    }); 
});
