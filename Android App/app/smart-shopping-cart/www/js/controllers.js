angular.module('starter.controllers', [])

.controller('AppCtrl', function($scope, $ionicModal, $timeout) {

  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  // Form data for the login modal
  $scope.loginData = {};

  // Create the login modal that we will use later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // Perform the login action when the user submits the login form
  $scope.doLogin = function() {
    console.log('Doing login', $scope.loginData);

    // Simulate a login delay. Remove this and replace with your login
    // code if using a login system
    $timeout(function() {
      $scope.closeLogin();
    }, 1000);
  };
})

.controller('PlaylistsCtrl', function($scope, $interval, Items, $ionicPopup, $cordovaNativeAudio) {
    var isMobile = {
        Android: function() {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function() {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function() {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function() {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function() {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function() {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    };

if(isMobile.any())
  $cordovaNativeAudio.preloadSimple('click', 'res/get.mp3')

  var userid;
  $scope.data = {};
      // Custom popup
    $ionicPopup.show({
         template: '<input type = "text" ng-model = "data.userid">',
         title: 'Login',
         subTitle: 'Please enter cart id',
         scope: $scope,
      
         buttons: [
            {
               text: '<b>OK</b>',
               type: 'button-positive',
               onTap: function(e) {
                 userid = String($scope.data.userid);
                 console.log(userid);
               }
            }
         ]
      })



var imgUrl = "img/logo.png";
var prelen = 0;
 $scope.sendorder = function() {
   $ionicPopup.show({
                  template: '<div ><h>Thanks!</h><p ng-model="cur_price" ><br>Your order is completed<br></p><b>Price: ${{cur_price | number: 2}} </b><br><b ng-model="cur_price">Tax: ${{cur_price* 0.08 | number : 2}}  </b><img src="'+ imgUrl +'" ></img> </div>',
                  cssClass: 'orderCompleted_popup',
                  scope: $scope,
                  buttons: [{
                    text: 'OK',
                    type: 'button-positive',
      }]
    })
 };



var apigClient = apigClientFactory.newClient({
  apiKey: ''
});




 var coke, water, apple, banana, orange, cookie;

    coke = {
      id: 0,
      name: 'Coke',
      img: 'img/coke.png',
      img_detail: 'img/shirt_detail.png',
      price: 2.98,
      quantity: 0,
      s: '1'
    };
    water =
    {
      id: 1,
      name: 'Evian Water',
      img: 'img/water.png',
      img_detail: 'img/pants_detail.png',
      price: 1.98,
      quantity: 0,
      s: '1'
    };
    apple =
    {
      id: 2,
      name: 'Apple',
      img: 'img/apple.png',
      img_detail: 'img/sweater_detail.png',
      price: 7.98,
      quantity: 0,
      s: '1'
    };
    orange =
    {
      id: 3,
      name: 'Orange',
      img: 'img/orange.png',
      img_detail: 'img/sweater_detail.png',
      price: 2.98,
      quantity: 0,
      s: '1'
    };
    banana =
    {
      id: 4,
      name: 'Banana',
      img: 'img/banana.png',
      img_detail: 'img/sweater_detail.png',
      price: 1.98,
      quantity: 0,
      s: '1'
    };
      cookie = {
      id: 0,
      name: 'Cookie',
      img: 'img/cookie.png',
      img_detail: 'img/shirt_detail.png',
      price: 2.98,
      quantity: 0,
      s: '1'
    };

    var pre

    var items = [coke, water, apple, banana, orange, cookie];
    var cart = [];
    $scope.recommends = [coke];
    $scope.cur_price = 0;
    var count = 0;
    var update = $interval(function() {

   let params = {
        "Content-Type": "application/json"
    };
    let body = {
      "request": userid
    };
    let additionalParams = {

    };
    let response = "";
    apigClient.ioTFetchPost(params,body,additionalParams).then(function(result){
      console.log(result);
      response = JSON.parse(result["data"]["body"]);
      var i = 0;
      var cart = [];
      var modify = false;
      var update_rec = false;
 while(i<response.length){

        if(response[i]["item"] == "Water"){
          if(water["quantity"] != Number(response[i]["amount"])){
            water["quantity"] = Number(response[i]["amount"]);
            water["s"] = Number(response[i]["amount"]);
            modify = true;
          }
          water["price"] = Number(response[i]["price"]);
          if(water["quantity"] > 0)
            cart.push(water);
        }
        else if(response[i]["item"] == "Banana"){
              if(banana["quantity"] != Number(response[i]["amount"])){
            banana["quantity"] = Number(response[i]["amount"]);
            banana["s"] = Number(response[i]["amount"]) + ' kg';
            modify = true;
          }
       
          banana["price"] = Number(response[i]["price"]);
          if(banana["quantity"] > 0)
            cart.push(banana);
        }
          else if(response[i]["item"] == "Coke"){
            if(coke["quantity"] != Number(response[i]["amount"])){
            coke["quantity"] = Number(response[i]["amount"]);
            coke["s"] = Number(response[i]["amount"]);
            modify = true;
          }
         
          coke["price"] = Number(response[i]["price"]);
          if(coke["quantity"] > 0)
            cart.push(coke);
        }
                  else if(response[i]["item"] == "Apple"){
            if(apple["quantity"] != Number(response[i]["amount"])){
            apple["quantity"] = Number(response[i]["amount"]);
            apple["s"] = Number(response[i]["amount"]) + " kg";
            modify = true;
          }
          apple["price"] = Number(response[i]["price"]);
          if(apple["quantity"] > 0)
            cart.push(apple);
        }
                  else if(response[i]["item"] == "Orange"){
            if(orange["quantity"] != Number(response[i]["amount"])){
            orange["quantity"] = Number(response[i]["amount"]);
            orange["s"] = Number(response[i]["amount"]) + " kg";
            modify = true;
          }
          orange["price"] = Number(response[i]["price"]);
          if(orange["quantity"] > 0)
            cart.push(orange);
        }
              else if(response[i]["item"] == "Cookie"){
         if(cookie["quantity"] != Number(response[i]["amount"])){
            cookie["quantity"] = Number(response[i]["amount"]);
              cookie["s"] = Number(response[i]["amount"]);
            modify = true;
          }
          cookie["price"] = Number(response[i]["price"]);
          if(cookie["quantity"] > 0)
            cart.push(cookie);
        }
        else if(response[i]["item"] == "Recommendation"){
            if(response[i]["amount"] == 'Coke'){
                $scope.recommends = [coke];
            }else  if(response[i]["amount"]== 'Cookie'){
       $scope.recommends = [cookie];
            }else  if(response[i]["amount"] == 'Water'){
   $scope.recommends = [water];
            }else  if(response[i]["amount"] == 'Apple'){
    $scope.recommends = [apple];
            }else  if(response[i]["amount"] == 'Orange'){
      $scope.recommends = [orange];
            }else  if(response[i]["amount"] == 'Banana'){
        $scope.recommends = [banana];
           }
        }
        //console.log(response[i])
         i++;
      }
      // if(prelen!= cart.length)
      //   modify == true;
      
      // prelen = cart.length;
      // if(modify == true){
          $scope.items = cart;
          var j = 0;
          var sum = 0;
          while(j<cart.length){
            sum = sum + cart[j]["price"]*cart[j]["quantity"];
            j++;
          }
          $scope.cur_price = sum;
          //$cordovaVibration.vibrate(100);
          if(isMobile.any() && modify == true)
              $cordovaNativeAudio.play('click');
      
    });
  }, 250);



})

.controller('PlaylistCtrl', function($scope, $stateParams) {
});
