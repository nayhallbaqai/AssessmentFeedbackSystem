$(document).ready(function(){

    function getActiveCourseID(){
        return $('#courses .active').attr('href');
    }

    function fetch_data() {
        $.ajax({
            url:"/students/",
            method:"GET",
            dataType: "html",
            success:function(data){
                $('#live_data').html(data);
            }
        });
    }

    function fetch_data_by_courseID(courseID) {
        $.ajax({
            url:"/classList/",
            method:"POST",
            data: {
                course_id: courseID,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "html",
            success:function(data){
                $('#live_data').html(data);
            }
        });
    }

    $('#viewStudentModal').on('show.bs.modal', function(){
        var selectedCourseID = getActiveCourseID();
        var selectedCourseVal = $('#courses .active').text();
        $('#viewStudentModal .modal-title').text(selectedCourseVal + " class list");
        fetch_data_by_courseID(selectedCourseID);
    });

    $(document).on('click', '#btn_add', function(){
        var student_id = $('#student_id').text();
        var first_name = $('#first_name').text();
        var last_name = $('#last_name').text();
        var course_id = getActiveCourseID();
        if(student_id == '') {
            alert("Enter student id");
            return false;
        }

        $.ajax({
            url:"/addStudent/",
            method:"POST",
            data:{
                student_id: student_id,
                first_name: first_name,
                last_name: last_name,
                course_id: course_id,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType:"text",
            success:function(data) {
                alert(data);
                fetch_data_by_courseID(course_id);
            }
        });
    });

    function edit_data(id, text, column_name) {
        $.ajax({
            url:"/changeStudent/",
            method:"POST",
            data:{
                id :id,
                text :text,
                column_name :column_name,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "text",
            success: function(data){

            }
        });
    }
      // $(document).on('blur', '.student_id', function(){
      //     var id = $(this).data("id0");
      //     var student_id = $(this).text();
      //     edit_data(id, student_id, "student_id");
      // });
    $(document).on('blur', '.first_name', function(){
        var id = $(this).data("id1");
        var first_name = $(this).text();
        edit_data(id, first_name, "first_name");
    });
    $(document).on('blur', '.last_name', function(){
        var id = $(this).data("id2");
        var last_name = $(this).text();
        edit_data(id,last_name, "last_name");
    });

    $(document).on('click', '.btn_delete', function(){
        var id = $(this).data("id3");
        var course_id = getActiveCourseID();
        if(confirm("Are you sure you want to delete this?")) {
            $.ajax({
                url:"/removeStudent/",
                method:"POST",
                data:{
                    student_id:id,
                    course_id: course_id,
                    'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
                },
                success:function(data){
                    fetch_data_by_courseID(course_id);
                },
                dataType:"text"
            });
        }
    });

 });