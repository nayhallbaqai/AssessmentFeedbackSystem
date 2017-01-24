
function getCourses() {
    $.ajax({
            url:"/getUserCourses/",
            method:"GET",
            dataType: "html",
            success:function(data){
                $('#courses').html(data);
            }
        });
}

$(document).ready(function(){
    // function getCourses(addingAssignment) {
    //     if (addingAssignment) {
    //         $.ajax({
    //         url:"getUserCourses/",
    //         method:"GET",
    //         dataType: "html",
    //         success:function(data){
    //             $('#').html(data);
    //         }
    //         });
    //     }
    //     $.ajax({
    //         url:"/getUserCourses/",
    //         method:"GET",
    //         dataType: "html",
    //         success:function(data){
    //             $('#courses').html(data);
    //         }
    //     });
    // }

    getCourses();

    function getAssignments(courseID){
        // var linkToSend = "/getCourseAssignment/";
        // if (courseID == "All") linkToSend = "/getAllAssignment/";

        $.ajax({
            url:"/ajax_assignment/",
            method:"POST",
            data:{
                id : courseID,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "html",
            success:function(data){
                $('#assignment').html(data);
            }
        });
    }

    $(document).on('click', '#course a', function(e){
        jQuery("#courses a").removeClass("active");
		jQuery($(this)).addClass("active");
        var courseID = $(this).attr('href');
        getAssignments(courseID);

    });

    $(document).on('click', '#addAssignment', function(){
        var selectedCourseID = $('#courses .active').attr('href');

    });

});