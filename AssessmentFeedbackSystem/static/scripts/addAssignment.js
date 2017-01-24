function getAssignments(courseID) {
        // var linkToSend = "/getCourseAssignment/";
        // if (courseID == "All") linkToSend = "/getAllAssignment/";

    $.ajax({
        url: "/ajax_assignment/",
        method: "POST",
        data: {
            id: courseID,
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        dataType: "html",
        success: function (data) {
            $('#assignment').html(data);
        }
    });

}

function addAssignment(title, selected_course, courseToUpdate){
    $.ajax({
        type: "POST",
        url: "/addAssignment/",
        data: {
            'course_id' : selected_course,
            'title' : title,
            'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(data) {
            $("#response").html(data);
            $('.modal-body input').val("");

            getAssignments(courseToUpdate);
        },
        dataType:'html'
    });
}

$(function(){

    // $('#addAssignment').click(function (e) {
    //     e.preventDefault();
    //     $('#assignmentModel').modal({
    //             show: true
    //         });
    // });

    // $('#assignmentModal').on('show.bs.modal', function(e){
    //     var button = $(e.relatedTarget);
    //     var data = button.data('whatever');
    //
    //     // var js_list = "{{courses}}";
    //     // console.log(js_list);
    //
    //     if (data=='addAssignment'){
    //         $('.modal-body').html('<div class="form-group">' +
    //                                     '<label for="assignment-title" class="control-label">Title:</label>' +
    //                                     '<input type="text" class="form-control" id="title">' +
    //                                 '</div>' +
    //                                 '<div class="form-group">' +
    //                                     '<label for="course-select" class="control-label">Course:</label>'+
    //                                     '<select class="selectpicker" data-live-search="true">' +
    //                                         '{% for course in courses %}' +
    //                                             '<option data-tokens="{{ course.name }}" value="{{ course.pk }}">{{ course.name }}</option>' +
    //                                         '{% endfor %}' +
    //                                     '</select>'+
    //                                 '</div>'
    //         );
    //     }else if( data=='addStudent'){
    //         // $('.modal-body').append('')
    //
    //     }else{
    //
    //     }
    // });

    $('#assignmentModal').on('hide.bs.modal', function(e){
        $('#response').empty();
        // $('.selectpicker').attr(':selected', false);
        // $("option:selected").removeAttr("selected");
        // $(".selectpicker option").prop(":selected", false);
    });

    $('#submitAssignment').click( function (e) {
        e.preventDefault();
        var title = $('#title').val();
        $('#title').val("");
        var selected_course = $('#assignmentModal .selectpicker').find(":selected").val();

        var courseToUpdate = $('#courses .active').attr('href');

        if (title == ""){
            $("#response").html('<label for="course-select" class="control-label">Title is empty!</label><br/>');
            return false;
        }
        addAssignment(title, selected_course, courseToUpdate)
    });
});

// $(document).ready(function(){
//     if (!$('#assignmentModal').hasClass('in')){
//         console.log("not showing");
//         // $("#assignmentModal .modal-body").empty();
//         // $("#assignmentModal .modal-body").html('');
//     }

// });
// $('.close').click( function () {
//     $("#assignmentModal .modal-body").empty();
//     alert("h");
// });