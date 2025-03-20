// Chọn tất cả các nút có lớp 'add-to-cart'
var addToCartBtns = document.getElementsByClassName('add-to-cart');

// Lặp qua từng nút và thêm sự kiện click
for (var i = 0; i < addToCartBtns.length; i++) {
    addToCartBtns[i].addEventListener('click', function () {
        // Lấy dữ liệu từ thuộc tính data-product và data-action
        var productId = this.dataset.product;
        var action = this.dataset.action;

        // Ghi thông tin ra console để kiểm tra
        console.log('productId:', productId, 'action:', action);

        // Gọi hàm xử lý nếu cần (ví dụ: gửi request tới server)
        // addToCart(productId, action);
        console.log('user :',user)
        if (user === "AnonymousUser"){
          console.log('user not logged in')
        //   updateUserOrder(productId,action)

        }else {
            updateUserOrder(productId,action)
        }
    })
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
