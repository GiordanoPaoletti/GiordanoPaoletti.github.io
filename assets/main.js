// Populate dynamic bits: year + publications from data/publications.json

document.getElementById("year").textContent = new Date().getFullYear();

function el(tag, className, html) {
  const e = document.createElement(tag);
  if (className) e.className = className;
  if (html != null) e.innerHTML = html;
  return e;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

async function loadPublications() {
  const list = document.getElementById("pub-list");
  try {
    const res = await fetch("data/publications.json", { cache: "no-store" });
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();

    // Updated label
    const upd = document.getElementById("pub-updated");
    if (data.last_updated) upd.textContent = "Updated " + data.last_updated;

    // Profile link
    const link = document.getElementById("pub-profile-link");
    const scholarLink = document.getElementById("scholar-link");
    if (data.scholar_profile) {
      link.href = data.scholar_profile;
      if (scholarLink) scholarLink.href = data.scholar_profile;
    } else {
      link.style.display = "none";
    }

    const pubs = (data.publications || []).slice().sort((a, b) => (b.year || 0) - (a.year || 0));
    list.innerHTML = "";
    if (!pubs.length) {
      list.appendChild(el("li", "pub-loading", "No publications yet."));
      return;
    }
    for (const p of pubs) {
      const title = p.url
        ? `<a href="${escapeHtml(p.url)}" target="_blank" rel="noopener">${escapeHtml(p.title)}</a>`
        : escapeHtml(p.title);
      const meta = [p.venue].filter(Boolean).map(escapeHtml).join(" · ");
      const yearTag = p.year ? `<span class="pub-year">${escapeHtml(p.year)}</span>` : "";
      const li = el("li");
      li.innerHTML =
        `<span class="pub-title">${title}</span>${yearTag}` +
        (meta ? `<br><span class="pub-meta">${meta}</span>` : "");
      list.appendChild(li);
    }
  } catch (err) {
    list.innerHTML = "";
    list.appendChild(el("li", "pub-loading", "Could not load publications."));
    console.error("publications load failed:", err);
  }
}

loadPublications();
