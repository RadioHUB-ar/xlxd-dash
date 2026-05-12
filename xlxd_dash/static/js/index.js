const users_table = document.getElementById("users_table");
const nodes_table = document.getElementById("nodes_table");
const peers_table = document.getElementById("peers_table");
const toggleRefresh = document.getElementById("toggle-refresh");
const toggleUserDetail = document.getElementById("toggle-user_detail");
const uptimeEl = document.getElementById("server_uptime");
const toggleUTC = document.getElementById("toggle-utc");
const dataStatus = document.getElementById("data_status");
const dataStatusMessage = document.getElementById("data_status_message");

function actualizarUptime() {
  uptime += 1;
  uptimeEl.textContent = secondsToDhms(uptime);
}
uptimeEl.textContent = secondsToDhms(uptime);
setInterval(actualizarUptime, 1000);

function loadData() {
  const uniq = [];
  fetch("/get_data")
    .then(res => res.json())
    .then(data => {
      users_table.innerHTML = "";
      nodes_table.innerHTML = "";
      peers_table.innerHTML = "";
      document.getElementById("users_div").classList.add("hidden");
      document.getElementById("nodes_div").classList.add("hidden");
      document.getElementById("peers_div").classList.add("hidden");
      document.getElementById("nodesIP").classList.remove("md:table-cell");
      document.getElementById("peersIP").classList.remove("md:table-cell");

      if (!data.available) {
        dataStatus.classList.remove("hidden");
        dataStatusMessage.textContent = data.message || "No XLXD data available.";
        return;
      }

      dataStatus.classList.add("hidden");

      let num = 1;
      let exec = true;
      const usuarios = Object.values(data.heard_users || {});
      // console.log(data)

      usuarios.forEach(item => {
        if (exec) {
          document.getElementById("users_div").classList.remove("hidden");
          exec = false;
        }

        const uniqueness = `${item.Call}`;
        // uniqueness = `${item.Call}${item.Suffix}`;
        let rowClassName = "";
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
        const link = document.createElement("a");
        link.href = `https://www.qrz.com/db/${item.CallLink}`;
        link.textContent = item.Call;
        link.target = "_blank";
        callsign.appendChild(link);
        row.appendChild(callsign);

        const suffix = document.createElement("td");
        suffix.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
        suffix.textContent = item.Suffix;
        row.appendChild(suffix);

        const dprs = document.createElement("td");
        dprs.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm text-center";
        const dprslink = document.createElement("a");
        dprslink.href = `https://aprs.fi/#!call=${item.CallLink}*`;
        dprslink.textContent = "🛰️";
        dprslink.target = "_blank";
        dprs.appendChild(dprslink);
        row.appendChild(dprs);

        const via = document.createElement("td");
        via.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        const vialink = document.createElement("a");
        vialink.href = `https://aprs.fi/#!call=${item.Via_node}`;
        vialink.textContent = item.Via_node;
        vialink.target = "_blank";
        via.appendChild(vialink);
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

      num = 1;
      exec = true;
      let showIP = false;
      const nodes = Object.values(data.linked_nodes || {});

      nodes.forEach(item => {
        if (exec) {
          document.getElementById("nodes_div").classList.remove("hidden");
          exec = false;
          if (item.IP) {
            showIP = true;
            document.getElementById("nodesIP").classList.add("md:table-cell");
          }
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
        const dprslink = document.createElement("a");
        dprslink.href = `https://aprs.fi/#!call=${item.Callsign}`;
        dprslink.textContent = item.Callsign;
        dprslink.target = "_blank";
        callsign.appendChild(dprslink);
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

        if (showIP) {
          const ip = document.createElement("td");
          ip.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
          ip.textContent = item.IP;
          row.appendChild(ip);
        }

        nodes_table.appendChild(row);
      });


      num = 1;
      exec = true;
      showIP = false;
      const peers = Object.values(data.linked_peers || {});

      peers.forEach(item => {
        if (exec) {
          document.getElementById("peers_div").classList.remove("hidden");
          exec = false;
          if (item.IP) {
            showIP = true;
            document.getElementById("peersIP").classList.add("md:table-cell");
          }
        }

        const row = document.createElement("tr");

        const order = document.createElement("td");
        order.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
        order.textContent = num++;
        row.appendChild(order);

        const callsign = document.createElement("td");
        callsign.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
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
        linked.textContent = item.LinkedModule.split("").join(" ");
        row.appendChild(linked);

        if (showIP) {
          const ip = document.createElement("td");
          ip.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm hidden md:table-cell";
          ip.textContent = item.IP;
          row.appendChild(ip);
        }

        peers_table.appendChild(row);
      });

    });
}

// toggle auto refresh
toggleRefresh.classList.remove('hidden');
let autoRefresh = false;
let intervalId = null;
toggleRefresh.addEventListener("click", () => {
  autoRefresh = !autoRefresh;
  if (autoRefresh) {
    toggleRefresh.textContent = "▶️";
    loadData();
    intervalId = setInterval(loadData, 5000);
  } else {
    toggleRefresh.textContent = "⏸️";
    clearInterval(intervalId);
  }
});

// dates on local / utc
toggleUTC.classList.remove('hidden');
let dateOnUTC = getLocal('dateOnUTC');
if (dateOnUTC === null) {
  dateOnUTC = true;
}
function toogleTimeIcon() {
  if (dateOnUTC) {
    toggleUTC.textContent = "🌍";
    loadData();
  } else {
    toggleUTC.textContent = "🏠";
    loadData();
  }
}
toggleUTC.addEventListener("click", () => {
  dateOnUTC = !dateOnUTC;
  toogleTimeIcon();
  setLocal("dateOnUTC", dateOnUTC);
});
toogleTimeIcon();

// toogle hide user activity detail
toggleUserDetail.classList.remove('hidden');
let user_data_detail = getLocal("user_data_detail")
if (user_data_detail === null) {
  user_data_detail = false;
}
if (user_data_detail === true) {
  toggleUserDetail.textContent = "👁️";
} else {
  toggleUserDetail.textContent = "🙈";
}
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
  setLocal("user_data_detail", user_data_detail);
});

loadData();
