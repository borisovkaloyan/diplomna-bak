using ParkingBuddy.ViewModel;

namespace ParkingBuddy.Views;

public partial class RegistrationPage : ContentPage
{
	public RegistrationPage()
	{
		InitializeComponent();
        BindingContext = new RegistrationPageViewModel();
    }
}