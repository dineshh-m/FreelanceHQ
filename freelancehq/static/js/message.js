$(document).ready(function() {
    var element = $(".received-messages");
    
    // Load the content dynamically here
    // ...
    
    // After the content is loaded
    var scrollHeight = element.prop("scrollHeight");
var containerHeight = element.height();
element.scrollTop(scrollHeight - containerHeight);
  });

$(document).on('click', '#send-btn', function(event) {
    let chatbox = $('#chatbox');
    let workspaceID = $('#workspace').data('workspace-id');
    let message = chatbox.val();
    let sender_id = $('#userid').data('user-id');
    let messageContainer =  $('.received-messages');

    messageContainer.append('<div class="you d-flex justify-content-between"><div><span class="font-weight-bold">You: </span>'+message+'</div><div class="time text-muted">'+new Date().toLocaleString()+'</div>'+'<div class="status"><img width="20px" src="/static/images/clock.svg" alt=""></div></div>');
    var element = $(".received-messages");
    var scrollHeight = element.prop("scrollHeight");
    element.scrollTop(scrollHeight);
    // messageContainer.append('');

    console.log(workspaceID, message, sender_id);

    event.preventDefault();
    $.ajax({
        url: '/api/message',
        type: 'POST',
        data: {
            workspaceID: $('#workspace').data('workspace-id'),
            message: chatbox.val(),
            senderID: $('#userid').data('user-id')
        },
        success: function(response) {
            let status = response.status;
            if(status == 'success'){
                messageContainer.find('.status img').attr("src", "/static/images/done.svg");
            }
        }
    });
});