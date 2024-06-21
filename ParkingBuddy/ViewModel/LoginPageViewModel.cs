using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace ParkingBuddy.ViewModel
{
    public partial class LoginPageViewModel : ObservableObject
    {
        private readonly BackendClient _client = new("http://34.118.78.253/", new HttpClient());

        [ObservableProperty]
        string loginIntro = "Welcome to the Parking Buddy app";

        [ObservableProperty]
        string emailEntry = "";

        [ObservableProperty]
        string passwordEntry = "";

        [ObservableProperty]
        string errorMessage = "";

        [RelayCommand]
        async Task LoginButtonPressed()
        {
            UserModel user = new UserModel()
            {
                Email = EmailEntry
            };
            byte[] bytes = [];

            using (HashAlgorithm algorithm = SHA256.Create())
                if (algorithm != null)
                {
                    bytes = algorithm.ComputeHash(Encoding.UTF8.GetBytes(PasswordEntry));
                }

            StringBuilder sb = new();
            foreach (byte b in bytes)
                sb.Append(b.ToString("X2"));

            user.Password = sb.ToString();

            try
            {
                var response = await _client.Get_user_data_users_data_postAsync(user);
                if (response != null && response.Username != "")
                {
                    await Shell.Current.GoToAsync("UserMainPage", new Dictionary<string, object>
                    {
                        { nameof(UserDataModel), response }
                    });
                    EmailEntry = "";
                    PasswordEntry = "";
                    ErrorMessage = "";
                }
                else
                {
                    ErrorMessage = "Failed to log in. Are you sure email and password are correct?";
                }
            }
            catch (ApiException ex)
            {
                try
                {
                    ErrorMessage = JObject.Parse(ex.Response).Value<string>("message") ?? "Shit";
                }
                catch
                {
                    ErrorMessage = ex.Message;
                }
            }
            
        }

        [RelayCommand]
        async Task RegisterNavButtonPressed()
        {
            await Shell.Current.GoToAsync("//LoginPage/RegistrationPage");
            EmailEntry = "";
            PasswordEntry = "";
            ErrorMessage = "";
        }
    }
}
