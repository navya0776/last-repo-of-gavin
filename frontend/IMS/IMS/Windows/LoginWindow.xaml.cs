using IMS.Services;
using IMS.Views;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace IMS.Windows
{
    public partial class LoginWindow : Window
    {
        public class LoginResponse
        {
            public string message { get; set; }
            public bool is_admin { get; set; }
            public bool is_new_user { get; set; }
        }

        public LoginWindow()
        {
            InitializeComponent();

            UsernameWatermark.Visibility = Visibility.Visible;
            PasswordWatermark.Visibility = Visibility.Visible;

            // ENTER navigation
            UsernameBox.KeyDown += TxtUsername_KeyDown;
            PasswordBox.KeyDown += TxtPassword_KeyDown;
        }

        private void TxtUsername_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
                PasswordBox.Focus();
        }

        private void TxtPassword_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
                Login_Click(sender, e);
        }

        private void UsernameBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            UsernameWatermark.Visibility =
                string.IsNullOrWhiteSpace(UsernameBox.Text)
                ? Visibility.Visible
                : Visibility.Hidden;
        }

        private void PasswordBox_PasswordChanged(object sender, RoutedEventArgs e)
        {
            PasswordWatermark.Visibility =
                string.IsNullOrWhiteSpace(PasswordBox.Password)
                ? Visibility.Visible
                : Visibility.Hidden;
        }

        private async void Login_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(UsernameWatermark.Text) ||
                string.IsNullOrWhiteSpace(PasswordBox.Password))
            {
                ShowError("Username and password required!");
                return;
            }

            var payload = new
            {
                username = UsernameBox.Text,
                password = PasswordBox.Password
            };

            var data = await ApiClient.PostAsync<LoginResponse>("auth/login", payload);

            if (data == null)
            {
                ShowError("Invalid credentials!");
                return;
            }

            var main = new MainWindow();
            Application.Current.MainWindow = main;
            main.Show();

            if (data.is_admin)
            {
                main.MainFrame.Navigate(new AdminDashboatd());
            }

            this.Hide();
        }

        private void ShowError(string message)
        {
            ErrorText.Text = message;
            ErrorPopup.IsOpen = true;
        }

        private void CloseErrorPopup_Click(object sender, RoutedEventArgs e)
        {
            ErrorPopup.IsOpen = false;
        }

    }
}
