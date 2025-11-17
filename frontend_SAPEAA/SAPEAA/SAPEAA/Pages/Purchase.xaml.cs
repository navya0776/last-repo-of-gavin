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

namespace SAPEAA.Pages
{
    /// <summary>
    /// Interaction logic for Purchase.xaml
    /// </summary>
    public partial class Purchase : Page
    {
        public Purchase()
        {
            InitializeComponent();
            var vm = new SAPEAA.ViewModels.ViewModel();
            this.DataContext = vm;

            // If role manager already had a role, set vm:
            if (!string.IsNullOrEmpty(SAPEAA.Services.RoleManager.CurrentRole))
                vm.SelectedRole = SAPEAA.Services.RoleManager.CurrentRole;
        }

        private void Analysis_Click(object sender, RoutedEventArgs e)
        {
            // Navigate to analysis page - adjust to your page type
            var asm = typeof(Purchase).Assembly;
            var t = asm.GetType("SAPEAA.Pages.Analysis");
            if (t != null)
            {
                var page = Activator.CreateInstance(t) as Page;
                var main = Application.Current.MainWindow as MainWindow;
                main?.RootFrame?.Navigate(page);
            }
            else
            {
                MessageBox.Show("Analysis page not found", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void Tile_Click(object sender, RoutedEventArgs e)
        {
            if (DataContext is not SAPEAA.ViewModels.ViewModel vm || vm.SelectedRole == null)
            {
                MessageBox.Show("No financial head selected.", "Error!", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            if (sender is not Button btn || btn.Tag is not string pageKey) return;

            // Map tag => page Type (adjust types/names to your project)
            Type? pageType = pageKey switch
            {
                "Job" => typeof(SAPEAA.NavigatingPages.Job),
                "CRV" => typeof(SAPEAA.NavigatingPages.CRV),
                "LPR" => typeof(SAPEAA.NavigatingPages.LPR),
                "Bill" => typeof(SAPEAA.NavigatingPages.Bill),
                "Indent" => typeof(SAPEAA.NavigatingPages.Indent),
                "Database" => typeof(SAPEAA.NavigatingPages.Database),
                "Order" => typeof(SAPEAA.NavigatingPages.Order),
                "Query" => typeof(SAPEAA.NavigatingPages.Query),
                "InspNote" => typeof(SAPEAA.NavigatingPages.InspNote),
                "System" => typeof(SAPEAA.NavigatingPages.SystemNew),
                "AnalysisPurchase" => typeof(SAPEAA.NavigatingPages.AnalysisPurchase),
                _ => null
            };

            if (pageType == null)
            {
                MessageBox.Show($"Page for '{pageKey}' not found.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            var pageInstance = Activator.CreateInstance(pageType) as Page;
            if (pageInstance == null)
            {
                MessageBox.Show($"Unable to create page {pageType.FullName}.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }

            // Navigate via a Frame named RootFrame on MainWindow
            var main = Application.Current.MainWindow as MainWindow;
            main?.RootFrame?.Navigate(pageInstance);
        }

        

        private static Type GetTypeByName(string fullName)
        {
            return typeof(Purchase).Assembly.GetType(fullName);
        }

    }
}
