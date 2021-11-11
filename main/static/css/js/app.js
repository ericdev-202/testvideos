$('.handle').on('click',function(){
	$('nav ul').toggleClass('showing');
});



  $(document).ready(function(){
        $(function(){
        $("#exampleModal").dialog({
          autoOpen: false,
          width: 400,
    });
        $(".js-create-student").on("click", function(){

          $("#exampleModal").dialog("open");
    });
  });
  $("form#student-form").on("submit",function GetTableData(e){  
    e.preventDefault();
    $.ajax({
      type:'POST',
      url:'{% url "student" %}',
      data:{
        mdate:$('#mdate').val(),        
        description:$('#description').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
  
      },
      success:function(data){
        if (data.student) {
          appendTomy_student(data.student);
        }
        alert("You Have Successfully Posted the Workdone!")
      }
      // success:function(data){
      //  document.getElementById("event-form").reset();
      //  $("#my_event tbody").append(
      //    '<tr><td>${fields["title"]||""}</td><td>${fields["description"]||""}</td><td>${fields["venue"]||""}</td><td>${fields["mdate"]||""}</td><td>${fields["mtime"]||""}</td></tr>'
      //    ) 
      // },
      // error : function(xhr,errmsg,err){
      //  console.log(xhr.status + ":" + xhr.responseText);
      // }
    });

    $('form#student-form').trigger("reset");
    return false;
    // body...
  });

});
  function appendTomy_student(student){
    $("#my_student > tbody:last-child").append(
      '<tr id="student-${student.id}"><td class="studentDate" name="mdate">${student.mdate}</td><td class="studentWorkdone" name="workdone">${student.workdone}</td><td><button type="button" class="btn btn-warning btn-sm " onClick="editStudent({{student.id}})" data-toggle="modal" data-target="#myModal"><span class="glyphicon glyphicon-pencil">Edit</span></button><button type="button" class="btn btn-danger btn-sm" onClick="deleteStudent({{student.id}})"><span class="glyphicon glyphicon-trash">Delete</span></button></td></tr>'
      )
  }   