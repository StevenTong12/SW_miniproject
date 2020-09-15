function SHOWmenuNAVBar()
{
document.getElementById('menuNAVBar').style.display = "block";//show contents of div
document.getElementById('menuBar').innerHTML = "<a onclick='HIDEmenuNAVBar()' href='javascript:void(0)'><img style='width:50px;float:right' src='hamburger.png'></a>";
}

function HIDEmenuNAVBar()
{
document.getElementById('menuNAVBar').style.display = "none";//hide contents of div
document.getElementById('menuBar').innerHTML = "<a onclick='SHOWmenuNAVBar()' href='javascript:void(0)'><img style='width:50px;float:right' src='hamburger.png'></a>";
}