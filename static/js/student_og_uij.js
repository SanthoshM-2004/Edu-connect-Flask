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




document.getElementById("ua").addEventListener("click", function(){
    document.querySelector(".popup-3").style.display = "flex";
})

document.getElementById("cross-3").addEventListener("click", function(){
    document.querySelector(".popup-3").style.display = "none";
})



document.getElementById("uq").addEventListener("click", function(){
    document.querySelector(".popup-2").style.display = "flex";
})

document.getElementById("cross-2").addEventListener("click", function(){
    document.querySelector(".popup-2").style.display = "none";
})




document.getElementById("oc").addEventListener("click", function(){
    document.querySelector(".popup-1").style.display = "flex";
})

document.getElementById("cross-1").addEventListener("click", function(){
    document.querySelector(".popup-1").style.display = "none";
})



document.querySelector(".profile-img").addEventListener("click", function(){
    document.querySelector(".popup-p").style.display = "flex";
})

document.getElementById("cross-p").addEventListener("click", function(){
    document.querySelector(".popup-p").style.display = "none";
})


