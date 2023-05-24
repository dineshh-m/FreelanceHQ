$(document).on('click', '.accept-proposal', function(event) {
    let element = $(event.target);
    let userProjectID = element.data('project-id');
    let proposedFreelancerID = element.data('freelancer-id');
    let feedID = element.data('feed-id');
    let proposalID = element.data('proposal-id');
    console.log("User project ID", userProjectID, "Proposed freelancer", proposedFreelancerID);
    
    event.preventDefault();

    $.ajax({
        url: "/api/create_workspace/",
        type: "POST",
        data: {
            userProjectID: userProjectID,
            proposedFreelancerID: proposedFreelancerID,
            proposalID: proposalID
        },
        success: function(response) {
            if(response.status == 'success') {
                $("#feed"+proposalID).remove()
                // $('#'+feedID).remove();
                $('#status'+'-accepted-'+proposalID).addClass('text-bg-success');
                $('#status'+'-accepted-'+proposalID).text('Accepted');
                console.log('#status'+'-accepted-'+proposalID)
                $('.'+userProjectID).remove();
            }
        }

    });
});

$(document).on('click', '.reject-proposal', function(event) {
    let element = $(event.target);
    let userProjectID = element.data('project-id');
    let proposedFreelancerID = element.data('freelancer-id');
    let feedID = element.data('feed-id')
    let proposalID = element.data('proposal-id')
    console.log("User project ID", userProjectID, "Proposed freelancer", proposedFreelancerID, "Proposal ID", proposalID);
    
    event.preventDefault();

    $.ajax({
        url: "/api/delete_proposal/",
        type: "POST",
        data: {
            userProjectID: userProjectID,
            proposedFreelancerID: proposedFreelancerID,
            proposalID: proposalID
        },
        success: function(response) {
            if(response.status == 'success') {
                $('#'+feedID).remove();
                // $('.'+userProjectID).remove();
                $('#status'+'-failed-'+proposalID).addClass('text-bg-danger')
                $('#status'+'-failed-'+proposalID).text('Rejected')
            }
        }

    });
});