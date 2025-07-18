// Chọn tất cả các nút có lớp 'add-to-cart'
var addToCartBtns = document.getElementsByClassName('add-to-cart');

// Lặp qua từng nút và thêm sự kiện click
for (var i = 0; i < addToCartBtns.length; i++) {
    addToCartBtns[i].addEventListener('click', function (e) {
        e.preventDefault();  

        var productId = this.dataset.product;
        var action = this.dataset.action;

        console.log('productId:', productId, 'action:', action);
        console.log('user :', user);

        if (user === "AnonymousUser") {
            console.log('user not logged in');
        } else {
            updateUserOrder(productId, action);
        }
    });
}

// Hàm xử lý hành động thêm vào giỏ hàng (nếu cần thiết)
function addToCart(productId, action) {
    console.log('Thêm sản phẩm vào giỏ hàng:', productId, 'với hành động:', action);
    // Thực hiện xử lý (ví dụ: gửi dữ liệu tới API hoặc server)
}

function updateUserOrder(productId,action){
    console.log('user logged in, success add')
    var url = '/update_item/'
    fetch(url,{
      method: 'POST',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken': csrftoken ,
      },
      body: JSON.stringify({'productId':productId,'action':action})
    })
    .then((response) =>{
      return response.json()
    })
    .then((data) =>{
      console.log('data',data)
      location.reload()
    })
  }
document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.querySelectorAll('.chg-quantity');

  buttons.forEach(button => {
    button.addEventListener('click', function () {
      const productId = this.dataset.product;
      const action = this.dataset.action;

      if (user === "AnonymousUser") {
        console.log("User not logged in");
        return;
      }

      updateUserOrder(productId, action);
    });
  });

  function updateUserOrder(productId, action) {
    const url = '/update_item/';
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ productId: productId, action: action })
    })
    .then(res => res.json())
    .then(data => {
      console.log('Updated:', data);
      location.reload();  // Cập nhật lại trang
    });
  }
});
