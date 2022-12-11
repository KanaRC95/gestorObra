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
/*
var trabajo;

$('#tp-name').click(function() {
   trabajo = $(this).attr('data-id');
});

$('#addObr').on('show.bs.modal', function (e) {
    var modal = $(this);
    var url = location.pathname.split('/').pop();;
    var obr = modal.find('.btn').attr('href');
    var link = '/assigOb/'+trabajo+'/'+obr+'/'+url;
    modal.find('.trbj').text(trabajo);
    modal.find('.btn-warning').attr('href',link);
});
*/