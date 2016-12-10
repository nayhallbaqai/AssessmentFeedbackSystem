$(function(){
    $('#courses a').click(function(e){
        e.preventDefault();
        jQuery("#courses a").removeClass("active");
		jQuery($(this)).addClass("active");

        $.ajax({
            type: "POST",
            url: "/ajax_assignment/",
            data: {
                'id' : $(this).attr('href'),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: assignmentSuccess,
            dataType: 'html'
        });
    });
});


function assignmentSuccess(data, textStatus, jqXHR){

    $('#assignment').html(data);
}