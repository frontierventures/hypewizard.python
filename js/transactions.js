$(document).ready(function(){
    $("select[name=transaction_status]").change(function(){     
        window.location='../transactions?status=' + this.value; 
    }); 
    $.ajax({
        url: '../get_session_user',
        async: false,
        cache: false,
        dataType: 'json',
        fail: function() { response.error = false }, 
        success: function(data) {
            response = data;
            //alert(response.action);
            if(response.action == 'create_transaction') {
                $('#row_0').css("background-color", "#0266C8");
                $('#row_0').css("color", "#FFFFFF");
            }
        }
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
                $('#claim_balance_alert').empty();
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
