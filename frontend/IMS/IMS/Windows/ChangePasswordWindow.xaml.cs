using IMS.Services;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace IMS.Windows
{
    public partial class ChangePasswordWindow : Window
    {
        public ChangePasswordWindow()
        {
            InitializeComponent();

            // Show watermark initially
            UsernameWatermark.Visibility = Visibility.Visible;
            PasswordWatermark.Visibility = Visibility.Visible;
            ConfirmPasswordWatermark.Visibility = Visibility.Visible;

            // Event handlers for watermarks
            UsernameBox.TextChanged += (s, e) =>
            {
                UsernameWatermark.Visibility =
                    string.IsNullOrWhiteSpace(UsernameBox.Text)
                    ? Visibility.Visible : Visibility.Hidden;
            };

            PasswordBox.PasswordChanged += (s, e) =>
            {
                PasswordWatermark.Visibility =
                    string.IsNullOrWhiteSpace(PasswordBox.Password)
                    ? Visibility.Visible : Visibility.Hidden;
            };

            ConfirmPasswordBox.PasswordChanged += (s, e) =>
            {
                ConfirmPasswordWatermark.Visibility =
                    string.IsNullOrWhiteSpace(ConfirmPasswordBox.Password)
                    ? Visibility.Visible : Visibility.Hidden;
            };

            // Allow Enter key behavior
            UsernameBox.KeyDown += UsernameBox_KeyDown;
            PasswordBox.KeyDown += PasswordBox_KeyDown;
            ConfirmPasswordBox.KeyDown += ConfirmPasswordBox_KeyDown;
        }

        private void UsernameBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
                PasswordBox.Focus();
        }

        private void PasswordBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
                ConfirmPasswordBox.Focus();
        }

        private void ConfirmPasswordBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
                ChangePassword_Click(null, null);
        }

        private async void ChangePassword_Click(object sender, RoutedEventArgs e)
        {
            ErrorBlock.Visibility = Visibility.Collapsed;

            if (string.IsNullOrWhiteSpace(UsernameBox.Text) ||
                string.IsNullOrWhiteSpace(PasswordBox.Password) ||
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

            bool success = await ApiService.ForgetPasswordAsync(
                UsernameBox.Text.Trim(),
                PasswordBox.Password.Trim()
            );

            if (!success)
            {
                ShowError("Failed to update password. Try again.");
                return;
            }

            MessageBox.Show("Password changed successfully!");

            this.Close(); // Close popup
        }

        private void ShowError(string msg)
        {
            ErrorBlock.Text = msg;
            ErrorBlock.Visibility = Visibility.Visible;
        }
    }
}
