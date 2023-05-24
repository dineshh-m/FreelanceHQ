// $(document).ready(function() {
//     $('.close-workspace').on('click', function(event) {
//         let workspaceID = $("#workspace-id").data();
//         console.log("Clicked");
//         deleteWorkspace(workspaceID);
//         console.log("CLICKED");
//     })
// });

// function deleteWorkspace(workspaceID) {
//     $.ajax({
//         url: "/delete_workspace",
//         type: "POST",
//         data: {
//             workspaceID: workspaceID
//         },
//         success: function(response) {
//             if(response.status == 'success') {
//                 console.log("Workspace Deleted");
//                 window.location.href="/";
//             }
//         },
//         error: function(xhr, status, error) {
//             console.log("Error deleting workspace "+ error);
//         }
//     });
// }