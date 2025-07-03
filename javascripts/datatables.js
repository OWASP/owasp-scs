document$.subscribe(function() {
    const currentPage = window.location.pathname; // Get the current page URL path

    // List the pages where you want to disable sorting
    const pagesWithNoSorting = [
        '/checklists/SCSVS-ARCH/',
        '/checklists/SCSVS-CODE/',
        '/checklists/SCSVS-GOV/',
        '/checklists/SCSVS-AUTH/',
        '/checklists/SCSVS-COMM/',
        '/checklists/SCSVS-CRYPTO/',
        '/checklists/SCSVS-ORACLE/',
        '/checklists/SCSVS-BLOCK/',
        '/checklists/SCSVS-BRIDGE/',
        '/checklists/SCSVS-DEFI/',
        '/checklists/SCSVS-COMP/',
    ];


    if (pagesWithNoSorting.includes(currentPage)) {
        $('table').DataTable({
            paging: false,
            ordering: false, // Disable sorting
            dom: '<"top"if>rt<"bottom"lp><"clear">'
        });
    } else {
        $('table').DataTable({
            paging: true, // Enable pagination if needed
            ordering: true, // Enable sorting if needed
            dom: '<"top"if>rt<"bottom"lp><"clear">'
        });
    }
});