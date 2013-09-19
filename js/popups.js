$(document).ready(function(){
    $('a[href*=feature_disabled]').colorbox({
        inline:true,           
        href: function() {              
        //var APIurl = $(this).attr('href'); 
        //$.ajax({
        //    url: APIurl, 
        //    async: false,
        //    cache: false,
        //    dataType: 'json',
        //    success: function(data) {
        //        response = data;
        //    }
        //});
        return "#feature_disabled_popup";
    }      
    });
});
