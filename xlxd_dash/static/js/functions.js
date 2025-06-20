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
  const date = new Date(epoch * 1000);
  let get = {}
  if (dateOnUTC == true) {
    get = {
      day: date.getUTCDate(),
      month: date.getUTCMonth() + 1,
      year: date.getUTCFullYear() - 2000,
      hour: date.getUTCHours(),
      minute: date.getUTCMinutes()
    }
  } else {
    get = {
      day: date.getDate(),
      month: date.getMonth() + 1,
      year: date.getFullYear() - 2000,
      hour: date.getHours(),
      minute: date.getMinutes()
    }
  };

  return get.day.toString().padStart(2, '0') + '/' +
         get.month.toString().padStart(2, '0') + '/' +
         get.year + ' ' +
         get.hour.toString().padStart(2, '0') + ':' +
         get.minute.toString().padStart(2, '0');
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById('popupmenu').classList.remove('hidden');
});

// toggle dark mode
document.addEventListener("DOMContentLoaded", () => {
  const toggleDark = document.getElementById("toggle-dark");

  function updateDarkMode() {
    const isDark = document.documentElement.classList.contains("dark");
    if (isDark) {
      toggleDark.textContent = "🌙";
      setLocal('darkmode', true);
    } else {
      toggleDark.textContent = "🔆";
      setLocal('darkmode', false);
    }
  }

  toggleDark.addEventListener("click", () => {
    document.documentElement.classList.toggle("dark");
    updateDarkMode();
  });

  darknow = getLocal('darkmode');
  if (darknow === false) {
    document.documentElement.classList.remove("dark");
  }

  updateDarkMode();
});

function setLocal(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function getLocal(key) {
  try {
      const value = localStorage.getItem(key);
      return value !== null ? JSON.parse(value) : null;
  } catch (e) {
      return null;
  }
}

const whatsnewKey = 'localwhatsnewDismissed';
function closewhatsnew() {
    localStorage.setItem(whatsnewKey, 'true');
    const whatsnew = document.getElementById('whatsnew');
    whatsnew.classList.add('opacity-0');
    setTimeout(() => whatsnew.classList.add('hidden'), 500);
}

window.addEventListener('DOMContentLoaded', () => {
  if (!localStorage.getItem(whatsnewKey)) {
    const whatsnew = document.getElementById('whatsnew');
    whatsnew.classList.remove('hidden');
    setTimeout(() => whatsnew.classList.add('opacity-100'), 50);
  }
});