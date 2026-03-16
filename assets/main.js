/**
 * assets/main.js — Yến Vân Guide
 * Shared helpers: render, modal (TikTok embed), utilities
 * KHÔNG fetch data tự động — mỗi trang tự fetch rồi gọi helpers.
 */

/* ── Thumbnail gradient cycle ── */
const THUMB_CLASSES = ['t0', 't1', 't2', 't3', 't4'];

/* ── Category → badge class + icon ── */
const BADGE_MAP = {
  'Hướng dẫn': { cls: 'badge-guide',   icon: '⚔️' },
  'Nhân vật':  { cls: 'badge-char',    icon: '👤' },
  'Meta':      { cls: 'badge-meta',    icon: '🏆' },
  'Podcast':   { cls: 'badge-podcast', icon: '🎙️' },
  'Event':     { cls: 'badge-guide',   icon: '🎪' },
};

function getCategoryBadge(category) {
  return BADGE_MAP[category] || { cls: 'badge-guide', icon: '📄' };
}

/* ── Date format: "2026-02-20" → "20/02/2026" ── */
function formatDate(isoDate) {
  if (!isoDate) return '';
  const [y, m, d] = isoDate.split('-');
  return `${d}/${m}/${y}`;
}

/* ── Number format: "1853" → "1.853" ── */
function formatViews(n) {
  return Number(n).toLocaleString('vi-VN');
}

/* ════════════════════════
   RENDER HELPERS
════════════════════════ */

/**
 * Render 1 video card (9:16 portrait)
 * @param {Object} v  - video object từ videos.json
 * @param {number} idx - index để xác định màu thumbnail fallback
 */
function renderVideoCard(v, idx = 0) {
  const tClass = THUMB_CLASSES[idx % 5];
  // Strip bracket prefix for tag pill
  const tag = v.tags[0] || '';
  
  // Hiển thị ảnh bìa từ TikTok nếu có, nếu không thì dùng gradient fallback
  const thumbHtml = v.thumbnail 
    ? `<img class="vid-thumb-img" src="${v.thumbnail}" alt="Thumbnail" loading="lazy" />`
    : `<div class="vid-thumb-bg ${tClass}" style="width:100%;height:100%"></div>`;

  return `<div class="vid-card" onclick="openModal('${v.id}','${escHtml(v.title)}','${escHtml(v.tags.join(','))}')">
    <div class="vid-thumb">
      ${thumbHtml}
      <div class="vid-tag-pill">${escHtml(tag)}</div>
      <div class="vid-play">▶</div>
    </div>
    <div class="vid-title">${escHtml(v.title)}</div>
    <div class="vid-date">${formatDate(v.date)}</div>
  </div>`;
}

/**
 * Render 1 article list-item (trang articles.html)
 * @param {Object} a - article object từ articles.json
 */
function renderArtListItem(a) {
  const badge = getCategoryBadge(a.category);
  return `<div class="art-list-item" onclick="location.href='article.html?id=${a.id}'">
    <div>
      <div class="art-list-cat"><span class="art-cat-badge ${badge.cls}">${badge.icon} ${escHtml(a.category)}</span></div>
      <div class="art-list-title">${escHtml(a.title)}</div>
      <div class="art-list-desc">${escHtml(a.description)}</div>
      <div class="art-list-meta">
        <span>${formatDate(a.date)}</span>
        <span>·</span>
        <span>${escHtml(a.readtime)} đọc</span>
        <span>·</span>
        <span>${formatViews(a.views)} lượt xem</span>
      </div>
    </div>
    <div class="art-list-thumb">${a.icon}</div>
  </div>`;
}

/**
 * Render 1 link card (trang links.html)
 * @param {Object} l - link object từ links.json
 */
function renderLinkCard(l) {
  return `<a class="link-card" href="${escHtml(l.url)}" target="_blank" rel="noopener">
    <div class="link-card-icon" style="background:${escHtml(l.bg)}; color:${escHtml(l.color)}">${l.icon}</div>
    <div class="link-card-text">
      <div class="link-card-name">${escHtml(l.name)}</div>
      <div class="link-card-desc">${escHtml(l.description)}</div>
    </div>
    <div class="link-card-arrow">→</div>
  </a>`;
}

/* ── Escape HTML ── */
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ════════════════════════
   TIKTOK MODAL
════════════════════════ */

let _modalCurrentId = null;

function openModal(videoId, title, tagsStr) {
  const modal = document.getElementById('modal');
  if (!modal) return;

  // Tránh reload nếu đang xem cùng video
  if (_modalCurrentId === videoId) {
    modal.classList.add('open');
    return;
  }
  _modalCurrentId = videoId;

  // Set title
  const titleEl = document.getElementById('modal-title');
  if (titleEl) titleEl.textContent = title;

  // Set tags
  const tagsEl = document.getElementById('modal-tags');
  if (tagsEl) {
    tagsEl.innerHTML = tagsStr.split(',')
      .filter(Boolean)
      .map(t => `<span class="modal-tag-pill">${escHtml(t.trim())}</span>`)
      .join('');
  }

  // Inject iframe sử dụng Native TikTok Player API (v1) với autoplay
  // Đây là cách tích hợp nhẹ nhất, focus hoàn toàn vào player và ít bị lỗi CORS/Autoplay nhất
  const bodyEl = document.getElementById('modal-body');
  if (bodyEl) {
    bodyEl.innerHTML = `<iframe
      src="https://www.tiktok.com/player/v1/${videoId}?&autoplay=1&loop=1&muted=0&volume=0.5"
      style="width: 100%; height: 100%; border: none; background: #000;"
      allowfullscreen
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      sandbox="allow-popups allow-popups-to-escape-sandbox allow-scripts allow-top-navigation allow-same-origin">
    </iframe>`;
  }


  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}


function closeModalDirect() {
  const modal = document.getElementById('modal');
  if (!modal) return;
  modal.classList.remove('open');
  document.body.style.overflow = '';
  // Reset để lần sau load lại embed
  _modalCurrentId = null;
  const bodyEl = document.getElementById('modal-body');
  if (bodyEl) bodyEl.innerHTML = '';
}

function handleModalOverlayClick(e) {
  if (e.target === document.getElementById('modal')) {
    closeModalDirect();
  }
}

/* ── Bind ESC key để đóng modal ── */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModalDirect();
});

/* ════════════════════════
   SHARED COMPONENTS
════════════════════════ */

/** Inject nav vào trang (dùng khi trang không include nav inline) */
function buildNav(activePage) {
  const pages = [
    { id: 'home',     href: 'index.html',    label: 'Trang chủ' },
    { id: 'articles', href: 'articles.html', label: 'Bài viết' },
    { id: 'videos',   href: 'videos.html',   label: 'Video' },
    { id: 'links',    href: 'links.html',    label: 'Liên kết' },
  ];
  return `<nav>
    <a class="nav-logo" href="index.html">
      <div class="nav-logo-icon">⚔</div>
      <div class="nav-logo-text">Yến Vân <span>Guide</span></div>
    </a>
    <div class="nav-links">
      ${pages.map(p => `<a class="nav-btn ${p.id === activePage ? 'active' : ''}" href="${p.href}">${p.label}</a>`).join('')}
      <a class="nav-btn nav-discord" href="links.html">💬 Discord</a>
    </div>
  </nav>`;
}

/** Inject modal HTML vào trang */
function buildModal() {
  return `<div class="modal-overlay" id="modal" onclick="handleModalOverlayClick(event)">
    <div class="modal-box">
      <div class="modal-head">
        <span class="modal-head-title" id="modal-title">Video</span>
        <button class="modal-close" onclick="closeModalDirect()">✕</button>
      </div>
      <div class="modal-body-embed" id="modal-body"></div>
      <div class="modal-footer" id="modal-tags"></div>
    </div>
  </div>`;
}

/** Inject footer HTML */
function buildFooter() {
  return `<footer>
    <span>© 2026 Yến Vân Guide · </span>
    <a href="https://tiktok.com/@tiu.hng.tuyn" target="_blank" rel="noopener">@tiu.hng.tuyn</a>
    <span> · Where Winds Meet Fan Site</span>
  </footer>`;
}

/* ════════════════════════
   FILTER HELPERS
════════════════════════ */

/**
 * Tạo filter bar HTML
 * @param {string[]} options - danh sách filter options
 * @param {string}   containerId - id của container để gán onclick
 * @param {Function} onFilter - callback(selectedOption)
 */
function buildFilterBar(options, containerId, onFilter) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = options.map((opt, i) =>
    `<button class="f-btn ${i === 0 ? 'active' : ''}"
      onclick="handleFilter(this,'${containerId}','${escHtml(opt)}')">${escHtml(opt)}</button>`
  ).join('');
  // Store callback
  container._onFilter = onFilter;
}

function handleFilter(btn, containerId, value) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.querySelectorAll('.f-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  if (container._onFilter) container._onFilter(value);
}
