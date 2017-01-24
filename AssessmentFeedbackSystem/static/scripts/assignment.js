$(function(){
    setCourseListener();

});


function setCourseListener() {
    $('#viewStudents').attr('disabled', true);
    $('#courses a').click(function(e){
        e.preventDefault();
        jQuery("#courses a").removeClass("active");
		jQuery($(this)).addClass("active");

        var checkAll = $(this).attr('href');

        if (checkAll == "All") $('#viewStudents').attr('disabled', true);
        else $('#viewStudents').attr('disabled', false);

        $.ajax({
            type: "POST",
            url: "/ajax_assignment/",
            data: {
                'id' : checkAll,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function (data) {
                $('#assignment').html(data);
            },
            dataType: 'html'
        });
    });

}