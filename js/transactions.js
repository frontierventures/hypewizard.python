$(document).ready(function(){
    $("select[name=transaction_status]").change(function(){     
        window.location='../transactions?status=' + this.value; 
    }); 
    $('a[href*=process_transaction]').colorbox({
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
                $('input[name=transaction_id]').val(response.transaction.id);
                return "#approve_transaction_popup";
            }
            if (response.action == 'disapprove') {
                $('input[name=transaction_id]').val(response.transaction.id);
                return "#disapprove_transaction_popup";
            }
        }      
    });
    $('form[name*=approve_transaction_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#approve_transaction_alert').empty();
                    $('#approve_transaction_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = '../transactions'; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name*=disapprove_transaction_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(json) {
                if (json.response == 0) {
                    $('#disapprove_transaction_alert').empty();
                    $('#disapprove_transaction_alert').append('<div class="alert alert-error" id="alert">' + json.text + '</div>');
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
