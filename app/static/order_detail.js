const addBtn = document.getElementById("addBtn");

const order_form_detail = document.getElementById("order-form-detail");

const orderBtn = document.getElementById("orderBtn");

const my_order_list = document.getElementById("my-order-list")

let list = []
function painting(orderObj){
    const li = document.createElement("li");
    li.id = orderObj.id;

    const span = document.createElement("span");
    span.innerText = `메뉴 : ${orderObj.formdata.menu} / 개수 : ${orderObj.formdata.quantity} / 옵션 : ${orderObj.formdata.option}`;

    const btn = document.createElement("button");
    btn.addEventListener("click", deleteOrder)
    btn.innerText = "❌";

    li.appendChild(span);
    li.appendChild(btn);

    my_order_list.appendChild(li);
}

function deleteOrder(event){
    const li = event.target.parentNode;
    list = list.filter((item) => { return Number(li.id) != item.id });
    li.remove();
}


function save(form){
    const orderObj = {
        id: Date.now(),
        formdata: {
            menu: form[0].value,
            quantity: form[1].value,
            option: form[2].value
        }
    };
    list.push(orderObj);
    painting(orderObj);
}

function submitForm(){
    const result = confirm('주문을 확정하시겠습니까?\n주문을 취소하시려면 대표주문자에게 직접 연락하셔야합니다.');
    if(result == true){
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(list)  
        }).then(() => location.reload());
        list = []
    }
    else{
        alert('확정을 취소했습니다')
    }
}

function addOrder(event){
    event.preventDefault();
    console.log(order_form_detail[0].value);
    console.log(order_form_detail[1].value);
    if (order_form_detail[0].value == '' || order_form_detail[1].value == ''){
        alert('입력을 완료해주세요')
    }
    else{
        if(order_form_detail[2].value == ''){
            order_form_detail[2].value = '없음'
        }
        save(order_form_detail);
        order_form_detail.reset();
    }
}

orderBtn.addEventListener("click", submitForm); 
addBtn.addEventListener("click", addOrder);