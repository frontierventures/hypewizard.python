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
});
