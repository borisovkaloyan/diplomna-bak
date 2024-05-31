using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ParkingBuddy.ViewModel
{
    public partial class RegistrationPageViewModel : ObservableObject
    {
        private readonly BackendClient _client = new("http://34.118.78.253/", new HttpClient());

        [ObservableProperty]
        string registrationLabel = "Register as a new user";

        [ObservableProperty]
        string emailEntry = "";

        [ObservableProperty]
        string usernameEntry = "";

        [ObservableProperty]
        string passwordEntry = "";

        [ObservableProperty]
        string repeatPasswordEntry = "";

        [ObservableProperty]
        string errorMessage = "";

        public RegistrationPageViewModel()
        {
        }

        [RelayCommand]
        async void RegisterButtonPressed()
        {
            if (!string.IsNullOrEmpty(PasswordEntry) && 
                !string.IsNullOrEmpty(RepeatPasswordEntry) && 
                (PasswordEntry == RepeatPasswordEntry))
            {
                CreateUserModel model = new CreateUserModel()
                {
                    Username = UsernameEntry,
                    Email = EmailEntry,
                    Password = PasswordEntry
                };

                try
                {
                    var result = await _client.Create_new_user_users_new_postAsync(model);
                }
                catch (ApiException ex)
                {
                    if (ex.StatusCode != 201)
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
                    else
                    {
                        ErrorMessage = "";
                        await Shell.Current.GoToAsync("UserMainPage", new Dictionary<string, object>
                        {
                            { 
                                nameof(UserDataModel), new UserDataModel()
                                {
                                    Username = UsernameEntry,
                                    Email = EmailEntry,
                                    Registration_plates = []
                                }
                            }
                        });
                        UsernameEntry = "";
                        EmailEntry = "";
                        PasswordEntry = "";
                        RepeatPasswordEntry = "";
                    }
                }
            }
        }
    }
}
