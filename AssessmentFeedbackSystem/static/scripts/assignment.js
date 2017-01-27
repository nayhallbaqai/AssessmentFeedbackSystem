$(function(){
    $('#viewStudents').attr('disabled', true);
    setCourseListener();

});


function setCourseListener() {

    $('#courses a').click(function(e){
        e.preventDefault();
        jQuery("#courses a").removeClass("active");
		jQuery($(this)).addClass("active");

        var checkAll = $(this).attr('href');

        if (checkAll == "All") $('#viewStudents').attr('disabled', true);
        else $('#viewStudents').attr('disabled', false);

        getAssignments(checkAll);
    });

}