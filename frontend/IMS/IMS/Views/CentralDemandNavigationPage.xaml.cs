using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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


namespace IMS.Views
{
    /// <summary>
    /// Interaction logic for CentralDemandNavigationPage.xaml
    /// </summary>
    public partial class CentralDemandNavigationPage : Page
    {
        public ObservableCollection<CDS> CDSList { get; set; }

            private string _eqptCode;

            public CentralDemandNavigationPage(string eqptCode)
            {
                InitializeComponent();
                _eqptCode = eqptCode;

                CDSList = new ObservableCollection<CDS>();
                DataContext = this;

                LoadCDS();
            }


        private async void LoadCDS()
        {
            try
            {
                var list = await ApiService.GetCDSAsync(); // all CDS
                CDSList.Clear();

                var filtered = list.Where(x => x.eqpt_code == _eqptCode);

                foreach (var item in filtered)
                    CDSList.Add(item);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Failed to load CDS data.\n" + ex.Message,
                                "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            var window = Window.GetWindow(this);
        }
    }

}
