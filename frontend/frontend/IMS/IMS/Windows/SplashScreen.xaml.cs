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
using System.Windows.Media.Animation;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace IMS.Windows
{
    /// <summary>
    /// Interaction logic for SplashScreen.xaml
    /// </summary>
    public partial class SplashScreen : Window
    {
        public SplashScreen()
        {
            InitializeComponent();
        }
        private async void IntroVideo_MediaEnded(object sender, RoutedEventArgs e)
        {
            // Fade out
            //var fade = new DoubleAnimation(1, 0, TimeSpan.FromSeconds(0.5));
            //this.BeginAnimation(OpacityProperty, fade);
            //await Task.Delay(500);

            //// Show login window
            //var login = new Windows.LoginWindow();
            //bool? result = login.ShowDialog();

            //if (result == true)
            //{
            //    var main = new MainWindow();
            //    main.Show();
            //}

            //this.Close();
        }

    }
}
