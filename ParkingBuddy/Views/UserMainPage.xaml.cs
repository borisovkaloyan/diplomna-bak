using ParkingBuddy.ViewModel;

namespace ParkingBuddy.Views;

public partial class UserMainPage : ContentPage
{
	public UserMainPage()
	{
		InitializeComponent();
        BindingContext = new UserMainPageViewModel();
    }

    protected override bool OnBackButtonPressed()
    {
        // Navigate back to the LoginPage
        Device.BeginInvokeOnMainThread(async () =>
        {
            await Navigation.PopToRootAsync();
        });
        return true; // Prevent the default back button action
    }
}