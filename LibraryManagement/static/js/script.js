// ============================================
// LIBRARY PRO - MAIN JAVASCRIPT
// ============================================

// Auto-hide alerts after 5 seconds
document.addEventListener("DOMContentLoaded", function() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});

// Confirm delete actions
function confirmDelete(message) {
  return confirm(message || 'Bạn có chắc chắn muốn thực hiện hành động này?');
}

// Format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount);
}

// Add loading state to buttons
document.addEventListener('DOMContentLoaded', function() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i>Đang xử lý...';
        submitBtn.disabled = true;
        
        // Re-enable after 3 seconds (fallback)
        setTimeout(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }, 3000);
      }
    });
  });
});

// Sidebar active link highlighting
document.addEventListener('DOMContentLoaded', function() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.sidebar-menu .nav-link');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href)) {
      link.classList.add('active');
    }
  });
});

// Search form enhancement
document.addEventListener('DOMContentLoaded', function() {
  const searchInputs = document.querySelectorAll('input[name="search"]');
  searchInputs.forEach(input => {
    input.addEventListener('input', function() {
      if (this.value.length > 0) {
        this.parentElement.classList.add('focused');
      } else {
        this.parentElement.classList.remove('focused');
      }
    });
  });
});

// Table row click effect
document.addEventListener('DOMContentLoaded', function() {
  const tableRows = document.querySelectorAll('tbody tr');
  tableRows.forEach(row => {
    row.addEventListener('click', function(e) {
      // Don't trigger if clicking on a link or button
      if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' || 
          e.target.closest('a') || e.target.closest('button')) {
        return;
      }
      
      // Add highlight effect
      this.style.backgroundColor = '#f1f5f9';
      setTimeout(() => {
        this.style.backgroundColor = '';
      }, 300);
    });
  });
});

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

// Print functionality
function printPage() {
  window.print();
}

// Export data to CSV (utility function)
function exportToCSV(data, filename) {
  if (!data || data.length === 0) {
    alert('Không có dữ liệu để xuất!');
    return;
  }
  
  const headers = Object.keys(data[0]);
  const csvContent = [
    headers.join(','),
    ...data.map(row => headers.map(header => 
      `"${(row[header] || '').toString().replace(/"/g, '""')}"`
    ).join(','))
  ].join('\n');
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = filename;
  link.click();
}

// Smooth scroll to top
function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Add scroll to top button
document.addEventListener('DOMContentLoaded', function() {
  const scrollBtn = document.createElement('button');
  scrollBtn.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
  scrollBtn.className = 'btn btn-primary scroll-top-btn';
  scrollBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  `;
  scrollBtn.onclick = scrollToTop;
  document.body.appendChild(scrollBtn);
  
  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
      scrollBtn.style.display = 'flex';
    } else {
      scrollBtn.style.display = 'none';
    }
  });
});

// Prevent form double submission
document.addEventListener('DOMContentLoaded', function() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      if (form.dataset.submitted === 'true') {
        e.preventDefault();
        return false;
      }
      form.dataset.submitted = 'true';
    });
  });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Ctrl + K for search focus
  if (e.ctrlKey && e.key === 'k') {
    e.preventDefault();
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
      searchInput.focus();
    }
  }
  
  // Escape to close modals
  if (e.key === 'Escape') {
    const modals = document.querySelectorAll('.modal.show');
    modals.forEach(modal => {
      const modalInstance = bootstrap.Modal.getInstance(modal);
      if (modalInstance) {
        modalInstance.hide();
      }
    });
  }
});

// Initialize all functionality
console.log('📚 Library Pro - Hệ thống Quản lý Thư viện đã sẵn sàng!');
console.log('💡 Mẹo: Nhấn Ctrl + K để tìm kiếm nhanh');