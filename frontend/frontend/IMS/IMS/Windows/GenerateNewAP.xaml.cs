using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
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
    /// Interaction logic for GenerateNewAP.xaml
    /// </summary>
    public partial class GenerateNewAP : Window
    {
        public GenerateNewAP()
        {
            InitializeComponent();

            cmbEquipment.ItemsSource = new[] { "Gun", "Tank", "Radar" };
            cmbEquipment.SelectedIndex = 0;
        }
        private static readonly Regex _numRegex = new Regex("^[0-9]+$");
        private void Numeric_PreviewTextInput(object sender, TextCompositionEventArgs e)
            => e.Handled = !_numRegex.IsMatch(e.Text);

        private void Ok_Click(object sender, RoutedEventArgs e)
        {

            if (string.IsNullOrWhiteSpace(txtDemandNo.Text))
            {
                MessageBox.Show("Demand No is required.", "Validation", MessageBoxButton.OK, MessageBoxImage.Exclamation);
                return;
            }
            DialogResult = true;
            this.Close();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e) => this.Close();

        private void Help_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Fill the form and press Ok to generate AP demand.", "Help");

        // “...” pickers – wire to your dialogs or lookups
        private void LedgerPicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Ledger Name picker here.");
        private void ScalePicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Scale/Issue picker here.");
        private void AssyPicker_Click(object sender, RoutedEventArgs e)
            => MessageBox.Show("Open Assy/Component picker here.");

        private void cmbYear_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }
    }
}



