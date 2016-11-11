//
    // If absolute URL from the remote server is provided, configure the CORS
    // header on that server.
    //
    // var url = './helloworld.pdf';
    var mycontext = document.location.href.split('/');
    var clongit = mycontext.length;
    if (mycontext[clongit - 1].indexOf("?_authenticator=") !== -1){
      mycontext.pop();
    }
    mycontext.push('view');
    mycontext.push('++widget++form.widgets.file');
    mycontext.push('download');
    // context.splice(context.length - 1, 1, 'download');
    var url = mycontext.join('/');

    ////////////////////////////////////////////////////
    //
    // Disable workers to avoid yet another cross-origin issue (workers need
    // the URL of the script to be loaded, and dynamically loading a cross-origin
    // script does not work).
    //
    // PDFJS.disableWorker = true;
    //
    // The workerSrc property shall be specified.
    //
    // PDFJS.workerSrc = '../../build/pdf.worker.js';
    PDFJS.workerSrc = '++resource++matem.planning/pdf.worker.js';
    //
    // Asynchronous download PDF
    //
    PDFJS.getDocument(url).then(function getPdfHelloWorld(pdf) {
      //
      // Fetch the first page
      //
      pdf.getPage(1).then(function getPageHelloWorld(page) {
        var scale = 1.5;
        var viewport = page.getViewport(scale);
        //
        // Prepare canvas using PDF page dimensions
        //
        var canvas = document.getElementById('the-canvas');
        var context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;
        //
        // Render PDF page into canvas context
        //
        var renderContext = {
          canvasContext: context,
          viewport: viewport
        };
        page.render(renderContext);
      });
    });

    ////////////////////////////////////////////////////
    // var pdfDoc = null,
    //   pageNum = 1,
    //   pageRendering = false,
    //   pageNumPending = null,
    //   scale = 0.8,
    //   canvas = document.getElementById('the-canvas'),
    //   ctx = canvas.getContext('2d');
    // /**
    //  * Get page info from document, resize canvas accordingly, and render page.
    //  * @param num Page number.
    //  */
    // function renderPage(num) {
    //   pageRendering = true;
    //   // Using promise to fetch the page
    //   pdfDoc.getPage(num).then(function(page) {
    //     var viewport = page.getViewport(scale);
    //     canvas.height = viewport.height;
    //     canvas.width = viewport.width;
    //     // Render PDF page into canvas context
    //     var renderContext = {
    //       canvasContext: ctx,
    //       viewport: viewport
    //     };
    //     var renderTask = page.render(renderContext);
    //     // Wait for rendering to finish
    //     renderTask.promise.then(function () {
    //       pageRendering = false;
    //       if (pageNumPending !== null) {
    //         // New page rendering is pending
    //         renderPage(pageNumPending);
    //         pageNumPending = null;
    //       }
    //     });
    //   });
    //   // Update page counters
    //   document.getElementById('page_num').textContent = pageNum;
    // }
    // /**
    //  * If another page rendering in progress, waits until the rendering is
    //  * finised. Otherwise, executes rendering immediately.
    //  */
    // function queueRenderPage(num) {
    //   if (pageRendering) {
    //     pageNumPending = num;
    //   } else {
    //     renderPage(num);
    //   }
    // }
    // /**
    //  * Displays previous page.
    //  */
    // function onPrevPage() {
    //   if (pageNum <= 1) {
    //     return;
    //   }
    //   pageNum--;
    //   queueRenderPage(pageNum);
    // }
    // document.getElementById('prev').addEventListener('click', onPrevPage);
    // /**
    //  * Displays next page.
    //  */
    // function onNextPage() {
    //   if (pageNum >= pdfDoc.numPages) {
    //     return;
    //   }
    //   pageNum++;
    //   queueRenderPage(pageNum);
    // }
    // document.getElementById('next').addEventListener('click', onNextPage);
    // /**
    //  * Asynchronously downloads PDF.
    //  */
    // PDFJS.getDocument(url).then(function (pdfDoc_) {
    //   pdfDoc = pdfDoc_;
    //   document.getElementById('page_count').textContent = pdfDoc.numPages;
    //   // Initial/first page rendering
    //   renderPage(pageNum);
    // });




