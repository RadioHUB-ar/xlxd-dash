const ref_table = document.getElementById("ref_table");
const ref_status = document.getElementById("ref_status");
const ref_status_message = document.getElementById("ref_status_message");
const ref_filter = document.getElementById("ref_filter");
const no_filter_results = document.createElement("tr");

no_filter_results.className = "hidden";
no_filter_results.innerHTML = `
  <td colspan="100%" class="text-center px-2 py-2 text-xs sm:text-sm text-gray-500">
    No matching reflectors
  </td>
`;

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
  fetch("/getreflist")
    .then(res => res.json())
    .then(data => {
      ref_table.innerHTML = "";
      const reflectors = Array.isArray(data.reflectors) ? data.reflectors : [];

      if (data.available === false || reflectors.length === 0) {
        ref_status.classList.remove("hidden");
        ref_status_message.textContent = data.message || "No reflector data available.";
        ref_table.innerHTML = `
          <tr>
            <td colspan="100%" class="text-center px-2 py-2 text-xs sm:text-sm text-gray-500">
              No reflector data available
            </td>
          </tr>
        `;
        return;
      }

      ref_status.classList.add("hidden");
      reflectors.forEach(item => {
        const row = document.createElement("tr");
        row.dataset.search = [
          item.name,
          item.country,
          item.comment,
          item.dashboardurl,
          item.online ? "online" : "offline"
        ].join(" ").toLowerCase();

        let order = document.createElement("td");
        order.className = "border border-gray-300 dark:border-gray-700 px-2 py-1 text-xs sm:text-sm";
        const link = document.createElement("a");
        link.href = item.dashboardurl;
        if (item.online) {
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
      ref_table.appendChild(no_filter_results);
      filterReflectors();
    })
    .catch(error => {
      ref_status.classList.remove("hidden");
      ref_status_message.textContent = "Could not load reflector list.";
      ref_table.innerHTML = `
        <tr>
          <td colspan="100%" class="text-center px-2 py-2 text-xs sm:text-sm text-gray-500">
            Could not load reflector list
          </td>
        </tr>
      `;
      console.error(error);
    });
}

function filterReflectors() {
  const filter = ref_filter.value.trim().toLowerCase();
  let visibleRows = 0;

  ref_table.querySelectorAll("tr[data-search]").forEach(row => {
    const matches = row.dataset.search.includes(filter);
    row.classList.toggle("hidden", !matches);
    if (matches) {
      visibleRows += 1;
    }
  });

  no_filter_results.classList.toggle("hidden", !filter || visibleRows > 0);
}

ref_filter.addEventListener("input", filterReflectors);

loadData();
