$(document).ready(function(){
    $("select[name=transaction_status]").change(function(){     
        window.location='../transactions?status=' + this.value; 
    }); 
    build_ask_grid();
    add_transactions();

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
    $('form[name=approve_transaction_form]').submit(function() { 
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(response) {
                if (response.error) {
                    $('#approve_transaction_alert').empty();
                    $('#approve_transaction_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
                    $.colorbox.resize();
                } else {
                    $.colorbox.close();
                    window.location = response.url; 
                }
            }     
        });
        return false; 
    }); 
    $('form[name=disapprove_transaction_form]').submit(function() { 
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            dataType: 'json',
            success: function(response) {
                if (response.error) {
                    $('#disapprove_transaction_alert').empty();
                    $('#disapprove_transaction_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
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
function build_ask_grid() {
    var response = {};
    $.ajax({
        url: '../get_asks',
        async: false,
        cache: false,
        dataType: 'json',
        fail: function() { response.error = false }, 
        success: function(data) {
            response = data;
        }
    });
    for (var i = 0; i < response.orders.length; i++)
        add_ask_to_grid(response.orders[i]);
};
function add_transactions() {
    var response = {};
    $.ajax({
        url: '../get_transactions',
        async: false,
        cache: false,
        dataType: 'json',
        fail: function() { response.error = false }, 
        success: function(data) {
            response = data;
        }
    });
    for (var i = 0; i < response.transactions.length; i++)
        add_transaction_to_grid(response.transactions[i]);
};
function add_ask_to_grid(ask) { 
    var action_url = '../process_ask?action=engage&id=' + ask.id; 
    var action_cell = '<div style="text-align:center"><a href="../">View Tweet</a> <a href="' + action_url + '">Engage Client</a></div>';

    alert("added ask");

    $('.asks').append('<div id="status_' + ask.twitter_status_id + '" class="span4">' +
            '<div class="block">' +
            '<div style="text-align:center; float:left; width:150px;">' +
            '<div style="text-align:center">' + ask.niche + '</div>' +
            '<div>' +
            '<a href="https://twitter.com/' + ask.twitter_name + '">' + ask.twitter_name + '</a>' +
            '<div>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '<div style="float: left;width: 150px;">' +
            '<div style="text-align:center;font-size: 30px;"><b>' + ask.cost + 'BTC</b></div>' +
            '<div style="text-align:center">' + ask.target + ' of ' + ask.goal + '</div>' +
            '</div>' +
            '<div style="text-align:center; display: table-cell; vertical-align: middle; font-size: 12px; height: 120px;">' +
            //'<a href="https://twitter.com/' + ask.twitter_name + '/status/' + ask.twitter_status_id + '">' + ask.twitter_status_text + '</a>' +    
            ask.twitter_status_text +    
            '</div>' +
            '<div style="text-align:center">' + ask.campaign_type + '</div>' +
            //action_cell + 
            '</div>' +
            '</div>');
};
function add_transaction_to_grid(transaction) { 
    alert(transaction.ask_id);
    var action_url = '../process_ask?action=engage&id=' + transaction.id; 
    var action_cell = '<div style="text-align:center"><a href="../process_transaction?action=approve&id=' + transaction.id + '">Approve</a> <a href="../process_transaction?action=disapprove&id=' + transaction.id + '">Approve</a></div>';
    
    $('#status_' + transaction.twitter_status_id).append(
            '<div class="block">' +
            '<div style="text-align:center; float:left; width:150px;">' +
            '<div style="text-align:center">' + transaction.status + '</div>' +
            '<div style="text-align:center">' + transaction.kind + '</div>' +
            '<div>' +
            '<a href="https://twitter.com/' + transaction.promoter_twitter_name + '">' + transaction.promoter_twitter_name + '</a>' +
            '<div>' +
            '</div>' +
            '</div>' +
            '</div>' +
            '<div style="float: left;width: 150px;">' +
            '<div style="text-align:center;">' + transaction.created_at + '</div>' +
            '<div style="text-align:center;">' + transaction.updated_at + '</div>' +
            '<div style="text-align:center;">' + transaction.wizard_score + '</div>' +
            '</div>' +
            '<div style="text-align:center"><img src="' + transaction.promoter_twitter_image + '"/>' + '</div>' +
            action_cell + 
            '<div style="text-align:center;">Transaction Id: ' + transaction.id + '</div>' +
            '</div>');
};
