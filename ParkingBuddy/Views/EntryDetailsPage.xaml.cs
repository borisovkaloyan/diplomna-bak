using ParkingBuddy.ViewModel;

namespace ParkingBuddy.Views;

public partial class EntryDetailsPage : ContentPage
{
	public EntryDetailsPage()
	{
		InitializeComponent();
		BindingContext = new EntryDetailsPageViewModel();
	}

    private void Pay(object sender, EventArgs e)
    {
		if (sender is Button button)
        {
            button.IsVisible = false;
            if (button.Parent.FindByName("IsPaidLabel") is Label label)
            {
                label.IsVisible = true;
            }
        }
    }
}