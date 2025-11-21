using System.Windows;
using System.Windows.Media;

namespace IMS
{
    public partial class MainWindow : Window
    {
        private bool isStoreExpanded = false;

        public MainWindow()
        {
            InitializeComponent();
            MainFrame.Navigate(new Views.Ledger());
            HeaderControl.ToggleSidebarRequested += OnToggleSidebarRequested;

        }

        private void Header_Loaded(object sender, RoutedEventArgs e)
        {

        }

        private void OnToggleSidebarRequested(object sender, EventArgs e)
        {
            var sidebar = SidebarControl.SideBar;
            var transform = new System.Windows.Media.TranslateTransform();
            sidebar.RenderTransform = transform;

            // Determine animation direction
            double from = sidebar.Visibility == Visibility.Visible ? 0 : -200;
            double to = sidebar.Visibility == Visibility.Visible ? -200 : 0;

            var anim = new System.Windows.Media.Animation.DoubleAnimation
            {
                From = from,
                To = to,
                Duration = TimeSpan.FromMilliseconds(300),
                EasingFunction = new System.Windows.Media.Animation.CubicEase()
            };

            transform.BeginAnimation(System.Windows.Media.TranslateTransform.XProperty, anim);
            sidebar.Visibility = sidebar.Visibility == Visibility.Visible ? Visibility.Collapsed : Visibility.Visible;
        }


    }
}
