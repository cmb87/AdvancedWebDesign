var button = document.getElementById("enter");
var input = document.getElementById("userinput");
var ul = document.querySelector("ul");

button.addEventListener("click", function() {
  var li = document.createElement("li");
  li.className = 'list-group-item';
  li.textContent = input.value;
  ul.appendChild(li);
})

function showDetails(clickedElement) {
    var dataid = $(clickedElement).attr("data-id");
    showDetailsAjax(dataid);
}

function showDetailsAjax(activityAdID) {
    var link = '@Url.Action("_PartialDetails", "ActivityAds", new { id = "-1"})'
    link = link.replace("-1", activityAdID);

    $.ajax({
        type: "GET",
        url: link,
        error: function(data)
        {},
        success: function (data) {
            $("#detailsModal .modal-body").html(data);
            $('#detailsModal').modal('show');
        },
    });
}
