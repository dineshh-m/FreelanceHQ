$(document).on('click', ".apply", function(event) {
    let element = event.target;
    let projectID = $(element).data('project-id')
    let freelancerID = $(element).data('freelancer-id')
    console.log("ProjectID", projectID, "FreelancerID", freelancerID)

    event.preventDefault();
    $.ajax({
        url: "/apply/project/"+projectID,
        type: "POST",
        data: {
            projectID: projectID,
            freelancerID: freelancerID
        },
        success: function(response) {
            let status = response.status;
            if(status == 'success') {
                $(element).text("Unapply")
                $(element).removeClass('apply btn-outline-dark')
                $(element).addClass('unapply btn-outline-danger')
                console.log("Apply response returned");
            }
            
        }
    });
});

$(document).on('click', ".unapply", function(event) {
    let element = event.target;
    let projectID = $(element).data('project-id')
    let freelancerID = $(element).data('freelancer-id')
    console.log("ProjectID", projectID, "FreelancerID", freelancerID)

    event.preventDefault();
    $.ajax({
        url: "/unapply/project/"+projectID,
        type: "POST",
        data: {
            projectID: projectID,
            freelancerID: freelancerID
        },
        success: function(response) {
            let status = response.status;
            if(status == 'success') {
                $(element).text("Apply")
                $(element).removeClass('unapply btn-outline-danger')
                $(element).addClass('apply btn-outline-dark')
                console.log("Unpply response returned");
            }
        }
    });
});