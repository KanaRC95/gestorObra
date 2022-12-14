function toggleJobs() {
    var lTable = document.getElementById("tablaJobsR");
    lTable.style.display = (lTable.style.display == "table") ? "none" : "table";
}

function toggleJobsD() {
    var lTable = document.getElementById("tablaJobsD");
    lTable.style.display = (lTable.style.display == "table") ? "none" : "table";
}

function toggleJobsP() {
    var lTable = document.getElementById("tablaJobsP");
    lTable.style.display = (lTable.style.display == "table") ? "none" : "table";
}

var obr;

$('#darBaja').click(function() {
   obr = $(this).attr('data-id');
});

$('#baja').on('show.bs.modal', function (e) {
    var modal = $(this);
    modal.find('.ced').attr('value',obr)
    //modal.find('.testo').attr('href',obr);
});
