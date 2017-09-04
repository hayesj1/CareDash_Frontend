function SignUpViewModel() {
    var self = this;
    self.signupURI = 'http://localhost:5000/providers/signup';
    self.firstName = ko.observable("");
    self.lastName = ko.observable("");
    self.email = ko.observable("");
    self.password = ko.observable("");
    self.passwordConfirm = ko.observable("");

    self.signupError = ko.observable("");
    self.confirmations = ko.observable("");

    self.ajax = function(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(data),
            error: function(jqXHR) {
                console.log("ajax error " + jqXHR.status);
            }
        };
        return $.ajax(request);
    }

    self.signup = function() {
        // Basic Validation
        if (self.firstName() == "" || self.lastName() == "" || self.email() == "" || self.password() == "" || self.passwordConfirm() == "") {
            self.signupError("All fields are required!");
            return;
        } else if (self.password() != self.passwordConfirm()) {
            self.signupError("Passwords must match!");
            return;
        }

        data = {
            fname: self.firstName(),
            lname: self.lastName(),
            email: self.email(),
            password: self.password()
        }
        self.ajax(self.signupURI, 'POST', data).done(function(data) {
            self.reset();
            self.signupError("");
            self.confirmations("Sign Up Successful!");
        }).fail(function(jqXHR) {
            if (jqXHR.status == 409)
               self.signupError("Email is already in use!");
               self.confirmations("");
            self.reset();
        });
    }

    self.reset = function() {
        self.firstName("");
        self.lastName("");
        self.email("");
        self.password("");
        self.passwordConfirm("");
    }
}

function LoginViewModel() {
    var self = this;
    self.loginURI = 'http://localhost:5000/providers/login';
    self.email = ko.observable("");
    self.password = ko.observable("");

    self.loginError = ko.observable("");

    self.ajax = function(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: JSON.stringify(data),
            error: function(jqXHR) {
                console.log("ajax error " + jqXHR.status);
            }
        };
        return $.ajax(request);
    }

    self.login = function() {
        // Basic Validation
        if (self.email() == "" || self.password() == "") {
            self.loginError("All fields are required!");
            return;
        }

        data = {
            email: self.email(),
            password: self.password()
        }
        self.ajax(self.loginURI, 'POST', data).done(function(data) {
            $('#loginDialog').modal('hide');
            self.reset();
            signupViewModel.signupError("");
            signupViewModel.confirmations("Log in Successful!");
        }).fail(function(jqXHR) {
            if (jqXHR.status == 403)
               self.loginError("Invalid email or password!");
            self.reset();
        });
    }

    self.reset = function() {
        self.email("");
        self.password("");
    }
}

var signupViewModel = new SignUpViewModel();
var loginViewModel = new LoginViewModel();

$(function() {
    ko.applyBindings(signupViewModel, $("#signupForm")[0]);
    ko.applyBindings(loginViewModel, $("#loginDialog")[0]);
});
