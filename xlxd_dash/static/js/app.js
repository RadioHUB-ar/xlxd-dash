const users_table = document.getElementById("users_table");
const nodes_table = document.getElementById("nodes_table");
const toggleDark = document.getElementById("toggle-dark");
const toggleRefresh = document.getElementById("toggle-refresh");
const toggleUserDetail = document.getElementById("toggle-user_detail");
const uptimeEl = document.getElementById("server_uptime");

function actualizarUptime() {
  uptime += 1;
  uptimeEl.textContent = secondsToDhms(uptime);
}
uptimeEl.textContent = secondsToDhms(uptime);
setInterval(actualizarUptime, 1000);

function loadData() {
  const uniq = []
  rowClassName = ""
  fetch("/get_data")
    .then(res => res.json())
    .then(data => {
      num = 1
      exec = true;
      users_table.innerHTML = "";
      const usuarios = Object.values(data.heard_users || {});
      // console.log(data)

      usuarios.forEach(item => {
        if (exec) {
          document.getElementById("users_div").classList.remove("hidden");
          exec = false;
        }

        uniqueness = `${item.Call}`;
        // uniqueness = `${item.Call}${item.Suffix}`;
        if ( uniq.includes(uniqueness) ) {
          if (user_data_detail) {
            rowClassName = "user_row";
          } else {
            rowClassName = "user_row hidden";
          }
        } else {
          rowClassName = "";
          uniq.push(uniqueness);
        }

        const row = document.createElement("tr");
        row.className = rowClassName;

        const order = document.createElement("td");
        order.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
        order.textContent = num++;
        row.appendChild(order);

        const pais = document.createElement("td");
        pais.title = item.Flag[1]
        pais.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell text-center";
        pais.innerHTML = item.Flag[0];
        row.appendChild(pais);

        const callsign = document.createElement("td");
        callsign.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        callsign.textContent = item.Call;
        row.appendChild(callsign);

        const suffix = document.createElement("td");
        suffix.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
        suffix.textContent = item.Suffix;
        row.appendChild(suffix);

        const dprs = document.createElement("td");
        dprs.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm text-center";
        dprs.innerHTML = `<a href="https://aprs.fi/#!call=${item.Call}*" target="_blank">🛰️</a>`;
        row.appendChild(dprs);

        const via = document.createElement("td");
        via.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        via.textContent = item.Via_node;
        row.appendChild(via);

        const time = document.createElement("td");
        time.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        time.textContent = epoch2dateTime(item.LastHeardTime);
        row.appendChild(time);

        const mod = document.createElement("td");
        mod.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        mod.textContent = item.On_module;
        row.appendChild(mod);

        users_table.appendChild(row);
      });

      num = 1
      exec = true;
      nodes_table.innerHTML = "";
      const nodes = Object.values(data.linked_nodes || {});

      nodes.forEach(item => {
        if (exec) {
          document.getElementById("nodes_div").classList.remove("hidden");
          exec = false;
        }

        const row = document.createElement("tr");

        const order = document.createElement("td");
        order.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
        order.textContent = num++;
        row.appendChild(order);

        const pais = document.createElement("td");
        pais.title = item.Flag[1]
        pais.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell text-center";
        pais.innerHTML = item.Flag[0]
        row.appendChild(pais);

        const callsign = document.createElement("td");
        callsign.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        callsign.textContent = item.Callsign;
        row.appendChild(callsign);

        const time = document.createElement("td");
        time.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        time.textContent = epoch2dateTime(item.LastHeardTime);
        row.appendChild(time);

        const connect = document.createElement("td");
        connect.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        connect.textContent = epoch2dateTime(item.ConnectTime);
        row.appendChild(connect);

        const proto = document.createElement("td");
        proto.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        proto.textContent = item.Protocol;
        row.appendChild(proto);

        const linked = document.createElement("td");
        linked.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        linked.textContent = item.LinkedModule;
        row.appendChild(linked);

        nodes_table.appendChild(row);
      });

    });
}

// toggle dark mode
function updateDarkMode() {
  const isDark = document.documentElement.classList.contains("dark");
  toggleDark.textContent = isDark ? "🌙" : "🔆";
}

toggleDark.addEventListener("click", () => {
  document.documentElement.classList.toggle("dark");
  updateDarkMode();
});

// toggle auto refresh
let autoRefresh = false;
let intervalId = null;
toggleRefresh.addEventListener("click", () => {
  autoRefresh = !autoRefresh;

  if (autoRefresh) {
    toggleRefresh.textContent = "🔁";
    loadData();
    intervalId = setInterval(loadData, 5000);
  } else {
    toggleRefresh.textContent = "⏸️";
    clearInterval(intervalId);
  }
});

// toogle hide user activity detail
let user_data_detail = false;
toggleUserDetail.addEventListener("click", () => {
  user_data_detail = !user_data_detail;

  if (user_data_detail) {
    toggleUserDetail.textContent = "👁️";
    document.querySelectorAll('.user_row').forEach(el => {
      el.classList.remove('hidden');
    });
  } else {
    toggleUserDetail.textContent = "🙈";
    document.querySelectorAll('.user_row').forEach(el => {
      el.classList.add('hidden');
    });
  }
});


// function capitalize(s)
// {
//     return s && s[0].toUpperCase() + s.slice(1).toLowerCase();
// }

function secondsToDhms(seconds) {
  seconds = Number(seconds);
  var d = Math.floor(seconds / (3600*24));
  var h = Math.floor(seconds % (3600*24) / 3600);
  var m = Math.floor(seconds % 3600 / 60);
  var s = Math.floor(seconds % 60);
  
  var dDisplay = d > 0 ? d + "D " : "";
  return dDisplay + h.toString().padStart(2,'0') + ":" + m.toString().padStart(2,'0') + ":" + s.toString().padStart(2,'0');
}

// function epoch2diff(epoch) {
//   diff = Math.floor(Date.now()/1000) - epoch
//   return secondsToDhms(diff) //date.getDate().toString().padStart(2,'0') + '/' + (date.getMonth()+1).toString().padStart(2,'0') + '/' + (date.getYear()-100) + ' ' + date.getHours().toString().padStart(2,'0') +':'+date.getMinutes().toString().padStart(2,'0')
// }

function epoch2dateTime(epoch) {
  date = new Date(epoch*1000)
  return date.getDate().toString().padStart(2,'0') + '/' + (date.getMonth()+1).toString().padStart(2,'0') + '/' + (date.getYear()-100) + ' ' + date.getHours().toString().padStart(2,'0') +':'+date.getMinutes().toString().padStart(2,'0')
}

updateDarkMode();
loadData();
