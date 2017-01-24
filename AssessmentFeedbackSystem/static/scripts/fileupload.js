/**
 * Created by nayhallbaqai on 15/12/2016.
 */

$(document).ready(function(){
    var selector = $('#uploadfile .selectpicker');
    var csvInput = $('#csvFileUpload');
    selector.selectpicker();
    var all = $('option[value="all"]');
    // console.log(all);


    var allOptions = [];
    $("#uploadfile .selectpicker option").each(function()
    {
        allOptions.push($(this).val());
    });

    selector.change(function(e) {

        var all = $('option[value=all]');
        if (all.is(':selected')) {
            if (getSelectedCourse().length == 0) {
                remove(allOptions,"all");
                selector.selectpicker("val",allOptions);
            } else {
                selector.selectpicker("deselectAll");

            }


        }
    });

    function remove(arr, what) {
        var found = arr.indexOf(what);
        while (found !== -1) {
            arr.splice(found, 1);
            found = arr.indexOf(what);
        }
    }

    function getSelectedCourse(){
        var selected = selector.val();
        if (selected !== null){
            remove(selected, "all");
        }
        return selected;
    }

    function checkCSV(){
        var ext = $("input#csvFileUpload").val().split(".").pop().toLowerCase();

        if($.inArray(ext, ["csv"]) === -1) {
            csvInput.replaceWith( csvInput = csvInput.clone( true ) );
            alert("Please upload a .csv file!");
            return false;
        }
    }

    function uploadStudents(course, students){

        $.ajax({
            type: "POST",
            url: "/addStudentByCSV/",
            data: {
                'courses[]' : course,
                students: JSON.stringify(students),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(data){
                alert(data);
            },
            dataType: 'html'
        });
    }

    csvInput.change(function(e){
        checkCSV();

        // if (e.target.files != undefined) {
        //     var reader = new FileReader();
        //     reader.onload = function(e) {
        //         var csvval=e.target.result.split("\n");
        //         var csvvalue=csvval[0].split(",");
        //         var inputrad="";
        //         console.log(csvval);
        //         for(var i=0;i<csvvalue.length;i++) {
        //             var temp=csvvalue[i];
        //             var inputrad=inputrad+" "+temp;
        //         }
        //         // $("#csvimporthint").html(inputrad);
        //         // $("#csvimporthinttitle").show();
        //     };
        //
        //     reader.readAsText(e.target.files.item(0));
        // }
        return false;
    });

    function checkHeader(listOfHeader){
        var isHeader = false;
        if (listOfHeader.length === 3){
            var id = (listOfHeader[0] == "ID");
            var firstname = (listOfHeader[1] == "Firstname");
            var surname = (listOfHeader[2] == "Surname");

            isHeader = id && firstname && surname;
        }else {
            isHeader = false;
        }

        return isHeader;
    }

    function csvFileChecking(csvDataInArray){
        if (csvDataInArray.length > 0) {
            if(checkHeader(csvDataInArray[0])){
                return true;
            }else{
                alert('CSV file header should be: ID, Firstname, Surname');
                return false;
            }
        } else {
            alert('No data in csv file');
            return false;
        }
    }

    $('form#addStudentByCSV').on('submit', function(e){
        e.preventDefault();
        var file = document.querySelector('input[name=file_upload]');
        checkCSV();

        var data = null;
        var csvObject = null;
        var course = [];
        // var file = csvInput1.files[0];
        // reader.readAsText(file);
        var reader = new FileReader();
        reader.readAsText(file.files[0]);
        reader.onload = function(event) {
            var csvData = event.target.result;
            data = $.csv.toArrays(csvData);
            var isValid = csvFileChecking(data);

            if (!isValid){
                csvInput.replaceWith( csvInput = csvInput.clone( true ) );
                return false;
            }else {
                csvObject = $.csv.toObjects(csvData);
                if (Object.keys(csvObject).length == 0){
                    csvInput.replaceWith( csvInput = csvInput.clone( true ) );
                    alert('No data in csv file');
                    return false;
                }else{
                    course = getSelectedCourse();
                    if (course == null){
                        alert('please select a course');
                        return false;
                    }else{
                        // console.log(typeof course);
                        uploadStudents(course, csvObject);
                    }
                }
            }
        };
        reader.onerror = function() {
            alert('Unable to read file');
        };


        // var csv = csvInput[0].files;
        // console.log(csv);
        // var formData = new FormData($(this)[0]);
        // formData.append('uploaded_file', csvInput[0].files[0]);
        // formData.append('lastModifed', csv[0].lastModified);
        // formData.append('fileName', csv[0].name);
        // console.log(formData);


        // $.ajax({
        // url: '{{ URL::route("file_upload") }}',
        // type: 'POST',
        // data: formData,
        // async: true,
        // cache: false,
        // contentType: false,
        // processData: false,
        // success: function (returndata) { //alert(returndata); return false;
        //
        // }
        // });

    });

    // $('#addStudentByCSV').validate({ // initialize the plugin
    //     rules: {
    //         field1: {
    //             required: true,
    //             extension: "csv"
    //         }
    //     },
    //     submitHandler: function (form) { // for demo
    //         alert('valid form submitted'); // for demo
    //         return false; // for demo
    //     }
    // });

});