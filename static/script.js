// Script cho trang tra cứu tên miền
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector(".search-input");
  const searchButton = document.querySelector(".search-button");

  searchButton.addEventListener("click", function () {
    performSearch();
  });

  searchInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      performSearch();
    }
  });

  function performSearch() {
    const searchTerm = searchInput.value.trim();

    if (searchTerm === "") {
      alert("Vui lòng nhập tên miền cần tra cứu");
      return;
    }

    // Sử dụng Flask route thay vì static HTML
    window.location.href = `/result?domain=${encodeURIComponent(
      searchTerm
    )}`;
  }

  const cards = document.querySelectorAll(".card");

  const observerOptions = {
    threshold: 0.2,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "0";
        entry.target.style.transform = "translateY(30px)";

        setTimeout(() => {
          entry.target.style.transition =
            "opacity 0.6s ease, transform 0.6s ease";
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
        }, 100);

        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  cards.forEach((card) => {
    observer.observe(card);
  });

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  const placeholders = [
    "Nhập tên miền cần tra cứu...",
    "Ví dụ: example.vn",
    "Ví dụ: google.com.vn",
    "Ví dụ: ministry.gov.vn",
  ];

  let placeholderIndex = 0;

  setInterval(() => {
    placeholderIndex = (placeholderIndex + 1) % placeholders.length;
    searchInput.placeholder = placeholders[placeholderIndex];
  }, 3000);
});

