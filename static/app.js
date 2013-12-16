function getVideoId(url) {
    if (url.indexOf('watch') > -1) {
        return url.slice(url.indexOf('v=')+2).match(/^[a-zA-Z0-9]+/)[0];
    } else if (url.indexOf("youtu.be/")) {
        return url.slice(url.indexOf("youtu.be/")+9);
    } else {
        throw "Invalid youtube url";
    }

}function PinrCtl($scope, $http) {
    $http.get('/items').success(function(data) {  
        $scope.items = data.items;    
    });
    $scope.showMenu = function(which) {
        if ($(which).is(':visible')) {
            $(".dropdown").hide();
        } else {
            $(".dropdown").hide();
            $(which).show();
        }
    }
    $scope.addText = function() {
        var data = {text: $scope.text, type: 'text'}
        $http.post('/items', data).success(function(data) {
            $scope.items.push(data.items);
            $(".dropdown").hide();
            $scope.text = "";
        });
    }
    $scope.addImage = function() {
        var data = {image: $scope.text, type: 'image'}
        $http.post('/items', data).success(function(data) {
            $scope.items.push(data.items);
            $(".dropdown").hide();
            $scope.text = "";
        });
    }

    $scope.showThis = false;
}
