using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Newtonsoft.Json.Linq;
using ParkingBuddy.Views;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ParkingBuddy.ViewModel
{
    public partial class UserMainPageViewModel : ObservableObject, IQueryAttributable
    {
        private readonly BackendClient _client = new("http://34.118.78.253/", new HttpClient());

        [ObservableProperty]
        UserDataModel? userModel;

        [ObservableProperty]
        ObservableCollection<string> plates = [];


        [ObservableProperty]
        string errorMessage = "";

        void IQueryAttributable.ApplyQueryAttributes(IDictionary<string, object> query)
        {
            UserModel = query[nameof(UserDataModel)] as UserDataModel;
            if (UserModel != null)
            {
                foreach (var plate in UserModel.Registration_plates)
                {
                    Plates.Add(plate[0..2] + " " + plate[2..6] + " " + plate[6..8]);
                }
            }
        }

        [ObservableProperty]
        string addPlateText = "Add new registration plate";

        [ObservableProperty]
        string newPlateText = "";

        [RelayCommand]
        async Task RegistrationPlateSelected(string clickedPlate)
        {
            try
            {
                var response = await _client.Get_entry_data_entry_data_postAsync(new RegistrationModel() { Registration_plate = clickedPlate[0..2] + clickedPlate[3..7] + clickedPlate[8..10] });
                if (response != null)
                {
                    await Shell.Current.GoToAsync(nameof(EntryDetailsPage), new Dictionary<string, object>
                    {
                        { nameof(ICollection<EntryDataModel>), response },
                        { "plate", clickedPlate }
                    });
                    UserModel = null;
                    Plates = [];
                }
                else
                {
                    ErrorMessage = "Did not receive response from backend. Service may be down.";
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
        void AddNewPlate()
        {
            try
            {
                if (UserModel != null)
                {
                    var result = _client.Create_new_plate_plates_new_postAsync(new CreatePlateModel() {
                        Email = UserModel.Email,
                        Registration_plate = NewPlateText.ToUpper()
                    }).Result;
                }
            }
            catch (AggregateException ex)
            {
                try
                {
                    if (ex.InnerException is ApiException inner)
                    {
                        if (inner.StatusCode != 201)
                        {
                            try
                            {
                                ErrorMessage = JObject.Parse(inner.Response).Value<string>("message") ?? "Shit";
                            }
                            catch
                            {
                                ErrorMessage = ex.Message;
                            }
                        }
                        else
                        {
                            string plate = NewPlateText.ToUpper();
                            Plates.Add(plate[0..2] + " " + plate[2..6] + " " + plate[6..8]);
                            UserModel?.Registration_plates.Add(plate);
                            NewPlateText = "";
                            ErrorMessage = "";
                        }
                    }
                    else
                    {
                        ErrorMessage = ex.Message;
                    }
                }
                catch
                {
                    ErrorMessage = ex.Message;
                }
            }
        }
    }
}
