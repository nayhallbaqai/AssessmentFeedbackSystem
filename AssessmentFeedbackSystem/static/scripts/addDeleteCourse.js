/**
 * Created by nayhallbaqai on 22/01/2017.
 */

function getCourses(forMainContent) {
    $.ajax({
            url:"/getUserCourses/",
            method:"POST",
            dataType: "html",
            data:{
                forMainContent: forMainContent,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success:function(data){
                if (forMainContent){
                    $('#courses').html(data);
                    setCourseListener();
                    getAssignments('All');
                    getCourses(false);
                }else{
                    // for select pickers

                    $('#assignmentModal .selectpicker').html(data).selectpicker('refresh');

                    $('#deleteCourseModal .selectpicker').html(data).selectpicker('refresh');

                    $('#uploadfile .selectpicker').html('<option data-tokens="all" value="all">Select / Deselect All</option>'+data).selectpicker('refresh');

                    $('#tutorTab .selectpicker').html('<option data-tokens="all" value="all">Select / Deselect All</option>'+data).selectpicker('refresh');


                }
            }
        });
}

function addCourse(name){
    $.ajax({
        type: "POST",
        url: "/addCourse/",
        data: {
            name : name,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function(data) {
            var message = '<div class="alert alert-success alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>' + data + '</div>';
            // var message = '<br/><label class="control-label">'+data+'</label><br/>';
            $('#courseResponse').html(message);
            // getCourses();
            $('.modal-body input').val("");
            // getCourses(true);
            getCourses(true);
        },
        dataType:'text'
    });
}

function deleteCourse(course_id) {

    $.ajax({
        type: "POST",
        url: "/deleteCourse/",
        data:{
            course_id: course_id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        dataType: "text",
        success: function (data) {
            $('#')
            getCourses(true);
        }
    });
    
}



$(document).ready(function(){

    $('#submitCourse').click(function (e) {
        e.preventDefault();

        // checking which tab is used
        var isCourse = $('#courseTab').hasClass('active');

        if (isCourse){

        //    check course name is given
            var courseName = $('#courseTitle').val();
            // $('#courseTitle').val("");

            if (courseName == ""){
                $('#courseResponse').html('<label class="control-label">Please enter a course name</label><br/>');
                return;
            }

            addCourse(courseName);
        }else{

            // add tutor
        }

    });

    $('#addCourseModal').on('hide.bs.modal', function(e){
        $('#courseResponse').empty();
        $('#tutorResponse').empty();
        // $('.selectpicker').attr(':selected', false);
        // $("option:selected").removeAttr("selected");
        // $(".selectpicker option").prop(":selected", false);
    });


    $('#submitDeleteCourse').click(function (e) {
        e.preventDefault();

        var selected_course = $('#deleteCourseModal .selectpicker').find(":selected").val();

        if (confirm('Are you sure you want to delete this?')){
            deleteCourse(selected_course);
        }

    });
});
