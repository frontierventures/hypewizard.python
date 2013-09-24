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
            if (response.action == 'claim') {
                $('input[name=transaction_id]').val(response.transaction.id);
                return "#claim_balance_popup";
            }
        }      
    });
    $('form[name*=claim_balance_form]').submit(function() { 
        var response = {};
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(response) {
                if (response.error) {
                    $('#claim_balance_alert').empty();
                    $('#claim_balance_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
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
