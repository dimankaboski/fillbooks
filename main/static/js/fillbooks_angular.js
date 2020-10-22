var app = angular.module('fillbooks_app', []);
app.controller('fillbooks_controller', ['$scope', '$http',

    function ($scope, $http) {
        function ajax(url, data) {
            var req = {
                method: 'POST',
                url: url,
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(data)
            };
            $http(req).then(function (response) {
                if (response.status == 200) {
                    location.reload()
                }

            });
        }
        
    }
]);