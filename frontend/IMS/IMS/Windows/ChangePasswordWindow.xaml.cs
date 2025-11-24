using IMS.Services;
using System.Windows;

namespace IMS.Windows
{
    public partial class ChangePasswordWindow : Window
    {
        private string _username;

        public ChangePasswordWindow(string username)
        {
            InitializeComponent();
            _username = username;

            UsernameBox.Text = username;
            UsernameBox.IsEnabled = false;
        }

        private async void ChangePassword_Click(object sender, RoutedEventArgs e)
        {
            ErrorBlock.Visibility = Visibility.Collapsed;

            if (string.IsNullOrWhiteSpace(PasswordBox.Password) ||
                string.IsNullOrWhiteSpace(ConfirmPasswordBox.Password))
            {
                ShowError("All fields are required.");
                return;
            }

            if (PasswordBox.Password != ConfirmPasswordBox.Password)
            {
                ShowError("Passwords do not match.");
                return;
            }

            var success = await ApiService.ForgetPasswordAsync(
                _username,
                PasswordBox.Password
            );

            if (!success)
            {
                ShowError("Failed to update password.");
                return;
            }

            MessageBox.Show("Password changed successfully!");

            this.Close();
        }

        private void ShowError(string msg)
        {
            ErrorBlock.Text = msg;
            ErrorBlock.Visibility = Visibility.Visible;
        }
    }
}
