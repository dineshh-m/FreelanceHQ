// $(function() {
//     $('#my-textarea').on('input', function() {
//       $.ajax({
//         url: '/api/suggest',
//         type: 'POST',
//         data: { text: $('#my-textarea').val() },
//         success: function(response) {
//           $('#my-textarea').val(response.suggestions);
//         }
//       });
//     });
//   });

// $(function() {
//   $('#my-textarea').on('input', function() {
//     var text = $('#my-textarea').val();
//     if (text.length > 0) {
//       $.ajax({
//         url: '/api/suggest',
//         type: 'POST',
//         data: { text: text },
//         success: function(response) {
//           var suggestions = response.suggestions;
//           var html = '';
//           for (var i = 0; i < suggestions.length; i++) {
//             html += '<div class="suggestion">' + suggestions[i] + '</div>';
//           }
//           $('#suggestion-box').html(html);
//         }
//       });
//     } else {
//       $('#suggestion-box').html('');
//     }
//   });
// });
var timeout = null;
const skills = [];

$(function() {
  $('#my-textarea').on('input', function() {
    var text = $('#my-textarea').val();
    if (text.length > 0) {
      clearTimeout(timeout);
      timeout = setTimeout(function() {
        $.ajax({
          url: '/api/suggest',
          type: 'POST',
          data: { text: text },
          success: function(response) {
            var suggestions = response.suggestions;
            var html = '';
            for (var i = 0; i < suggestions.length; i++) {
              html += '<div class="suggestion"' + 'data-skill-id='+ suggestions[i][0] +  '>' + suggestions[i][1] + '</div>';
            }
            $('#suggestion-box').html(html);
          }
        });
      }, 500); // Set the delay here (in milliseconds)
    } else {
      $('#suggestion-box').html('');
    }
  });
});

// For skill textarea
$("#my-textarea").on("blur", function() {
  setTimeout(function() { $("#suggestion-box").css("display", "none"); }, 500)
  
});

$("#my-textarea").on("focus", function() {
  $("#suggestion-box").css("display", "block");
});

$(document).on("click", ".suggestion", function() {
  let skill = $(event.target).text();
  let skillId = $(event.target).data('skill-id')
  console.log(skill);

  if(!skills.includes(skill)) {
    skills.push(skill);
    $("#skill-box").append('<div class="skill" data-value='+'"' + skillId + '"' +  '>' + skill + '</div>');
  }

});
  

// $(".suggestion").on("click", function(event) {
//   console.log("hel");
//   let skill = $(event.target).text();
//   console.log(skill);
//   $("#skill-box").append('<div class="skill">' + skill + '</div>');
// })

$('#profile-submit').click(function(event) {
  event.preventDefault(); // prevent form from submitting

  const form = $('#profile-form');
  const div = $('#skill-box');
  const nestedDivs = div.find('.skill');

  nestedDivs.each(function(index) {
    const input = $('<input>').attr({
      type: 'hidden',
      name: 'nested-values[]',
      value: $(this).data('value')
    });
    form.append(input);
  });

  form.submit(); // submit the form with the hidden input fields
});

// $(document).on("click", "#submit-bu")

$('#post-submit').click(function(event) {
  event.preventDefault(); // prevent form from submitting

  const form = $('#post-form');
  const div = $('#skill-box');
  const nestedDivs = div.find('.skill');

  nestedDivs.each(function(index) {
    const input = $('<input>').attr({
      type: 'hidden',
      name: 'nested-values[]',
      value: $(this).data('value')
    });
    form.append(input);
  });

  form.submit(); // submit the form with the hidden input fields
});