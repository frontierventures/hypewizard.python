$(document).ready(function(){
    var kind = $('input[name*=kind]').val();
    build_grid(kind);

    $('a[href*=feature_disabled]').colorbox({
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
            if (response.reason == 'unauthorized') {
                $('#feature_disabled_alert').empty();
                $('#feature_disabled_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
                $.colorbox.resize();
                return "#feature_disabled_popup";
            }
            if (response.reason == 'unverified') {
                $('#feature_disabled_alert').empty();
                $('#feature_disabled_alert').append('<div class="alert alert-error" id="alert">' + response.message + '</div>');
                $.colorbox.resize();
                return "#feature_disabled_popup";
            }
        }      
    });
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
    if (!ask.engage.is_allowed && ask.engage.reason == 'different_user') {
        action_url = '../process_ask?action=withdraw&id=' + ask.id; 
        action_cell = '<div style="text-align:center"><a href="' + action_url + '">Withdraw</a></div>';
    }

    if (!ask.engage.is_allowed && ask.engage.reason == 'unverified') {
        var action_url = '../feature_disabled?reason=unverified';
        var action_cell = '<div style="text-align:center"><a href="../">View Tweet</a> <a href="' + action_url + '">Engage Client</a></div>';
    }

    if (!ask.engage.is_allowed && ask.engage.reason == 'unauthorized') {
        var action_url = '../feature_disabled?reason=unauthorized';
        var action_cell = '<div style="text-align:center"><a href="../">View Tweet</a> <a href="' + action_url + '">Engage Client</a></div>';
    }

    if (ask.engage.is_allowed) {
        action_url = '../process_ask?action=engage&id=' + ask.id; 
        action_cell = '<div style="text-align:center"><a href="../">View Tweet</a> <a href="' + action_url + '">Engage Client</a></div>';
    }

    //$('.asks').append(
    //        '<div class="block">' + 
    //        '<div style="text-align:center">' + ask.niche + '</div>' +
    //        '<div style="text-align:center"><a href="https://twitter.com/' + ask.twitter_name + '">' + ask.twitter_name + '</a></div>' +
    //        '<div style="text-align:center; font-size: 16px"><a href="https://twitter.com/' + ask.twitter_name + '/status/' + ask.twitter_status_id + '">' + ask.twitter_status_text + '</a></div>' +
    //        '<div style="text-align:center">' + ask.campaign_type + '</div>' +
    //        '<div style="text-align:center">' + ask.target + ' of ' + ask.goal + '</div>' +
    //        '<div style="text-align:center">' + ask.cost + '</div>' +
    //        action_cell + 
    //        '</div>'); 

    $('.asks').append(
            '<div class="block">' +
            '<div style="text-align:center;float: left;width: 150px;">' +
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
            action_cell + 
            '<hr />' +
            '</div>');
};
function add_bid_to_market(rule, bid) { 
    var user = {};
    $.ajax({
        url: '../get_user?twitter_id=' + bid.twitter_id,
        async: false,
        cache: false,
        dataType: 'json',
        fail: function() { response.reload = false }, 
        success: function(data) {
            user = data;
        }
    });
    if (!bid.engage.is_allowed && bid.engage.reason == 'different_user') {
        action_url = '../process_bid?action=withdraw&id=' + bid.id; 
        action_cell = '<div style="text-align:center"><a href="' + action_url + '">Withdraw</a></div>';
    }

    if (!bid.engage.is_allowed && bid.engage.reason == 'unverified') {
        var action_url = '../feature_disabled?reason=unverified';
        var action_cell = '<div style="text-align:center"><a href="' + action_url + '">Engage Promoter</a></div>';
    }

    if (!bid.engage.is_allowed && bid.engage.reason == 'unauthorized') {
        var action_url = '../feature_disabled?reason=unauthorized';
        var action_cell = '<div style="text-align:center"><a href="' + action_url + '">Engage Promoter</a></div>';
    }

    if (bid.engage.is_allowed) {
        action_url = '../process_bid?action=engage&id=' + bid.id; 
        action_cell = '<div style="text-align:center"><a href="' + action_url + '">Engage Promoter</a></div>';
    }

    $('.bids').append(
            '<div class="block">' + 
            '<div style="text-align:center">' + bid.niche + '</div>' +
            '<div style="text-align:center"><a href="http://twitter.com/' + bid.twitter_name + '">' + bid.twitter_name + '</a></div>' +
            '<div style="text-align:center"> (S: ' + user.statuses_count + ', F: ' + user.followers_count + ')</div>' +
            '<div style="text-align:center">' + bid.campaign_type + '</div>' +
            '<div style="text-align:center">' + bid.cost + '</div>' +
            action_cell + 
            '</div>');
};
