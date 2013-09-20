$(document).ready(function(){
    $("select[name=offer_status]").change(function(){     
        window.location='../offers?status=' + this.value; 
    }); 
    $('a[href*=process_offer]').colorbox({
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
            if (response.action == 'approve') {
                $('input[name=offer_id]').val(response.offer.id);
                return "#approve_offer_popup";
            }
            if (response.action == 'disapprove') {
                $('input[name=offer_id]').val(response.offer.id);
                return "#disapprove_offer_popup";
            }
        }      
    });
    $('form[name*=approve_offer_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#approve_offer_alert').empty();
                    $('#approve_offer_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../offers'; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name*=disapprove_offer_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#disapprove_offer_alert').empty();
                    $('#disapprove_offer_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../offers'; 
                }
            }     
        });
        return false; 
    }); 
});
