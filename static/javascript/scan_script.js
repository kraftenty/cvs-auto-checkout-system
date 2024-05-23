const socket = io();
let totalPrice = 0; // 총 가격을 저장할 변수

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
});

socket.on('item', function(data) {
    const tableBody = document.getElementById('item-table').getElementsByTagName('tbody')[0];
    const row = tableBody.insertRow();
    const cell1 = row.insertCell(0);
    const cell2 = row.insertCell(1);
    const cell3 = row.insertCell(2);
    const cell4 = row.insertCell(3);

    cell1.innerHTML = data.name;
    cell2.innerHTML = data.price;
    cell3.innerHTML = `<div class="quantity-control">
        <button class="decrease" disabled>-</button>
        <span class="quantity">${data.quantity}</span>
        <button class="increase">+</button>
    </div>`;
    cell4.innerHTML = '<button class="remove">삭제</button>';

    // 총 가격 업데이트
    totalPrice += data.price;
    document.getElementById('total-price').innerText = totalPrice;

    // 결제 버튼 활성화
    if (totalPrice > 0) {
        document.getElementById('submit-button').classList.remove('disabled-button');
        document.getElementById('submit-button').disabled = false;
    }

    // 버튼 이벤트 핸들러 추가
    const decreaseButton = cell3.querySelector('.decrease');
    const increaseButton = cell3.querySelector('.increase');
    const quantitySpan = cell3.querySelector('.quantity');
    const removeButton = cell4.querySelector('.remove');

    increaseButton.addEventListener('click', function() {
        let quantity = parseInt(quantitySpan.innerText);
        quantity += 1;
        quantitySpan.innerText = quantity;
        if (quantity > 1) {
            decreaseButton.disabled = false;
        }
        totalPrice += data.price;
        document.getElementById('total-price').innerText = totalPrice;
    });

    decreaseButton.addEventListener('click', function() {
        let quantity = parseInt(quantitySpan.innerText);
        if (quantity > 1) {
            quantity -= 1;
            quantitySpan.innerText = quantity;
            totalPrice -= data.price;
            document.getElementById('total-price').innerText = totalPrice;
            if (quantity === 1) {
                decreaseButton.disabled = true;
            }
        }
    });

    removeButton.addEventListener('click', function() {
        const row = this.closest('tr');
        const quantity = parseInt(quantitySpan.innerText);
        totalPrice -= data.price * quantity;
        document.getElementById('total-price').innerText = totalPrice;
        row.remove();

        if (totalPrice === 0) {
            document.getElementById('submit-button').classList.add('disabled-button');
            document.getElementById('submit-button').disabled = true;
        }
    });
});

document.getElementById('payment-form').onsubmit = function(event) {
    if (totalPrice === 0) {
        alert('상품이 스캔되지 않았습니다.');
        event.preventDefault();
        return;
    }

    const paymentMethod = document.querySelector('input[name="payment_method"]:checked').value;
    // 가격 
    document.getElementById('total-price-input').value = totalPrice;
    // 결제 수단
    document.getElementById('payment-method-input').value = paymentMethod;
    // 날짜
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    document.getElementById('year-input').value = year;
    document.getElementById('month-input').value = month;
    document.getElementById('day-input').value = day;
};