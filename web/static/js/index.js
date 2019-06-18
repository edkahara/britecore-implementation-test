$(document).ready(function(){
  $('select').formSelect();
  $('.datepicker').datepicker({
    minDate : new Date()
  });
  $('.modal').modal();
  $('.collapsible').collapsible();
  $('.sidenav').sidenav();
  $('.title').characterCounter();

  $.validator.addMethod("regex", function(value, element, regex) {
    return regex.test(value);
  });

  $('form').each(function () {
    $(this).validate({
      rules: {
        title: {
          required: true,
          maxlength: 50,
          regex: /^\S/
        },
        description: {
          required: true,
          regex: /^\S/
        },
        clientId: "required",
        priority: "required",
        productId: "required",
        targetDate: "required"
      },
      messages: {
        title: {
          required: "enter the title",
          maxlength: "title is too long",
          regex: "title cannot be blank"
        },
        description: {
          required: "enter the description",
          regex: "description cannot be blank"
        },
        clientId: {
          required: "choose the client"
        },
        priority: {
          required: "enter the client priority"
        },
        productId: {
          required: "choose the product area"
        },
        targetDate: {
          required: "enter the target date"
        },
      },
      errorElement : 'div',
      errorPlacement: function(error, element) {
        var placement = $(element).data('error');
        if (placement) {
          $(placement).append(error);
        } else {
          error.insertAfter(element);
        }
      }
    });
  });

  $('.viewButton').click(function() {
    var requestId = $(this).data("edit");
    $.get("/" + requestId, function(data) {
      $('.card-title h4').text(data.title);
      $('.card-content p').text(data.description);
    });
  });

  var months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];

  function formatDate(date) {
	  return months[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear();
  }

  $('.editButton').click(function() {
    var requestId = $(this).data("edit");
    $.get("/" + requestId, function(data) {
      date = new Date(data.targetDate);

      $('#editForm').attr('action', '/update/' + data.id);
      $("#title").val(data.title);
      $("#description").val(data.description);
      $("#clientId").val(data.clientId);
      $("#priority").val(data.priority);
      $("#productId").val(data.productId);
      $("#targetDate").val(formatDate(date));
      M.updateTextFields();
    });
  });
});
