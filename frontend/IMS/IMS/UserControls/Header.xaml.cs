using IMS.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace IMS.UserControls
{
    /// <summary>
    /// Interaction logic for UserControl1.xaml
    /// </summary>
    public partial class Header : UserControl
    {
        public event EventHandler ToggleSidebarRequested;

        public Header()
        {
            InitializeComponent();
        }

        private void MyButton_Click(object sender, RoutedEventArgs e)
        {
            ToggleSidebarRequested?.Invoke(this, EventArgs.Empty);

        }


        private async void LogoutButton_Click(object sender, RoutedEventArgs e)
        {
            bool success = await ApiService.LogoutAsync();

            if (success)
            {
                MessageBox.Show("Logged out successfully.");

                var login = new IMS.Windows.LoginWindow();
                login.Show();

                Window.GetWindow(this)?.Close();
            }
            else
            {
                MessageBox.Show("Logout failed.");
            }
        }

    }
}
