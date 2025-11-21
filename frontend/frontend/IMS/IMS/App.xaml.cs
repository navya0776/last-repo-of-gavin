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
        //protected override void OnStartup(StartupEventArgs e)
        //{
        //    base.OnStartup(e);

        //    // Start Splash Video instead of Login
        //    var splash = new Windows.SplashScreen();
        //    splash.Show();
        //}


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
