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
using System.Windows.Shapes;

namespace IMS.Windows
{

    public partial class ReportsPageLedger : Window
    {
        public string SelectedReport { get; private set; } = null;

        public ReportsPageLedger()
        {
            InitializeComponent();
        }
        private void OkButton_Click(object sender, RoutedEventArgs e)
        {
            if (ReportsList.SelectedItem is ListBoxItem selected)
            {
                SelectedReport = selected.Content.ToString();
                this.DialogResult = true;
            }
            else
            {
                MessageBox.Show("Please select a report.", "No Selection", MessageBoxButton.OK, MessageBoxImage.Warning);
            }
        }

        private void CancelButton_Click(object sender, RoutedEventArgs e)
        {
            this.DialogResult = false;
        }
    }
}
