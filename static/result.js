document.addEventListener("DOMContentLoaded", function () {
  //Lấy domain từ URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const domain = urlParams.get("domain");

  //Xử lý tìm kiếm mới
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  searchBtn.addEventListener("click", function () {
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

    // Reload trang với domain mới - sử dụng Flask route
    window.location.href = `/result?domain=${encodeURIComponent(
      searchTerm
    )}`;
  }

  //Lấy các phần tử HTML
  const warningBox = document.getElementById("warningBox");
  const warningTitle = document.getElementById("warningTitle");
  const warningDescription = document.getElementById("warningDescription");
  const iconPath = document.getElementById("warningIconPath");
  const iconText = document.getElementById("warningIconText");

  //Hàm gọi API Flask
  async function fetchApiResult(url) {
    // Hiển thị trạng thái đang tải
    warningTitle.textContent = "ĐANG PHÂN TÍCH...";
    warningDescription.textContent = `Vui lòng chờ trong khi hệ thống phân tích: ${url}`;
    warningBox.classList.remove("safe", "fake");

    try {
      const response = await fetch("/api/check", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: url }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Lỗi máy chủ API");
      }

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error || "Lỗi khi xử lý URL");
      }

      //Lấy tỷ lệ phần trăm lừa đảo từ Flask API
      const percentage = data.phishing_probability.toFixed(2);

      //is_safe = false nghĩa là giả mạo
      if (!data.is_safe) {
        warningBox.classList.remove("safe");
        warningBox.classList.add("fake");
        warningTitle.textContent = `WEBSITE NÀY GIẢ MẠO (${percentage}%)`;
        warningDescription.textContent =
          "Cảnh báo: Website này có dấu hiệu giả mạo. Vui lòng không cung cấp thông tin cá nhân hoặc thực hiện giao dịch tài chính!";
        iconPath.setAttribute("fill", "#DC143C");
        iconText.textContent = "!";
      } else {
        warningBox.classList.remove("fake");
        warningBox.classList.add("safe");
        warningTitle.textContent = `WEBSITE NÀY AN TOÀN - TỶ LỆ GIẢ MẠO: (${percentage}%)`;
        warningDescription.textContent =
          "Website này có vẻ an toàn. Tuy nhiên vẫn cần cẩn trọng khi cung cấp thông tin cá nhân.";
        iconPath.setAttribute("fill", "#28a745");
        iconText.textContent = "✓";
      }
    } catch (error) {
      // Xử lý lỗi
      warningBox.classList.remove("safe");
      warningBox.classList.add("fake");
      warningTitle.textContent = "LỖI KẾT NỐI API";
      warningDescription.textContent = `Không thể kết nối đến máy chủ phân tích. (Lỗi: ${error.message}). Vui lòng chạy file app.py trước!`;
      iconPath.setAttribute("fill", "#DC143C");
      iconText.textContent = "!";
    }
  }

  // Tự động chạy khi tải trang
  if (domain) {
    // Nếu có domain, gọi hàm API
    fetchApiResult(domain);
  } else {
    // Nếu không có domain (lần đầu vào trang)
    warningTitle.textContent = "CHƯA CÓ URL";
    warningDescription.textContent =
      "Vui lòng nhập một URL vào thanh tìm kiếm ở trên để bắt đầu phân tích.";
  }
});

