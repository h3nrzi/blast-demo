/* ==========================================================================
   AI NEWS RADAR - DASHBOARD FRONTEND LOGIC
   Handles API fetching, Category Filtering, Search, Sorting & Bookmarks
   ========================================================================== */

let state = {
  articles: [],
  categories: [],
  activeCategory: 'All',
  searchQuery: '',
  sortBy: 'newest',
  lastUpdated: null
};

// DOM Element References
const articlesGrid = document.getElementById('articles-grid');
const categoryPillsContainer = document.getElementById('category-pills');
const searchInput = document.getElementById('search-input');
const clearSearchBtn = document.getElementById('clear-search');
const sortSelect = document.getElementById('sort-select');
const visibleCountElem = document.getElementById('visible-count');
const totalCountElem = document.getElementById('total-count');
const lastUpdatedText = document.getElementById('last-updated-text');
const refreshBtn = document.getElementById('refresh-btn');
const emptyState = document.getElementById('empty-state');
const resetFiltersBtn = document.getElementById('reset-filters-btn');
const toastContainer = document.getElementById('toast-container');

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  loadData();
});

function setupEventListeners() {
  // Search Input
  searchInput.addEventListener('input', (e) => {
    state.searchQuery = e.target.value.trim().toLowerCase();
    clearSearchBtn.style.display = state.searchQuery ? 'block' : 'none';
    render();
  });

  clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    state.searchQuery = '';
    clearSearchBtn.style.display = 'none';
    render();
  });

  // Sort Selector
  sortSelect.addEventListener('change', (e) => {
    state.sortBy = e.target.value;
    render();
  });

  // Refresh Button
  refreshBtn.addEventListener('click', () => {
    triggerFeedRefresh();
  });

  // Reset Filters Button
  resetFiltersBtn.addEventListener('click', () => {
    state.activeCategory = 'All';
    state.searchQuery = '';
    searchInput.value = '';
    clearSearchBtn.style.display = 'none';
    render();
  });
}

// Fetch Payload from API Endpoint
async function loadData() {
  try {
    const res = await fetch('/api/articles');
    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
    const data = await res.json();
    
    state.articles = data.articles || [];
    state.categories = ['All', ...(data.metadata?.categories || []), '♥ Bookmarked'];
    state.lastUpdated = data.metadata?.last_updated;

    updateHeaderTime();
    renderCategoryPills();
    render();
  } catch (err) {
    console.error('Failed loading articles:', err);
    showToast('Failed to load news payload', 'error');
  }
}

// Trigger Backend Feed Refresh
async function triggerFeedRefresh() {
  refreshBtn.classList.add('spinning');
  showToast('Refreshing AI RSS feeds...', 'info');

  try {
    const res = await POST('/api/refresh');
    if (res.success) {
      showToast(`Refreshed! Ingested ${res.total_count} articles`, 'success');
      await loadData();
    } else {
      showToast('Feed refresh completed with warnings', 'warning');
    }
  } catch (err) {
    console.error('Refresh error:', err);
    showToast('Network error while refreshing feeds', 'error');
  } finally {
    refreshBtn.classList.remove('spinning');
  }
}

// Render Category Filter Pills
function renderCategoryPills() {
  categoryPillsContainer.innerHTML = '';

  state.categories.forEach(cat => {
    const pill = document.createElement('button');
    pill.className = `pill-btn ${state.activeCategory === cat ? 'active' : ''}`;
    
    const count = calculateCategoryCount(cat);
    pill.innerHTML = `<span>${cat}</span><span class="count-badge">${count}</span>`;
    
    pill.addEventListener('click', () => {
      state.activeCategory = cat;
      renderCategoryPills();
      render();
    });

    categoryPillsContainer.appendChild(pill);
  });
}

function calculateCategoryCount(category) {
  if (category === 'All') return state.articles.length;
  if (category === '♥ Bookmarked') return state.articles.filter(a => a.is_bookmarked).length;
  return state.articles.filter(a => a.category === category).length;
}

// Filter, Sort, and Render Articles Grid
function render() {
  let filtered = state.articles.filter(item => {
    // Category Filter
    if (state.activeCategory === '♥ Bookmarked' && !item.is_bookmarked) return false;
    if (state.activeCategory !== 'All' && state.activeCategory !== '♥ Bookmarked' && item.category !== state.activeCategory) return false;

    // Search Query Filter
    if (state.searchQuery) {
      const matchTitle = item.title.toLowerCase().includes(state.searchQuery);
      const matchSummary = item.summary.toLowerCase().includes(state.searchQuery);
      const matchSource = item.source.toLowerCase().includes(state.searchQuery);
      if (!matchTitle && !matchSummary && !matchSource) return false;
    }

    return true;
  });

  // Sorting
  filtered.sort((a, b) => {
    if (state.sortBy === 'newest') {
      return new Date(b.published_at) - new Date(a.published_at);
    } else if (state.sortBy === 'source') {
      return a.source.localeCompare(b.source);
    } else if (state.sortBy === 'title') {
      return a.title.localeCompare(b.title);
    }
    return 0;
  });

  // Update Counters
  visibleCountElem.textContent = filtered.length;
  totalCountElem.textContent = state.articles.length;

  // Render Grid or Empty State
  if (filtered.length === 0) {
    articlesGrid.style.display = 'none';
    emptyState.style.display = 'block';
  } else {
    articlesGrid.style.display = 'grid';
    emptyState.style.display = 'none';
    articlesGrid.innerHTML = filtered.map(item => createArticleCardHTML(item)).join('');
    attachBookmarkListeners();
  }
}

// Generate HTML for Single Article Card
function createArticleCardHTML(item) {
  const sourceClass = item.source.toLowerCase().replace(/\s+/g, '-');
  const formattedDate = formatRelativeTime(item.published_at);
  
  return `
    <article class="article-card" data-id="${item.id}">
      <div class="card-top">
        <span class="source-badge ${sourceClass}">${item.source}</span>
        <span class="category-tag">${item.category}</span>
      </div>
      
      <h2 class="card-title">
        <a href="${item.url}" target="_blank" rel="noopener noreferrer">${escapeHTML(item.title)}</a>
      </h2>
      
      <p class="card-summary">${escapeHTML(item.summary)}</p>
      
      <div class="card-footer">
        <div class="footer-meta">
          <span>${formattedDate}</span>
          <span>•</span>
          <span>${item.read_time}</span>
        </div>
        
        <button class="bookmark-btn ${item.is_bookmarked ? 'active' : ''}" data-id="${item.id}" title="${item.is_bookmarked ? 'Remove Bookmark' : 'Bookmark Article'}">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="${item.is_bookmarked ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      </div>
    </article>
  `;
}

// Attach Event Listeners to Bookmark Buttons
function attachBookmarkListeners() {
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const articleId = btn.getAttribute('data-id');
      const article = state.articles.find(a => a.id === articleId);
      if (!article) return;

      // Optimistic UI Update
      article.is_bookmarked = !article.is_bookmarked;
      renderCategoryPills();
      render();

      showToast(article.is_bookmarked ? 'Saved to bookmarks ♥' : 'Removed from bookmarks', 'info');

      try {
        await POST('/api/bookmark', { article_id: articleId });
      } catch (err) {
        console.error('Bookmark API Error:', err);
        article.is_bookmarked = !article.is_bookmarked; // Rollback
        render();
      }
    });
  });
}

// Helper Utilities
function updateHeaderTime() {
  if (!state.lastUpdated) return;
  lastUpdatedText.textContent = `Updated ${formatRelativeTime(state.lastUpdated)}`;
}

function formatRelativeTime(dateStr) {
  try {
    const dt = new Date(dateStr);
    const now = new Date();
    const diffSec = Math.floor((now - dt) / 1000);
    
    if (diffSec < 60) return 'just now';
    if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`;
    if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`;
    return `${Math.floor(diffSec / 86400)}d ago`;
  } catch (e) {
    return 'recently';
  }
}

function escapeHTML(str) {
  return (str || '').replace(/[&<>"']/g, match => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[match]));
}

async function POST(url, body = {}) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return res.json();
}

function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toastContainer.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}
