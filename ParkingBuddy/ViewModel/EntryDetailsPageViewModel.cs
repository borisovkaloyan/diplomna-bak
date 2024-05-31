using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;
using ParkingBuddy;
using Newtonsoft.Json.Linq;
using System.Collections.ObjectModel;
using System.ComponentModel;

namespace ParkingBuddy
{
    public partial class EntryDataModel : ObservableObject
    {
        [ObservableProperty]
        string exitTimeString = "------";

        [ObservableProperty]
        string enterTimeString = "------";
    }
}

namespace ParkingBuddy.ViewModel
{
    
    public partial class EntryDetailsPageViewModel : ObservableObject, IQueryAttributable
    {
        private readonly BackendClient _client = new("http://34.118.78.253/", new HttpClient());

        [ObservableProperty]
        string? plate;

        [ObservableProperty]
        ObservableCollection<EntryDataModel> entryData = [];

        [ObservableProperty]
        string entryIntro = "Parking entries for ";

        [ObservableProperty]
        string errorMessage = "";

        public void ApplyQueryAttributes(IDictionary<string, object> query)
        {
            if (query[nameof(ICollection<EntryDataModel>)] is ICollection<EntryDataModel> receivedData)
            {
                foreach (var item in receivedData)
                {
                    EntryData.Add(item);
                }
            }

            if (EntryData != null)
            {
                foreach(var data in EntryData)
                {
                    if (data.Exit_time != new DateTimeOffset())
                    {
                        data.ExitTimeString = data.Exit_time.ToString();
                    }
                    data.EnterTimeString = data.Entry_time.ToString();
                }
            }
            Plate = query["plate"] as string;
        }

        [RelayCommand]
        public async Task PayEntry(EntryDataModel entry)
        {
            try
            {
                var response = await _client.Pay_entry_entry_pay_postAsync(new PayEntryModel() { Entry_id = entry.Id });
                if (response != null && EntryData != null)
                {
                    entry.Is_paid = false;
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
    }
}
