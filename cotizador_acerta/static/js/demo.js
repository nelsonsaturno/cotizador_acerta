 $(function () {

    /* 
        ==========================================================================
            CODE FOR DEMO PAGE (IGNORE)
        ========================================================================== 
    */

     var isTouch = "ontouchstart" in document.documentElement,
         evt = isTouch ? 'touchend' : 'click';

     $("#open-demo").one(evt, function (e) {
         e.preventDefault();
         sideMenu.open();
     });
 });