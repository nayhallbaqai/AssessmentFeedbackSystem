/**
 * Created by nayhallbaqai on 22/01/2017.
 */

function getCourses(forMainContent) {

    var selected_course = $('#courses .active').attr('href');
    console.log(selected_course);
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

                    var course = $('#courses a[href="'+selected_course+'"]');
                    if (course.length == 0){
                        $('#viewStudents').attr('disabled', true);
                        getAssignments("All");
                    }else {
                        jQuery("#courses a").removeClass("active");
                        jQuery(course).addClass("active");
                        getAssignments(selected_course);
                    }
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
            getCourses(true);
        }
    });
    
}

function courseAssignToTutor(username, courses) {

    $.ajax({
        type: "POST",
        url: "/assignCourseToTutor/",
        data:{
            username: username,
            'courses[]': courses,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        dataType: "text",
        success: function (data) {
            alert(data);
        }
    });
}



$(document).ready(function(){

    // selectpicker for tutor
    // check if all selected then select all courses

    var selector = $('#tutorTab .selectpicker');
    selector.selectpicker();
    var allOptions = [];

    $("#tutorTab .selectpicker option").each(function()
    {
        allOptions.push($(this).val());
    });

    selector.change(function(e) {
        allValueCheck(selector, allOptions)
    });


    $('#submitCourse').click(function (e) {
        e.preventDefault();

        // checking which tab is used
        var isCourse = $('#courseTab').hasClass('active');

        if (isCourse){

        //    check course name is given
            var courseName = $('#courseTitle').val();
            // $('#courseTitle').val("");

            if (courseName == ""){
                var message = '<div class="alert alert-danger alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>Please enter a course name</div>';
                $('#courseResponse').html(message);
                return;
            }

            addCourse(courseName);
        }else{

            // add tutor

            var tutorUsername = $('#tutorUsername').val();
            var courses = getSelectedCourse(selector);

            if (tutorUsername == ""){
                var message = '<div class="alert alert-danger alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>Please add a username</div>';
                $('#tutorResponse').html(message);
                return;
            }

            if (courses == null){
                var message = '<div class="alert alert-danger alert-dismissable"><a href="#" class="close" data-dismiss="alert" aria-label="close">×</a>Please select a course</div>';
                $('#tutorResponse').html(message);
                return;
            }

            courseAssignToTutor(tutorUsername, courses); // courses need to add
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
