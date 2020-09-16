var homeApp = {};
(function(){
var homeContainer = document.getElementById("home_container");

    var logtout =  function(){
        firebase.auth().signOut().then(function(){
            console.log('success');
            window.location.replace("/");
        },
        function(){})
    }

var init = function()
{
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) 
        {
          // User is signed in.
          console.log("stay");
          homeContainer.style.display = "";
        } 
        else 
        {
          // No user is signed in.
          homeContainer.style.display = "none";
          console.log("redirect");
          window.location.replace("home");
        }
      });
}
    
init();

homeApp.logout = logtout; 
})();