$(document).ready(function(){
    $('a[href*=process_ask]').colorbox({
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
                if (response.available_balance == 0) {
                    return "#deposit_popup";
                } else {
                    return "#create_ask_popup";
                }
            }
            if (response.action == 'withdraw') {
                $('input[name=ask_id]').val(response.ask.id);
                return "#withdraw_ask_popup";
            }
            if (response.action == 'engage') {
                $('input[name=transaction_type]').val('engage_client');
                $('input[name=ask_id]').val(response.ask.id);
                return "#engage_client_popup";
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
                    window.location = '../'; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name*=deposit_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(response) {
                if (response.error) {
                    $('#deposit_alert').empty();
                    $('#deposit_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = response.url; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name*=engage_client]').submit(function() { 
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
                    window.location = '../?kind=client'; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name*=withdraw_ask]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#withdraw_ask_alert').empty();
                    $('#withdraw_ask_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../'; 
                }
            }     
        });
        return false; 
    }); 
});
