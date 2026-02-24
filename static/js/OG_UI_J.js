const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
	const li = item.parentElement;

	item.addEventListener('click', function () {
		allSideMenu.forEach(i=> {
			i.parentElement.classList.remove('active');
		})
		li.classList.add('active');
	})
});




// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})



const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})

// profile popup

document.querySelector(".profile-1").addEventListener("click", function(){
    document.querySelector(".popup-p").style.display = "flex";
})

document.getElementById("cross-p").addEventListener("click", function(){
    document.querySelector(".popup-p").style.display = "none";
})

document.querySelector(".profile-2").addEventListener("click", function(){
    document.querySelector(".popup-p").style.display = "flex";
})

document.getElementById("cross-p").addEventListener("click", function(){
    document.querySelector(".popup-p").style.display = "none";
})

// grid popup

document.getElementById("uv").addEventListener("click", function(){
    document.querySelector(".popup-1").style.display = "flex";
})

document.getElementById("cross-1").addEventListener("click", function(){
    document.querySelector(".popup-1").style.display = "none";
})


document.getElementById("uq").addEventListener("click", function(){
    document.querySelector(".popup-2").style.display = "flex";
})

document.getElementById("cross-2").addEventListener("click", function(){
    document.querySelector(".popup-2").style.display = "none";
})

document.getElementById("oc").addEventListener("click", function(){
    document.querySelector(".popup-3").style.display = "flex";
})

document.getElementById("cross-3").addEventListener("click", function(){
    document.querySelector(".popup-3").style.display = "none";
})

document.getElementById("ua").addEventListener("click", function(){
    document.querySelector(".popup-4").style.display = "flex";
})

document.getElementById("cross-4").addEventListener("click", function(){
    document.querySelector(".popup-4").style.display = "none";
})

document.getElementById("noti").addEventListener("click", function(){
    document.querySelector(".popup-n").style.display = "flex";
})

document.getElementById("cross-n").addEventListener("click", function(){
    document.querySelector(".popup-n").style.display = "none";
})



// side-bar popup

document.getElementById("cj").addEventListener("click", function(){
    document.querySelector(".popup-s1").style.display = "flex";
})

document.getElementById("cross-s1").addEventListener("click", function(){
    document.querySelector(".popup-s1").style.display = "none";
})

document.getElementById("ci").addEventListener("click", function(){
    document.querySelector(".popup-s2").style.display = "flex";
})

document.getElementById("cross-s2").addEventListener("click", function(){
    document.querySelector(".popup-s2").style.display = "none";
})

document.getElementById("assign").addEventListener("click", function(){
    document.querySelector(".popup-s3").style.display = "flex";
})

document.getElementById("cross-s3").addEventListener("click", function(){
    document.querySelector(".popup-s3").style.display = "none";
})

document.getElementById("notes").addEventListener("click", function(){
    document.querySelector(".popup-s4").style.display = "flex";
})

document.getElementById("cross-s4").addEventListener("click", function(){
    document.querySelector(".popup-s4").style.display = "none";
})



function showVideo(id) {
    // Hide all videos
    document.querySelectorAll('.video-popup').forEach(el => {
      el.style.display = 'none';
      const videoTag = el.querySelector('video');
      if (videoTag) videoTag.pause(); // Pause any playing video
    });

    // Show the selected one
    const videoDiv = document.getElementById(id);
    videoDiv.style.display = 'block';
  }

  function closeVideo(id) {
    const videoDiv = document.getElementById(id);
    videoDiv.style.display = 'none';

    const videoTag = videoDiv.querySelector('video');
    if (videoTag) {
      videoTag.pause();
      videoTag.currentTime = 0;
    }
  }
