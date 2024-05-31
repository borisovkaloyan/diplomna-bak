using ParkingBuddy.ViewModel;

namespace ParkingBuddy.Views;

public partial class UserMainPage : ContentPage
{
	public UserMainPage()
	{
		InitializeComponent();
        BindingContext = new UserMainPageViewModel();
    }
}