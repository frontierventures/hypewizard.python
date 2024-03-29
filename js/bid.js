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
            if (response.action == 'withdraw') {
                $('input[name=bid_id]').val(response.bid.id);
                return "#withdraw_bid_popup";
            }
            if (response.action == 'engage') {
                $('input[name=transaction_type]').val('engage_promoter');
                $('input[name*=bid_id]').val(response.bid.id);
                return "#engage_promoter_popup";
            }
        }      
    });
    $('form[name=create_bid_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(response) {
                if (response.error) {
                    $('#create_bid_alert').empty();
                    $('#create_bid_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = response.url; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name=engage_promoter_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(response) {
                if (response.error) {
                    $('#engage_promoter_alert').empty();
                    $('#engage_promoter_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../offers'; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name=withdraw_bid_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#withdraw_bid_alert').empty();
                    $('#withdraw_bid_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../?kind=promoter'; 
                }
            }     
        });
        return false; 
    }); 
});
