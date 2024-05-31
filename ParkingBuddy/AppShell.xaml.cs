using ParkingBuddy.Views;

namespace ParkingBuddy
{
    public partial class AppShell : Shell
    {
        public AppShell()
        {
            Routing.RegisterRoute(nameof(LoginPage) + "/" + nameof(RegistrationPage), typeof(RegistrationPage));
            Routing.RegisterRoute(nameof(UserMainPage), typeof(UserMainPage));
            Routing.RegisterRoute(nameof(EntryDetailsPage), typeof(EntryDetailsPage));
            InitializeComponent();
        }
    }
}
