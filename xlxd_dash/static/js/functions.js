function secondsToDhms(seconds) {
    seconds = Number(seconds);
    var d = Math.floor(seconds / (3600*24));
    var h = Math.floor(seconds % (3600*24) / 3600);
    var m = Math.floor(seconds % 3600 / 60);
    var s = Math.floor(seconds % 60);
    
    var dDisplay = d > 0 ? d + "D " : "";
    return dDisplay + h.toString().padStart(2,'0') + ":" + m.toString().padStart(2,'0') + ":" + s.toString().padStart(2,'0');
  }

  function epoch2dateTime(epoch) {
    date = new Date(epoch*1000)
    return date.getDate().toString().padStart(2,'0') + '/' + (date.getMonth()+1).toString().padStart(2,'0') + '/' + (date.getYear()-100) + ' ' + date.getHours().toString().padStart(2,'0') +':'+date.getMinutes().toString().padStart(2,'0')
  }

// toggle dark mode
document.addEventListener("DOMContentLoaded", () => {
  const toggleDark = document.getElementById("toggle-dark");

  function updateDarkMode() {
    const isDark = document.documentElement.classList.contains("dark");
    toggleDark.textContent = isDark ? "🌙" : "🔆";
  }

  toggleDark.addEventListener("click", () => {
    document.documentElement.classList.toggle("dark");
    updateDarkMode();
  });

  updateDarkMode();
});

function toggleDropdown() {
  document.getElementById("dropdown").classList.toggle("hidden");
}