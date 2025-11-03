
using DocumentFormat.OpenXml.Office2016.Excel;
using DocumentFormat.OpenXml.Spreadsheet;
using IMS.Services;
using IMS.Views;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Linq.Expressions;
using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Text;
using System.Threading.Tasks;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;




namespace IMS.Windows
{
    /// <summary>
    /// Interaction logic for Window1.xaml
    /// </summary>


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
        }

        private void UsernameBox_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
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
            if (string.IsNullOrWhiteSpace(UsernameBox.Text) ||
                string.IsNullOrWhiteSpace(PasswordBox.Password))
            {
                MessageBox.Show("Username and password required!");
                return;
            }


            var payload = new { username = UsernameBox.Text, password = PasswordBox.Password };

            var data = await ApiClient.PostAsync<LoginResponse>("auth/login", payload);


            if (data == null)
            {
                MessageBox.Show("Invalid credentials!");
                return;
            }

            var main = new MainWindow();
            Application.Current.MainWindow = main;
            main.Show();

            if (data.is_admin)
            {
                main.MainFrame.Navigate(new AdminDashboatd());
            }
            else
            {
                if (data.is_new_user)
                {
                    var popup = new ChangePasswordWindow();
                    popup.ShowDialog();
                }

                main.MainFrame.Navigate(new Dashboard());
            }



            this.Hide();
        }







        private void Close_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private async Task<LoginResponse?> Authenticate(string username, string password)
        {
            var payload = new
            {
                username,
                password
            };

            try
            {
                HttpResponseMessage response =
                    await Services.ApiClient._client.PostAsJsonAsync("auth/login", payload);

                if (!response.IsSuccessStatusCode)
                    return null;

                var data = await response.Content.ReadFromJsonAsync<LoginResponse>();
                return data;
            }
            catch
            {
                MessageBox.Show("Could not connect to server!");
                return null;
            }
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
