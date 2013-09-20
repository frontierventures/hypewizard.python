$(document).ready(function(){
    var kind = $('input[name*=kind]').val();
    build_grid(kind);
});
function build_grid(kind) {
    if (kind == 'client') {
        $('.asks').empty();
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
            add_ask_to_market(response.rule, response.orders[i]);
    }

    if (kind == 'promoter') {
        $('.bids').empty();
        var response = {};
        $.ajax({
            url: '../get_bids',
            async: false,
            cache: false,
            dataType: 'json',
            fail: function() { response.error = true }, 
            success: function(data) {
                response = data;
            }
        });
        for (var i = 0; i < response.orders.length; i++)
            add_bid_to_market(response.rule, response.orders[i]);
    }
};
function add_ask_to_market(rule, ask) { 
    var action_url = '../feature_disabled?reason=not_authorized';
    if (rule != 'limit')
        action_url = '../process_ask?action=engage&id=' + ask.id; 

    $('.asks').append(
            '<tr>' + 
            '<td style="text-align:center">' + ask.niche + '</td>' +
            '<td style="text-align:center"><a href="https://twitter.com/' + ask.twitter_name + '">' + ask.twitter_name + '</td>' +
            '<td style="text-align:center"><a href="https://twitter.com/' + ask.twitter_name + '/status/' + ask.status_id + '">' + ask.status_id + '</td>' +
            '<td style="text-align:center">' + ask.campaign_type + '</td>' +
            '<td style="text-align:center">' + ask.cost + '</td>' +
            '<td style="text-align:center"><a href="' + action_url + '">Engage Client</a></td>' +
            '</tr>');
};
function add_bid_to_market(rule, bid) { 
    var user = {};
    $.ajax({
        url: '../get_user?twitter_name=' + bid.twitter_name,
        async: false,
        cache: false,
        dataType: 'json',
        fail: function() { response.reload = false }, 
        success: function(data) {
            user = data;
        }
    });
    
    var action_url = '../feature_disabled?reason=not_authorized';
    if (rule != 'limit')
        action_url = '../process_bid?action=engage&id=' + bid.id; 

    $('.bids').append(
            '<tr>' + 
            '<td style="text-align:center">' + bid.niche + '</td>' +
            '<td style="text-align:center"><a href="http://twitter.com/' + bid.twitter_name + '">' + bid.twitter_name + '</td>' +
            '<td style="text-align:center">' + user.statuses_count + '</td>' +
            '<td style="text-align:center">' + user.followers_count + '</td>' +
            '<td style="text-align:center">' + bid.campaign_type + '</td>' +
            '<td style="text-align:center">' + bid.cost + '</td>' +
            '<td style="text-align:center"><a href="' + action_url + '">Engage Promoter</a></td>' +
            '</tr>');
};
