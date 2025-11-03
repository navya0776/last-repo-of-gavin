using System.Configuration;
using System.Data;
using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace IMS
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            Windows.LoginWindow login = new Windows.LoginWindow();
            bool? result = login.ShowDialog();

            if (result == true)
            {
                MainWindow main = new MainWindow();
                main.Show();
            }
            else
            {
                 // exit app if login fails
            }
        }

        public class StringNullOrEmptyToVisibilityConverter : IValueConverter
        {
            public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
            {
                return string.IsNullOrEmpty(value as string)
                    ? Visibility.Collapsed
                    : Visibility.Visible;
            }

            public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            {
                throw new NotImplementedException();
            }
        }
    }
}
