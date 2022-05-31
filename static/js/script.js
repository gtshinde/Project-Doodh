function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

function toggleUserDetails() {
  // console.log("Inside the toggleUserDetails() ");
  // console.log(document.getElementById("userDetails").style.display);

  // in the beginning "userDetails" has style display as an empty string ("")
  // so we have added one more or conditio to check if it is an empty string
  if (document.getElementById("userDetails").style.display == "none" || document.getElementById("userDetails").style.display == ""){
    document.getElementById("userDetails").style.display = "block";
  }
  else if (document.getElementById("userDetails").style.display == "block"){
    document.getElementById("userDetails").style.display = "none";
  }
}