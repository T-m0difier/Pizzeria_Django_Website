        $(document).ready(function () {
            let $loginForm = $("#loginForm");
            let $registerForm = $("#registerForm");
            let $modalTitle = $("#modalTitle");

        // Toggle between login and register forms
            $("#toggleRegister").on("click", function (e) {
                e.preventDefault();
                $loginForm.hide();
                $registerForm.show();
                $modalTitle.text("Register");
            });

            $("#toggleLogin").on("click", function (e) {
                e.preventDefault();
                $registerForm.hide();
                $loginForm.show();
                $modalTitle.text("Login");
            });

        // Check for error flags and open modal accordingly
            if ($("#loginError").val() === "True") {
                $loginForm.show();
                $registerForm.hide();
                $modalTitle.text("Login");
                $("#authModal").modal("show");
            }

            if ($("#registerError").val() === "True") {
                $registerForm.show();
                $loginForm.hide();
                $modalTitle.text("Register");
                $("#authModal").modal("show");
            }

            if ($("#updateError").val() === "True") {
                $("#profileView").hide();
                $("#profileForm").show();
                $("#accountModalTitle").text("Update Profile");
                $("#updateProfileModal").modal("show");
            }
        });



            document.addEventListener("DOMContentLoaded", function () {
                var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                tooltipTriggerList.forEach(function (tooltipTriggerEl) {
                    new bootstrap.Tooltip(tooltipTriggerEl);
                });
            });



        $(document).ready(function () {
            let $profileView = $("#profileView");
            let $profileForm = $("#profileForm");
            let $accountModalTitle = $("#accountModalTitle");
        // Switch to Update Profile
            $("#toggleUpdateProfile").on("click", function (e) {
                e.preventDefault();
                $profileView.hide();
                $profileForm.show();
                $accountModalTitle.text("Update Profile");
            });

            // Switch back to Profile View
            $("#toggleProfileView").on("click", function (e) {
                e.preventDefault();
                $profileForm.hide();
                $profileView.show();
                $accountModalTitle.text("Your Account");
            });


        });


        $(document).ready(function () {
            $("#openUpdateProfile").on("click", function () {
                $("#accountModal").modal("hide");
                $("#updateProfileModal").modal("show");
            });
        });

        $(document).ready(function () {
            // Check if there's a modal ID passed from the backend
            if (typeof openModalId !== 'undefined' && openModalId) {
                $('#' + openModalId).modal('show');
            }
        });

        
        