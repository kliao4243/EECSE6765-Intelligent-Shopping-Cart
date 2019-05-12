angular.module('app.services', [])

.factory('Items', function() {
    var cart = {};
    var coke, water, apple;

    coke = {
      id: 0,
      name: 'Coke',
      img: 'img/shirt.png',
      img_detail: 'img/shirt_detail.png',
      price: 2.98,
      quantity: 0
    };
    water =
    {
      id: 1,
      name: 'Evian Water',
      img: 'img/pants.png',
      img_detail: 'img/pants_detail.png',
      price: 1.98,
      quantity: 0
    };
    apple =
    {
      id: 2,
      name: 'Apple',
      img: 'img/sweater.png',
      img_detail: 'img/sweater_detail.png',
      price: 7.98,
      quantity: 0,
    };
   



    var items = [coke, water, apple];

  
    function getCartPrice(){
      var cartPrice = 0;
      for (var key in cart) {
          cartPrice += (cart[key].item.price * cart[key].quantity);
      }
      return cartPrice;
    }
    function roundNum(num){
      return parseFloat(Math.round(num * 100) / 100).toFixed(2);
    }
    return {
    	getItems: function(){
    		return items;
    	},
        setPrice: function(val) {
          for (var i=0;i<val.length;i++){
            items[i].price = val[i];
          }
        },
        all: function() {
          return items;
        },
        get: function(itemId) {
          for (var i = 0; i < items.length; i++) {
              if (items[i].id === parseInt(itemId)) {
                  return items[i];
              }
          }
          return null;
        },
        getTotalPrice: function(){
            var cartPrice = getCartPrice();
            return roundNum(cartPrice);
        },
        getCartPrice: function(){
            var cartPrice = getCartPrice();
            return roundNum(cartPrice);
        },
        showCart: function(){
            return cart;
        },
        clear: function(){
            cart = {};
            for (var key in items) {

                items[key]["quantity"]=0;
            }
      
        }
  };
})

