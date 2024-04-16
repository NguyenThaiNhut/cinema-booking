console.log("Sanity check!");

// Get Stripe publishable key
fetch("config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  document.querySelector("#btn-payment-submit").addEventListener("click", (event) => {
    event.preventDefault();

    // Lấy giá trị từ các trường input
    var name = document.getElementById("name").value;
    var phone = document.getElementById("phone").value;
    
    fetch("/payment/create-checkout-session/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name,
        phone: phone
      }),
    })
    .then((result) => { 
        return result.json(); 
    })
    .then((data) => {
      
      if (data.success){
        console.log(data.sessionId)
        return stripe.redirectToCheckout({sessionId: data.sessionId})
      } else {
        if(data.errors["name"] != undefined){
          alert(`${data.errors["name"]}`)
        }
        if(data.errors["phone"] != undefined){
          alert(`${data.errors["phone"]}`)
        }
          
      }
    })
    .then((res) => {
      console.log(res);
    });
  });
});