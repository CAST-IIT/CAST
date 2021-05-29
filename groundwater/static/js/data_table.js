let selectedRowIds;
if (localStorage.getItem("rowIds") === null) {
    // No localStorage exists thereby create one
    selectedRowIds = [];
    localStorage.setItem("rowIds", JSON.stringify(selectedRowIds));
    console.log(`selectedRowIds: ${selectedRowIds} created in local storage`);
} else {
    // localStorage exists thereby fetch it
    selectedRowIds = JSON.parse(localStorage.getItem("rowIds"));
    console.log(`selectedRowIds: ${selectedRowIds} fetched from local storage`);
}
console.log("Selected row id's : " + selectedRowIds);

$(document).ready(function () {
    let table = $('#data-table').DataTable({
        "lengthChange": false,
        "lengthMenu":[ [5,10, 20, 50, -1], [5,10, 20, 50, "All"]],
        "columnDefs": [
            {
                "targets": [0],
                "visible": false,
            },
        ],
        dom: 'Bfrtip',
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
        "scrollY": true,
        "scrollX": true,
    });
    let table_similar = $('#similar-data-table').DataTable({
        "lengthChange": false,
        // "pageLength": 10,
        "lengthMenu":[ [5,10, 20, 50, -1], [5,10, 20, 50, "All"]],
        "columnDefs": [
            {
                "targets": [0],
                "visible": false,
            },
        ],
        dom: 'Bfrtip',
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
        "scrollY": true,
        "scrollX": true,
    });

    // Hide the column displaying the 'id' as the id here represent
    // row id in the database table
    let idColumn = table.column('id');
    idColumn.visible(!idColumn.visible);

    let idColumnSimilar = table_similar.column('id');
    idColumnSimilar.visible(!idColumnSimilar.visible);

    for (let i = 0; i < selectedRowIds.length; i++) {
        // There is an already selected row in the table
        // thereby select it again as on redirecting on the same
        // page it will be automatically un-selected
        $(`#${selectedRowIds[i]}_table`).toggleClass('selected');
    }

    // Set-up an onClick listener on each row to save the row id of the
    // selected row and remove the row id of the unselected row
    $("#data-table tbody").on('click', 'tr', function () {
        $(this).toggleClass('selected');
        let rowId = table.row(this).data()[0];
        if (selectedRowIds.includes(rowId)) {
            // Remove the rowId from the array
            selectedRowIds.splice(selectedRowIds.indexOf(rowId), 1);
            console.log("Deselected row id : " + rowId);
        } else {
            // Add the rowId to the array
            selectedRowIds.push(Number(rowId));
            console.log("Selected row id : " + rowId);
        }

        // Save the updated rowId's array to local-storage
        localStorage.setItem("rowIds", JSON.stringify(selectedRowIds));

    });
});
