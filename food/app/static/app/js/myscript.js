$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


$('.plus-cart').click(function(){
    var id = $(this).attr("pid");
    var eml = $(this).siblings("#quantity");
    console.log("pid= ", id);
    $.ajax({
        type: "GET",
        url: "/pluscart/",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log("data= ", data);
            eml.text(data.quantity);
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid");
    var eml = $(this).siblings("#quantity");
    $.ajax({
        type: "GET",
        url: "/minuscart/",
        data: {
            prod_id: id
        },
        success: function(data){
            eml.text(data.quantity);
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
        }
    });
});



$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data){
            // console.log("Amount:", data.amount);
            // console.log("Total Amount:", data.totalamount);
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            console.log("Removing item from DOM");
            $(eml).closest('.row').remove(); // Remove the item from the DOM
            if (parseInt(data.amount) === 0) { // Check if amount becomes zero
                $('.text-center.mb-5').show(); // Show the "Cart Is Empty" section
                $('.col-lg-8').hide(); // Hide the column containing cart items
                $('.col-lg-4').hide(); // Hide the column containing total amount
            }
        }
    });
});


$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})