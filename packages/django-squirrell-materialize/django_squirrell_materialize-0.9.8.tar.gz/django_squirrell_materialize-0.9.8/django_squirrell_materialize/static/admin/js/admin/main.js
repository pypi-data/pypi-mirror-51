
// Abre el sidenav

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {
        edge: 'right',
        draggable: true,
        inDuration: 450,
        outDuration: 200,
        onOpenStart: null,
        onOpenEnd: null,
        onCloseStart: null,
        onCloseEnd: null,
        preventScrolling: true
    });
    
  });
  
document.addEventListener('DOMContentLoaded', function() {

    var elem = document.querySelector('.tabs')

    var instance = M.Tabs.init(elem, {
        duration: 300,
        onShow: null,
        swipeable: false,
        responsiveThreshold: Infinity,
    });
    console.log("Hola")
});

/*
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems, {
        classes: 'hola'
    });
});
*/
