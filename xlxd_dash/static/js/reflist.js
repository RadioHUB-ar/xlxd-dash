const ref_table = document.getElementById("ref_table");

function secondsToDhms(seconds) {
  seconds = Number(seconds);
  var d = Math.floor(seconds / (3600*24));
  var h = Math.floor(seconds % (3600*24) / 3600);
  var m = Math.floor(seconds % 3600 / 60);
  var s = Math.floor(seconds % 60);
  
  var dDisplay = d > 0 ? d + "D " : "";
  return dDisplay + h.toString().padStart(2,'0') + ":" + m.toString().padStart(2,'0') + ":" + s.toString().padStart(2,'0');
}

function loadData() {
  const down_time = 1800+600;
  const now = Math.floor(Date.now() / 1000);
  const uniq = []
  rowClassName = ""
  fetch("/getreflist")
    .then(res => res.json())
    .then(data => {
      num = 1
      exec = true;
      ref_table.innerHTML = "";
      const reflectors = Object.values(data.heard_users || {});

      data['XLXAPI']['answer']['reflectorlist']['reflector'].forEach(item => {
        const row = document.createElement("tr");

        order = document.createElement("td");
        order.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        link = document.createElement("a");
        link.href = item.dashboardurl;
        if (item.lastcontact > now - down_time) {
          link.textContent = `✅ ${item.name}`;
        } else {
          link.textContent = `❌ ${item.name}`;
        }
        link.target = "_blank";
        order.appendChild(link);
        row.appendChild(order);

        order = document.createElement("td");
        order.className = "truncate-cell border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        order.textContent = item.country;
        row.appendChild(order);

        order = document.createElement("td");
        order.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        order.textContent = item.comment;
        row.appendChild(order);

        ref_table.appendChild(row);
      });
    });
}

loadData();
