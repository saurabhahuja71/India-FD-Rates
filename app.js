const categories = [
  ["private", "Private sector banks", "Commercial private banks with retail FD products."],
  ["public", "Public sector banks", "Government-owned banks and their retail term deposits."],
  ["small-finance", "Small finance banks", "RBI-licensed small finance banks; not mixed with other categories."]
];

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
const rate = (v) => v == null ? "—" : `${Number(v).toFixed(2)}%`;
function table(key, title, description, rows) {
  const items = rows.filter(r => r.category === key).sort((a,b) => b.regular.rate - a.regular.rate).slice(0, 5);
  return `<section class="category"><div class="section-heading"><div><p class="eyebrow">TOP 5</p><h2>${title}</h2><p>${description}</p></div><span class="count">${items.length} banks</span></div>
  <div class="table-scroll"><table><thead><tr><th>Rank</th><th>Bank name</th><th>Regular citizens<br><small>highest rate</small></th><th>Senior citizens<br><small>highest rate</small></th><th>Tenure</th><th>Last updated</th><th>Source</th></tr></thead><tbody>
  ${items.map((r,i) => `<tr><td class="rank">${i+1}</td><td><strong>${esc(r.bank)}</strong><small class="note">${esc(r.notes || "")}</small></td><td><span class="rate">${rate(r.regular.rate)}</span><small>${esc(r.regular.tenure)}</small></td><td><span class="rate senior">${rate(r.senior.rate)}</span><small>${esc(r.senior.tenure)}</small></td><td>${esc(r.regular.tenure === r.senior.tenure ? r.regular.tenure : `Regular: ${r.regular.tenure}<br>Senior: ${r.senior.tenure}`)}</td><td>${esc(r.last_updated)}</td><td><a class="source" href="${esc(r.source)}" target="_blank" rel="noopener">Official page ↗</a></td></tr>`).join("")}</tbody></table></div></section>`;
}
fetch("data/fd-rates.json").then(r => r.json()).then(data => {
  document.querySelector("#updated").textContent = `Last checked ${data.generated_at} · ${data.rows.length} banks tracked`;
  document.querySelector("#app").innerHTML += categories.map(c => table(...c, data.rows)).join("");
}).catch(() => { document.querySelector("#app").innerHTML += '<p class="error">The latest rate snapshot could not be loaded.</p>'; });
