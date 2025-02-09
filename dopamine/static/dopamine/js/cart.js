document.addEventListener('DOMContentLoaded', function () {
    // Tìm tất cả các nút giỏ hàng
    const cartIcons = document.querySelectorAll('.add-to-cart');
  
    // Gắn sự kiện click
    cartIcons.forEach(icon => {
      icon.addEventListener('click', function (event) {
        event.preventDefault(); // Ngăn hành động mặc định của thẻ <a>
  
        // Lấy thông tin từ data-product (nếu có)
        const productId = this.getAttribute('data-product');
        const action = this.getAttribute('data-action');
        // Hiển thị thông báo trong console
        console.log(`productId`,productId,'action',action);
    });
    });
  });
  